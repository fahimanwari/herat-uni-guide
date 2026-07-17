"""
Seed news, FAQs, and more department data for all 16 faculties.
Run: python seed_content.py
"""

import asyncio
import uuid

from app.database import SessionLocal, engine, Base
from app.modules.universities.models import University
from app.modules.faculties.models import Faculty
from app.modules.departments.models import Department
from app.modules.kankor.models import KankorCutoff
from app.modules.news.models import News
from app.modules.faqs.models import Faq


async def seed():
    async with SessionLocal() as db:
        # Get university
        from sqlalchemy import select
        uni = (await db.execute(select(University))).scalars().first()
        if not uni:
            print("No university found. Run seed.py first!")
            return

        # --- News ---
        news_data = [
            {
                "university_id": uni.id,
                "title_fa": "آغاز ثبت‌نام کانکور ۱۴۰۵",
                "body_fa": "ثبتنام امتحان کانکور سال ۱۴۰۵ از تاریخ ۱ جوزا آغاز می‌شود. شاگردان صنف ۱۲ مکتب می‌توانند از طریق مکاتب خود ثبت‌نام کنند.",
                "is_published": True,
                "send_notification": True,
            },
            {
                "university_id": uni.id,
                "title_fa": "نتایج امتحانات نیم‌سال اول اعلان شد",
                "body_fa": "نتایج امتحانات نیم‌سال اول سال تحصیلی ۱۴۰۴ اعلان شد. محصلان می‌توانند از طریق پورتال محصلانی نتایج خود را ببینند.",
                "is_published": True,
                "send_notification": False,
            },
            {
                "university_id": uni.id,
                "title_fa": "همایش علمی پوهنځی کمپیوتر ساینس",
                "body_fa": "همایش علمی تحت عنوان «آینده هوش مصنوعی در افغانستان» توسط پوهنځی کمپیوتر ساینس برگزار می‌شود.",
                "is_published": True,
                "send_notification": False,
            },
            {
                "university_id": uni.id,
                "title_fa": "بورسیه تحصیلی برای محصلان ممتاز",
                "body_fa": "پوهنتون هرات بورسیه تحصیلی برای محصلان ممتاز در سال تحصیلی ۱۴۰۵ اعلام کرد. متقاضیان تا ۳۰ جوزا درخواست دهند.",
                "is_published": True,
                "send_notification": True,
            },
        ]

        for nd in news_data:
            db.add(News(id=uuid.uuid4(), **nd))
        await db.commit()
        print(f"News: {len(news_data)} added")

        # --- FAQs ---
        faq_data = [
            {
                "university_id": uni.id,
                "question_fa": "شرایط ثبت‌نام کانکور چیست؟",
                "answer_fa": "برای ثبت‌نام در کانکور باید شاگرد صنف ۱۲ مکتب باشید و نمره مکتبی شما حداقل ۶۰٪ باشد. ثبت‌نام از طریق مکتب صورت می‌گیرد.",
                "category": "کانکور",
                "sort_order": 1,
            },
            {
                "university_id": uni.id,
                "question_fa": "آیا پوهنتون هرات خوابگاه دارد؟",
                "answer_fa": "بله، پوهنتون هرات برای محصلان ولایات دور خوابگاه دارد. برای ثبت‌نام در خوابگاه به اداره محصلانی مراجعه کنید.",
                "category": "عمومی",
                "sort_order": 2,
            },
            {
                "university_id": uni.id,
                "question_fa": "هزینه تحصیل چقدر است؟",
                "answer_fa": "تحصیل در پوهنتون‌های دولتی افغانستان رایگان است. فقط هزینه ثبت‌نام اولیه و مواد درسی بر عهده محصل است.",
                "category": "عمومی",
                "sort_order": 3,
            },
            {
                "university_id": uni.id,
                "question_fa": "آیا امکان انتقال از پوهنتون دیگر وجود دارد؟",
                "answer_fa": "بله، انتقال از پوهنتون‌های دیگر ممکن است. باید ریز نمرات و مدارک لازم را به اداره تحصیلات پیشرفته ارائه دهید.",
                "category": "انتقال",
                "sort_order": 4,
            },
            {
                "university_id": uni.id,
                "question_fa": "آیا پوهنتون کورس‌های آنلاین دارد؟",
                "answer_fa": "بله، پوهنتون هرات کورس‌های آنلاین در برخی رشته‌ها ارائه می‌دهد. برای اطلاعات بیشتر به پورتال آموزشی مراجعه کنید.",
                "category": "آموزش",
                "sort_order": 5,
            },
            {
                "university_id": uni.id,
                "question_fa": "چگونه می‌توانم استادان یک پوهنځی را ببینم؟",
                "answer_fa": "از طریق صفحه پوهنځی مربوطه در این وبسایت می‌توانید لیست استادان و تخصص‌های آنها را ببینید.",
                "category": "عمومی",
                "sort_order": 6,
            },
            {
                "university_id": uni.id,
                "question_fa": "آیا پوهنتون برنامه‌های تحقیقاتی دارد؟",
                "answer_fa": "بله، پوهنتون هرات برنامه‌های تحقیقاتی متعددی در حوزه‌های مختلف علمی دارد. علاقه‌مندان می‌توانند با پوهنځی مربوطه تماس بگیرند.",
                "category": "تحقیق",
                "sort_order": 7,
            },
            {
                "university_id": uni.id,
                "question_fa": "زبان تدریس در پوهنتون چیست؟",
                "answer_fa": "زبان اصلی تدریس دری و پشتو است. در برخی رشته‌ها انگلیسی نیز استفاده می‌شود.",
                "category": "آموزش",
                "sort_order": 8,
            },
            {
                "university_id": uni.id,
                "question_fa": "آیا پوهنتون بازار کار دارد؟",
                "answer_fa": "بله، پوهنتون هرات با نهادهای دولتی و خصوصی همکاری دارد و به فارغ‌التحصیلان در یافتن کار کمک می‌کند.",
                "category": "فراغت",
                "sort_order": 9,
            },
            {
                "university_id": uni.id,
                "question_fa": "تقویم اکادمیک پوهنتون چیست؟",
                "answer_fa": "سال تحصیلی پوهنتون هرات شامل دو نیم‌سال است: نیم‌سال اول (جوزا-جدی) و نیم‌سال دوم (جدی-سرطان).",
                "category": "عمومی",
                "sort_order": 10,
            },
        ]

        for fd in faq_data:
            db.add(Faq(id=uuid.uuid4(), **fd))
        await db.commit()
        print(f"FAQs: {len(faq_data)} added")

        # --- Extra departments for Medicine faculty ---
        med_faculty = (await db.execute(
            select(Faculty).where(Faculty.slug == "medicine")
        )).scalars().first()

        if med_faculty:
            med_depts = [
                Department(
                    id=uuid.uuid4(),
                    faculty_id=med_faculty.id,
                    slug="internal-medicine",
                    name_fa="داخله",
                    name_en="Internal Medicine",
                    description_fa="دیپارتمنت داخله یکی از مهم‌ترین بخش‌های طب معالجوی است که تشخیص و درمان بیماری‌های داخلی را آموزش می‌دهد.",
                    department_type="degree",
                    duration_years=7,
                    subjects=["فیزیولوژی", "پاتولوژی", "فارماکولوژی", "طب داخلی"],
                    career_paths=[{"title": "داکتر داخله", "desc": "تشخیص و درمان بیماری‌ها"}],
                ),
                Department(
                    id=uuid.uuid4(),
                    faculty_id=med_faculty.id,
                    slug="surgery",
                    name_fa="جراحی",
                    name_en="Surgery",
                    description_fa="دیپارتمنت جراحی آموزش عملی جراحی‌های عمومی و تخصصی را ارائه می‌دهد.",
                    department_type="degree",
                    duration_years=7,
                    subjects=["جراحی عمومی", "جراحی تخصصی", "آناتومی"],
                    career_paths=[{"title": "جراح", "desc": "انجام عملیات جراحی"}],
                ),
            ]
            db.add_all(med_depts)
            await db.commit()
            print(f"Medicine departments: {len(med_depts)} added")

        print("\nDone!")


if __name__ == "__main__":
    asyncio.run(seed())
