"""Seed the official-format Kankor exam blueprint.

Run: python seed_blueprint.py

فورمت رسمی کانکور عمومی: ۱۶۰ سوال چهارجوابه، نمره کل ۳۶۰ (تایید شده از NEXA).
⚠️ تعداد دقیق سوال هر مضمون به‌صورت رسمی منتشر نمی‌شود — اعداد زیر باید توسط
تیم محتوا با شمارش یک فورم واقعی (PDF فورم‌های ۱۴۰۱ یا بانک انیس ۱۳۹۸/۱۳۹۹)
تایید و در صورت نیاز از طریق PATCH /mock-kankor/blueprints اصلاح شود.
"""

import asyncio

from sqlalchemy import select

from app.database import SessionLocal
from app.modules.question_bank.models import ExamBlueprint

BLUEPRINT_NAME = "کانکور آزمایشی کامل (فورم عمومی)"

# ⚠️ TO VERIFY against a real form — see docstring. Sums to 160.
SECTIONS = [
    {"subject": "ریاضی", "count": 30},
    {"subject": "فزیک", "count": 24},
    {"subject": "کیمیا", "count": 24},
    {"subject": "بیولوژی", "count": 24},
    {"subject": "دری", "count": 12},
    {"subject": "پشتو", "count": 6},
    {"subject": "تعلیمات اسلامی", "count": 12},
    {"subject": "تاریخ", "count": 10},
    {"subject": "جغرافیه", "count": 8},
    {"subject": "انگلیسی", "count": 10},
]

TOTAL_MINUTES = 180  # ~۳ ساعت مطابق امتحان واقعی


async def seed():
    assert sum(s["count"] for s in SECTIONS) == 160, "sections must sum to 160"
    async with SessionLocal() as db:
        existing = (await db.execute(
            select(ExamBlueprint).where(ExamBlueprint.name_fa == BLUEPRINT_NAME)
        )).scalar_one_or_none()
        if existing:
            existing.sections = SECTIONS
            existing.total_minutes = TOTAL_MINUTES
            existing.is_active = True
            await db.commit()
            print(f"Updated existing blueprint: {BLUEPRINT_NAME}")
            return

        db.add(ExamBlueprint(
            name_fa=BLUEPRINT_NAME,
            description_fa=(
                "ساختار فورم عمومی کانکور: ۱۶۰ سوال، ~۱۸۰ دقیقه. "
                "⚠️ تعداد سوال هر مضمون باید با یک فورم رسمی واقعی تایید شود."
            ),
            total_minutes=TOTAL_MINUTES,
            sections=SECTIONS,
            is_active=True,
        ))
        await db.commit()
        print(f"Created blueprint: {BLUEPRINT_NAME} — {len(SECTIONS)} sections, 160 questions, {TOTAL_MINUTES} min")
        print("⚠️  Verify per-subject counts against a real form PDF, then PATCH /mock-kankor/blueprints if needed.")


if __name__ == "__main__":
    asyncio.run(seed())
