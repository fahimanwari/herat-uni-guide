from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.core.exceptions import NotFoundError

app = FastAPI(title="Herat University Guide API", version="1.0")

# CORS — dev (localhost) + production (guide.hu.edu.af)
origins = [o.strip() for o in settings.allowed_origins.split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(NotFoundError)
async def not_found_handler(request: Request, exc: NotFoundError):
    return JSONResponse(status_code=404, content={"detail": exc.message})


@app.get("/health")
async def health():
    return {"status": "ok"}


# Modules — one line added per new module
from app.modules.universities.router import router as universities_router
from app.modules.faculties.router import router as faculties_router
from app.modules.departments.router import router as departments_router
from app.modules.news.router import router as news_router
from app.modules.faqs.router import router as faqs_router
from app.modules.kankor.router import router as kankor_router
from app.modules.quiz.router import router as quiz_router
from app.modules.ai.router import router as ai_router
from app.modules.ai.admin_router import router as rag_admin_router
from app.modules.admin_auth.router import router as admin_auth_router
from app.modules.notifications.router import router as notifications_router
from app.modules.exam.router import router as exam_router
from app.modules.users.router import router as users_router
from app.modules.question_bank.router import router as question_bank_router

app.include_router(universities_router, prefix="/api/v1")
app.include_router(faculties_router, prefix="/api/v1")
app.include_router(departments_router, prefix="/api/v1")
app.include_router(news_router, prefix="/api/v1")
app.include_router(faqs_router, prefix="/api/v1")
app.include_router(kankor_router, prefix="/api/v1")
app.include_router(quiz_router, prefix="/api/v1")
app.include_router(ai_router, prefix="/api/v1")
app.include_router(rag_admin_router, prefix="/api/v1")
app.include_router(admin_auth_router, prefix="/api/v1")
app.include_router(notifications_router, prefix="/api/v1")
app.include_router(exam_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")
app.include_router(question_bank_router, prefix="/api/v1")

# SQLAdmin — import after app is created
from app.admin import admin  # noqa: E402, F401
