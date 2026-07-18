import uuid
from fastapi import APIRouter, Depends, Query, Request
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db
from app.core.security import get_current_admin
from app.core.rate_limit import rate_limiter
from .service import QuestionBankService
from .schemas import GenerateExamRequest, QuestionBankItem, QuestionBankCreate

router = APIRouter(prefix="/question-bank", tags=["question-bank"])


# --- Public endpoints ---

@router.get("/stats")
async def get_stats(db: AsyncSession = Depends(get_db)):
    return await QuestionBankService(db).get_stats()


@router.post("/generate-exam")
async def generate_exam(payload: GenerateExamRequest, db: AsyncSession = Depends(get_db)):
    return await QuestionBankService(db).generate_exam(
        subject=payload.subject,
        num_questions=payload.num_questions,
        difficulty=payload.difficulty,
    )


@router.get("/questions")
async def list_questions(
    subject: str | None = None,
    year: int | None = None,
    grade: str | None = None,
    limit: int = Query(50, le=500),
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
):
    return await QuestionBankService(db).list_questions(subject, limit, offset, year=year, grade=grade)


# --- Admin CRUD (requires auth) ---

@router.post("/questions", response_model=QuestionBankItem)
async def create_question(
    payload: QuestionBankCreate,
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return await QuestionBankService(db).create_question(payload)


@router.patch("/questions/{question_id}", response_model=QuestionBankItem)
async def update_question(
    question_id: uuid.UUID,
    payload: QuestionBankItem,
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return await QuestionBankService(db).update_question(question_id, payload)


@router.delete("/questions/{question_id}")
async def delete_question(
    question_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return await QuestionBankService(db).delete_question(question_id)


@router.post("/import")
async def import_questions(
    questions: list[dict],
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return await QuestionBankService(db).import_questions(questions)


class OcrRequest(BaseModel):
    image_base64: str


@router.post("/ocr")
async def ocr_extract(
    payload: OcrRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_current_admin),
):
    """Extract questions from image using Gemini vision."""
    client_ip = request.client.host
    await rate_limiter.check_rate_limit(f"ocr:{client_ip}", limit=10, window=86400)

    from app.providers.ai.factory import get_ai_provider
    from app.config import settings

    if settings.ai_provider != "gemini":
        return {"error": "OCR فقط با Gemini کار می‌کند", "questions": []}

    provider = get_ai_provider()
    if not hasattr(provider, "chat_with_image"):
        return {"error": "این provider از تصویر پشتیبانی نمی‌کند", "questions": []}

    prompt = """این تصویر شامل سوالات چهارجوابه کانکور است. لطفاً سوالات را به این فورمت JSON استخراج کن:
[{
  "subject": "مضمون (ریاضی/فزیک/کیمیا/بیولوژی/دری/پشتو/تعلیمات اسلامی/تاریخ/جغرافیه/انگلیسی)",
  "year": 1402,
  "source": "منبع",
  "difficulty": "easy/medium/hard",
  "question_fa": "متن سوال",
  "options": [{"text": "گزینه ۱", "is_correct": true}, {"text": "گزینه ۲"}, {"text": "گزینه ۳"}, {"text": "گزینه ۴"}],
  "explanation_fa": "توضیح (اختیاری)"
}]
فقط JSON برگردان، هیچ متن اضافی ننویس."""

    try:
        result = await provider.chat_with_image(prompt, payload.image_base64)
        # Try to parse JSON from response
        import json
        # Find JSON array in response
        match = re.search(r'\[.*\]', result, re.DOTALL)
        if match:
            questions = json.loads(match.group())
            return {"questions": questions, "count": len(questions)}
        return {"error": "فرمت پاسخ AI قابل پردازش نیست", "raw": result, "questions": []}
    except Exception as e:
        return {"error": f"خطا در استخراج: {str(e)}", "questions": []}


import re
