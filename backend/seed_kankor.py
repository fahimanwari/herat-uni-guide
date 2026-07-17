"""
Seed kankor cutoffs and quiz data.
Run: python seed_kankor.py
"""

import asyncio
import uuid

from app.database import SessionLocal, engine, Base
from app.modules.universities.models import University
from app.modules.faculties.models import Faculty
from app.modules.departments.models import Department, StudentProject, AlumniStory, CareerRoadmap
from app.modules.kankor.models import KankorCutoff, KankorGuide
from app.modules.quiz.models import QuizQuestion, QuizOption, DepartmentTraitProfile


async def seed():
    async with SessionLocal() as db:
        # --- Kankor Cutoffs (3 years for CS departments) ---
        depts = (await db.execute(
            __import__("sqlalchemy").select(Department)
            .where(Department.department_type == "degree")
        )).scalars().all()

        cutoff_data = {
            "database-information-systems": [
                (1402, 210, 40), (1403, 215, 45), (1404, 220, 50),
            ],
            "network-information-technology": [
                (1402, 200, 35), (1403, 205, 40), (1404, 210, 45),
            ],
            "software-engineering": [
                (1402, 225, 50), (1403, 230, 55), (1404, 235, 60),
            ],
        }

        count = 0
        for dept in depts:
            if dept.slug in cutoff_data:
                for year, score, cap in cutoff_data[dept.slug]:
                    db.add(KankorCutoff(
                        id=uuid.uuid4(),
                        department_id=dept.id,
                        year=year,
                        min_score=score,
                        capacity=cap,
                    ))
                    count += 1
        await db.commit()
        print(f"Cutoffs: {count} records added")

        # --- Kankor Guides ---
        guides = [
            KankorGuide(
                id=uuid.uuid4(),
                title_fa="راهنمای عمومی کانکور ۱۴۰۵",
                body_fa="کانکور امتحان ورودی پوهنتون‌های دولتی افغانستان است. هر سال صدها هزار شاگرد در این امتحان شرکت می‌کنند. نمره کانکور از ۳۵۰ محاسبه می‌شود.",
                category="عمومی",
                sort_order=1,
            ),
            KankorGuide(
                id=uuid.uuid4(),
                title_fa="نحوه انتخاب رشته",
                body_fa="بعد از اعلام نتایج، شاگردان بر اساس نمره و علاقه‌مندی خود رشته‌ها را انتخاب می‌کنند. توصیه می‌شود هم علاقه و هم بازار کار را در نظر بگیرید.",
                category="انتخاب رشته",
                sort_order=2,
            ),
        ]
        db.add_all(guides)
        await db.commit()
        print(f"Guides: {len(guides)} added")

        # --- Quiz Questions (10 sample) ---
        questions_data = [
            {
                "question_fa": "كداميك از فعاليت‌ها براي شما جذاب‌تر است؟",
                "category": "علایق",
                "options": [
                    ("حل مسائل رياضي و منطقي", {"logic": 3, "biology": 0, "language": 0, "art": 0, "social": 0, "handson": 1}),
                    ("مطالعه متون ادبي و نوشتن", {"logic": 0, "biology": 0, "language": 3, "art": 1, "social": 1, "handson": 0}),
                    ("آزمايش در لابراتوار", {"logic": 1, "biology": 2, "language": 0, "art": 0, "social": 0, "handson": 3}),
                    ("کار با کامپیوتر و برنامه‌نویسي", {"logic": 2, "biology": 0, "language": 0, "art": 1, "social": 0, "handson": 2}),
                ],
            },
            {
                "question_fa": "در وقت فراغت ترجيح مي‌دهيد چه کار کنيد؟",
                "category": "علایق",
                "options": [
                    ("کتاب بخوانم", {"logic": 1, "biology": 0, "language": 3, "art": 0, "social": 0, "handson": 0}),
                    ("ورزش کنم", {"logic": 0, "biology": 1, "language": 0, "art": 0, "social": 2, "handson": 2}),
                    ("نقاشي بکشم", {"logic": 0, "biology": 0, "language": 0, "art": 3, "social": 0, "handson": 1}),
                    ("با دوستانم باشم", {"logic": 0, "biology": 0, "language": 1, "art": 0, "social": 3, "handson": 0}),
                ],
            },
            {
                "question_fa": "كدام درس در مکتب براي شما آسان‌تر بود؟",
                "category": "توانایی",
                "options": [
                    ("رياضيات", {"logic": 3, "biology": 0, "language": 0, "art": 0, "social": 0, "handson": 1}),
                    ("ادبيات", {"logic": 0, "biology": 0, "language": 3, "art": 1, "social": 1, "handson": 0}),
                    ("علوم", {"logic": 1, "biology": 3, "language": 0, "art": 0, "social": 0, "handson": 1}),
                    ("زبان انگليسي", {"logic": 0, "biology": 0, "language": 2, "art": 0, "social": 1, "handson": 0}),
                ],
            },
            {
                "question_fa": "آيا ترجيح مي‌دهيد با انسان‌ها کار کنيد يا با ماشين‌ها؟",
                "category": "شخصیت",
                "options": [
                    ("با انسان‌ها", {"logic": 0, "biology": 0, "language": 1, "art": 0, "social": 3, "handson": 0}),
                    ("با ماشين‌ها و ابزار", {"logic": 1, "biology": 0, "language": 0, "art": 0, "social": 0, "handson": 3}),
                    ("هر دو به يک اندازه", {"logic": 1, "biology": 0, "language": 0, "art": 0, "social": 1, "handson": 1}),
                ],
            },
            {
                "question_fa": "در يک پروژه گروهي، دوست داريد چه نقشي داشته باشيد؟",
                "category": "شخصیت",
                "options": [
                    ("رهبر و ممدير گروه", {"logic": 1, "biology": 0, "language": 0, "art": 0, "social": 3, "handson": 0}),
                    ("طراح و خلاق", {"logic": 1, "biology": 0, "language": 0, "art": 3, "social": 0, "handson": 1}),
                    ("اجراکننده و عملیاتی", {"logic": 0, "biology": 0, "language": 0, "art": 0, "social": 0, "handson": 3}),
                    ("تحقيق و تحليل", {"logic": 3, "biology": 1, "language": 1, "art": 0, "social": 0, "handson": 0}),
                ],
            },
            {
                "question_fa": "كدام موضوع براي شما جالب‌تر است؟",
                "category": "علایق",
                "options": [
                    ("هوش مصنوعي و تکنالوژي", {"logic": 3, "biology": 0, "language": 0, "art": 0, "social": 0, "handson": 1}),
                    ("بيولوژي و طب", {"logic": 1, "biology": 3, "language": 0, "art": 0, "social": 0, "handson": 1}),
                    ("تاريخ و فرهنگ", {"logic": 0, "biology": 0, "language": 3, "art": 1, "social": 2, "handson": 0}),
                    ("معماري و ساختمان‌سازي", {"logic": 1, "biology": 0, "language": 0, "art": 2, "social": 0, "handson": 3}),
                ],
            },
            {
                "question_fa": "آيا از کار فيزيکي لذت مي‌بريد؟",
                "category": "توانایی",
                "options": [
                    ("بله، خيلي", {"logic": 0, "biology": 0, "language": 0, "art": 0, "social": 0, "handson": 3}),
                    ("کمي", {"logic": 0, "biology": 0, "language": 0, "art": 0, "social": 0, "handson": 1}),
                    ("خير، ترجيح مي‌دهم پشت ميز کار کنم", {"logic": 1, "biology": 0, "language": 1, "art": 0, "social": 0, "handson": 0}),
                ],
            },
            {
                "question_fa": "آيا به مطالعه علوم طبي علاقه‌منديد؟",
                "category": "علایق",
                "options": [
                    ("بله، خيلي علاقه دارم", {"logic": 1, "biology": 3, "language": 0, "art": 0, "social": 0, "handson": 1}),
                    ("کمي", {"logic": 0, "biology": 1, "language": 0, "art": 0, "social": 0, "handson": 0}),
                    ("خير", {"logic": 0, "biology": 0, "language": 1, "art": 1, "social": 1, "handson": 0}),
                ],
            },
            {
                "question_fa": "در آينده دوست داريد در کدام بخش کار کنيد؟",
                "category": "شغل",
                "options": [
                    ("بخش خصوصي و شرکت‌ها", {"logic": 1, "biology": 0, "language": 0, "art": 0, "social": 1, "handson": 1}),
                    ("دولت و اداره‌ها", {"logic": 0, "biology": 0, "language": 1, "art": 0, "social": 3, "handson": 0}),
                    ("خودم کار خودم را داشته باشم", {"logic": 1, "biology": 0, "language": 0, "art": 1, "social": 0, "handson": 2}),
                    (" organisation‌هاي بين‌المللي", {"logic": 0, "biology": 1, "language": 2, "art": 0, "social": 2, "handson": 0}),
                ],
            },
            {
                "question_fa": "آيا از نوشتن و گزارش‌نويسي لذت مي‌بريد؟",
                "category": "توانایی",
                "options": [
                    ("بله، خيلي", {"logic": 0, "biology": 0, "language": 3, "art": 0, "social": 1, "handson": 0}),
                    ("کمي", {"logic": 0, "biology": 0, "language": 1, "art": 0, "social": 0, "handson": 0}),
                    ("خير", {"logic": 1, "biology": 0, "language": 0, "art": 1, "social": 0, "handson": 1}),
                ],
            },
        ]

        q_count = 0
        for q_data in questions_data:
            q = QuizQuestion(
                id=uuid.uuid4(),
                question_fa=q_data["question_fa"],
                category=q_data["category"],
                sort_order=q_count,
            )
            db.add(q)
            await db.flush()
            for opt_text, weights in q_data["options"]:
                db.add(QuizOption(
                    id=uuid.uuid4(),
                    question_id=q.id,
                    text_fa=opt_text,
                    trait_weights=weights,
                ))
            q_count += 1
        await db.commit()
        print(f"Quiz: {q_count} questions added")

        # --- Department Trait Profiles (only degree depts) ---
        profiles = {
            "database-information-systems": {"logic": 3, "biology": 0, "language": 1, "art": 0, "social": 1, "handson": 1},
            "network-information-technology": {"logic": 3, "biology": 0, "language": 0, "art": 0, "social": 0, "handson": 3},
            "software-engineering": {"logic": 3, "biology": 0, "language": 0, "art": 2, "social": 0, "handson": 2},
        }

        p_count = 0
        for dept in depts:
            if dept.slug in profiles:
                db.add(DepartmentTraitProfile(
                    id=uuid.uuid4(),
                    department_id=dept.id,
                    trait_weights=profiles[dept.slug],
                ))
                p_count += 1
        await db.commit()
        print(f"Trait profiles: {p_count} added")


if __name__ == "__main__":
    asyncio.run(seed())
