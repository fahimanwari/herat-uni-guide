"""
Seed practice exams with questions.
Run: python seed_exams.py
"""

import asyncio
import uuid

from app.database import SessionLocal
from app.modules.exam.models import Exam, ExamQuestion, ExamOption


async def seed():
    async with SessionLocal() as db:
        # --- Exam 1: Kankor Math Practice ---
        exam1 = Exam(
            id=uuid.uuid4(),
            title_fa="تمرین ریاضی — کانکور",
            title_en="Math Practice — Kankor",
            description_fa="سوالات تمرینی ریاضی برای آمادگی کانکور. ۱۰ سوال، ۶۰ دقیقه.",
            category="kankor",
            duration_minutes=60,
            total_questions=10,
            is_active=True,
        )
        db.add(exam1)
        await db.flush()

        math_questions = [
            ("اگر x + 5 = 12 باشد، x چقدر است؟", "7", "5", "12", "17", 0),
            ("مساحت مستطیلی با طول ۸ و عرض ۵ چقدر است؟", "40", "13", "26", "30", 0),
            ("اگر ۲۰٪ از عدد ۱۵۰ کم شود، چقدر می‌ماند؟", "120", "130", "110", "140", 0),
            ("فاضلاب ۱۵ از ۲۳ چقدر است؟", "8", "38", "7", "9", 0),
            ("اگر سرعت ۶۰ کیلومتر در ساعت باشد، در ۲ ساعت چقدر طی می‌شود؟", "120 کیلومتر", "30 کیلومتر", "90 کیلومتر", "60 کیلومتر", 0),
            ("چند عدد اول بین ۱ تا ۲۰ وجود دارد؟", "8", "7", "9", "6", 0),
            ("اگر a = 3 و b = 4 باشد، a² + b² چقدر است؟", "25", "12", "7", "49", 0),
            ("Log₂(8) چقدر است؟", "3", "2", "4", "8", 0),
            ("اگر مثلثی با اضلاع ۳، ۴، ۵ داشته باشیم، آیا قائمالزایا است؟", "بله", "خیر", "فقط اگر زاویه ۹۰ درجه باشد", "غیرممکن است", 0),
            (" Derivative تابع x² چیست؟", "2x", "x²", "2x²", "x", 0),
        ]

        for i, (q, *opts_with_idx) in enumerate(math_questions):
            correct_idx = opts_with_idx[-1]  # last element is correct index
            all_opts = opts_with_idx[:-1]    # all except last are options

            question = ExamQuestion(
                id=uuid.uuid4(),
                exam_id=exam1.id,
                question_fa=q,
                sort_order=i,
                points=1,
            )
            db.add(question)
            await db.flush()

            for j, opt_text in enumerate(all_opts):
                db.add(ExamOption(
                    id=uuid.uuid4(),
                    question_id=question.id,
                    text_fa=str(opt_text),
                    is_correct=(j == correct_idx),
                ))

        # --- Exam 2: Kankor Science Practice ---
        exam2 = Exam(
            id=uuid.uuid4(),
            title_fa="تمرین علوم — کانکور",
            title_en="Science Practice — Kankor",
            description_fa="سوالات تمرینی علوم برای آمادگی کانکور. ۱۰ سوال، ۶۰ دقیقه.",
            category="kankor",
            duration_minutes=60,
            total_questions=10,
            is_active=True,
        )
        db.add(exam2)
        await db.flush()

        science_questions = [
            ("واحد اندازه‌گیری انرژی چیست؟", "ژول", "نیوتن", "وات", "پاسکال", 0),
            ("سریع‌ترین سیاره منظومه شمسی کدام است؟", "عطارد", "زهره", "مریخ", "مشتری", 0),
            ("فرمول آب چیست؟", "H₂O", "CO₂", "O₂", "H₂", 0),
            ("نیروی جاذبه زمین تقریباً چقدر است؟", "9.8 m/s²", "10.5 m/s²", "8.2 m/s²", "11.0 m/s²", 0),
            ("کدام گاز بیشترین درصد جو زمین را تشکیل می‌دهد؟", "نیتروژن", "اکسیژن", "آرگون", "دی‌اکسید کربن", 0),
            ("عدد اتمی کربن چند است؟", "6", "12", "8", "14", 0),
            ("آیا نور در خلأ سریع‌تر حرکت می‌کند یا در آب؟", "خلأ", "آب", "هر دو یکسان", "بستگی به طول موج دارد", 0),
            ("کدام اندام بیشترین انرژی را مصرف می‌کند؟", "مغز", "قلب", "کبد", "کلیه", 0),
            ("فرمول محاسبه سرعت متوسط چیست؟", "مسافت/زمان", "زمان/مسافت", "نیرو×زمان", "جرم×شتاب", 0),
            ("کدام فلز رسانای بهتری برای برق است؟", "مس", "آهن", "آلومینیوم", "سرب", 0),
        ]

        for i, (q, *opts_with_idx) in enumerate(science_questions):
            correct_idx = opts_with_idx[-1]
            all_opts = opts_with_idx[:-1]

            question = ExamQuestion(
                id=uuid.uuid4(),
                exam_id=exam2.id,
                question_fa=q,
                sort_order=i,
                points=1,
            )
            db.add(question)
            await db.flush()

            for j, opt_text in enumerate(all_opts):
                db.add(ExamOption(
                    id=uuid.uuid4(),
                    question_id=question.id,
                    text_fa=str(opt_text),
                    is_correct=(j == correct_idx),
                ))

        # --- Exam 3: CS Department Practice ---
        exam3 = Exam(
            id=uuid.uuid4(),
            title_fa="تمرین کمپیوتر ساینس",
            title_en="Computer Science Practice",
            description_fa="سوالات تمرینی کمپیوتر ساینس برای داوطلبان رشته CS. ۱۰ سوال، ۴۵ دقیقه.",
            category="department",
            duration_minutes=45,
            total_questions=10,
            is_active=True,
        )
        db.add(exam3)
        await db.flush()

        cs_questions = [
            ("کدام زبان برنامه‌نویسی بیشتر برای هوش مصنوعی استفاده می‌شود؟", "Python", "Java", "C++", "JavaScript", 0),
            ("SQL برای چه کاری استفاده می‌شود؟", "مدیریت پایگاه داده", "طراحی وب", "ویرایش عکس", "پخش ویدیو", 0),
            ("HTTP معنای چیست؟", "HyperText Transfer Protocol", "High Tech Transfer Program", "Home Tool Transfer Protocol", "Hyper Text Transmission Process", 0),
            ("کدام یک زبان سطح پایین است؟", "Assembly", "Python", "JavaScript", "Ruby", 0),
            ("RAM مخفف چیست؟", "Random Access Memory", "Read Access Memory", "Run All Memory", "Random Active Memory", 0),
            ("کدام پروتکل برای ارسال ایمیل استفاده می‌شود؟", "SMTP", "HTTP", "FTP", "SSH", 0),
            ("Git برای چه کاری استفاده می‌شود؟", "کنترل نسخه", "ویرایش متن", "مدیریت پایگاه داده", "طراحی وب", 0),
            ("کدام یک سیستم‌عامل نیست؟", "Microsoft Word", "Windows", "Linux", "macOS", 0),
            ("API مخفف چیست؟", "Application Programming Interface", "Advanced Program Integration", "Automatic Process Input", "Application Process Interface", 0),
            ("CPU مخفف چیست؟", "Central Processing Unit", "Computer Personal Unit", "Central Program Utility", "Computer Processing Unit", 0),
        ]

        for i, (q, *opts_with_idx) in enumerate(cs_questions):
            correct_idx = opts_with_idx[-1]
            all_opts = opts_with_idx[:-1]

            question = ExamQuestion(
                id=uuid.uuid4(),
                exam_id=exam3.id,
                question_fa=q,
                sort_order=i,
                points=1,
            )
            db.add(question)
            await db.flush()

            for j, opt_text in enumerate(all_opts):
                db.add(ExamOption(
                    id=uuid.uuid4(),
                    question_id=question.id,
                    text_fa=str(opt_text),
                    is_correct=(j == correct_idx),
                ))

        await db.commit()
        print(f"Exams created:")
        print(f"  1. {exam1.title_fa} ({exam1.total_questions} questions)")
        print(f"  2. {exam2.title_fa} ({exam2.total_questions} questions)")
        print(f"  3. {exam3.title_fa} ({exam3.total_questions} questions)")


if __name__ == "__main__":
    asyncio.run(seed())
