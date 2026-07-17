"""
Seed ALL 70 departments for ALL 16 faculties of Herat University.
Run: python seed_all_departments.py
"""

import asyncio
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import SessionLocal
from app.modules.universities.models import University
from app.modules.faculties.models import Faculty
from app.modules.departments.models import Department
from app.modules.kankor.models import KankorCutoff


# Faculty slug → list of (slug, name_fa, name_en, type, duration, description)
DEPARTMENTS = {
    "computer-science": [
        ("database-info-systems", "دیتابیس و سیستم‌های معلوماتی", "Database & Information Systems", "degree", 4,
         "طراحی، مدیریت و بهینه‌سازی پایگاه‌های داده برای ذخیره و بازیابی داده‌های بزرگ."),
        ("network-it", "نتورک و تکنالوژی معلوماتی", "Network & IT", "degree", 4,
         "طراحی، پیاده‌سازی و مدیریت شبکه‌های کامپیوتری و زیرساخت‌های IT."),
        ("software-engineering", "انجنیری نرم‌افزار", "Software Engineering", "degree", 4,
         "طراحی، توسعه و آزمایش نرم‌افزارهای با کیفیت."),
        ("computer-education", "آموزش کامپیوتر", "Computer Education", "service", 4,
         "خدمات آموزشی کامپیوتر به پوهنځی‌های دیگر."),
    ],
    "medicine": [
        ("medicine-program", "طب معالجوی — برنامه واحد", "Medicine — Unified Program", "degree", 7,
         "برنامه کامل طب معالجوی شامل علوم پایه و کلینیکی."),
        ("basic-sciences", "علوم پایه طب — اناتومی، فزیولوژی، بیوشیمی", "Basic Medical Sciences", "degree", 3,
         "آموزش علوم پایه طب شامل اناتومی، فزیولوژی و بیوشیمی."),
        ("paraclinical", "پاراکلینیک — پتالوژی، فارمکولوژی، میکروبیولوژی", "Paraclinical Sciences", "degree", 3,
         "آموزش علوم پاراکلینیکی شامل پتالوژی و فارمکولوژی."),
        ("internal-medicine", "داخله", "Internal Medicine", "degree", 7,
         "تشخیص و درمان بیماری‌های داخلی."),
        ("surgery", "جراحی", "Surgery", "degree", 7,
         "آموزش عملی جراحی‌های عمومی و تخصصی."),
        ("gynecology", "نسایی و ولادی", "Obstetrics & Gynecology", "degree", 7,
         "مراقبت از سلامت زنان و زایمان."),
        ("pediatrics", "اطفال", "Pediatrics", "degree", 7,
         "مراقبت از سلامت اطفال."),
        ("public-health", "صحت عامه", "Public Health", "degree", 5,
         "آموزش بهداشت عمومی و پیشگیری از بیماری‌ها."),
    ],
    "dentistry": [
        ("dentistry-program", "ستوماتولوژی — برنامه واحد", "Dentistry — Unified Program", "degree", 5,
         "برنامه کامل طب دندان."),
        ("basic-dental-sciences", "علوم پایه ستوماتولوژی", "Basic Dental Sciences", "degree", 3,
         "علوم پایه طب دندان."),
        ("dental-clinics", "کلینیک‌های تخصصی دندان", "Dental Specialty Clinics", "degree", 5,
         "کلینیک‌های عملی تخصصی دندان."),
    ],
    "engineering": [
        ("civil-engineering", "انجنیری سیول", "Civil Engineering", "degree", 4,
         "طراحی و ساخت ساختمان‌ها، پل‌ها و زیرساخت‌ها."),
        ("architecture", "آرشیتکچر / معماری", "Architecture", "degree", 5,
         "طراحی معماری ساختمان‌ها و فضاهای شهری."),
        ("electrical-engineering", "برق و الکترونیک", "Electrical Engineering", "degree", 4,
         "طراحی سیستم‌های برقی و الکترونیکی."),
        ("mechanical-engineering", "میخانیک", "Mechanical Engineering", "degree", 4,
         "طراحی و ساخت ماشین‌آلات و سیستم‌های مکانیکی."),
    ],
    "economics": [
        ("national-economics", "اقتصاد ملی", "National Economics", "degree", 4,
         "مطالعه سیستم‌های اقتصادی و سیاست‌های مالی."),
        ("management-bba", "منجمنت و ادارۀ تشبثات (BBA)", "Management & Business Administration", "degree", 4,
         "مدیریت کسب‌وکار و سازمان‌ها."),
        ("finance-banking", "امور مالی و بانکی", "Finance & Banking", "degree", 4,
         "مدیریت مالی، بانکداری و سرمایه‌گذاری."),
        ("statistics-econometrics", "احصائیه و اکونومتری", "Statistics & Econometrics", "degree", 4,
         "تحلیل آماری و مدل‌سازی اقتصادی."),
    ],
    "law": [
        ("judicial-prosecution", "قضایی و څارنوالی", "Judicial & Prosecution", "degree", 4,
         "حقوق جزایی، قضایی و څارنوالی."),
        ("administrative-diplomacy", "اداری و دیپلوماسی", "Administrative & Diplomatic", "degree", 4,
         "حقوق اداری، بین‌المللی و دیپلوماسی."),
    ],
    "education": [
        ("math-education", "ریاضی", "Mathematics Education", "degree", 4,
         "تدریس ریاضیات در مکاتب."),
        ("physics-education", "فزیک", "Physics Education", "degree", 4,
         "تدریس فزیک در مکاتب."),
        ("chemistry-education", "کیمیا", "Chemistry Education", "degree", 4,
         "تدریس کیمیا در مکاتب."),
        ("biology-education", "بیولوژی", "Biology Education", "degree", 4,
         "تدریس بیولوژی در مکاتب."),
        ("dari-literature-education", "زبان و ادبیات دری", "Dari Literature Education", "degree", 4,
         "تدریس زبان و ادبیات دری."),
        ("pashto-literature-education", "زبان و ادبیات پشتو", "Pashto Literature Education", "degree", 4,
         "تدریس زبان و ادبیات پشتو."),
        ("english-literature-education", "زبان و ادبیات انگلیسی", "English Literature Education", "degree", 4,
         "تدریس زبان و ادبیات انگلیسی."),
        ("history-education", "تاریخ", "History Education", "degree", 4,
         "تدریس تاریخ در مکاتب."),
        ("geography-education", "جغرافیه", "Geography Education", "degree", 4,
         "تدریس جغرافیه در مکاتب."),
        ("islamic-studies", "علوم و فرهنگ اسلامی", "Islamic Studies", "degree", 4,
         "تدریس علوم و فرهنگ اسلامی."),
        ("psychology-education", "روانشناسی و علوم تربیتی", "Psychology & Educational Sciences", "degree", 4,
         "روانشناسی تربیتی و علوم آموزشی."),
        ("computer-education-edu", "کمپیوتر ساینس آموزشی", "Computer Science Education", "degree", 4,
         "تدریس کامپیوتر در مکاتب."),
    ],
    "science": [
        ("math", "ریاضی", "Mathematics", "degree", 4,
         "مطالعه ریاضیات محض و کاربردی."),
        ("physics", "فزیک", "Physics", "degree", 4,
         "مطالعه قوانین فیزیک و کیهان."),
        ("chemistry", "کیمیا", "Chemistry", "degree", 4,
         "مطالعه ترکیبات شیمیایی و واکنش‌ها."),
        ("biology", "بیولوژی", "Biology", "degree", 4,
         "مطالعه موجودات زنده و فرآیندهای حیاتی."),
        ("geology", "جیولوجی", "Geology", "degree", 4,
         "مطالعه ساختمان و تاریخ زمین."),
    ],
    "agriculture": [
        ("agronomy", "اگرانومی — علوم نباتی", "Agronomy — Plant Sciences", "degree", 4,
         "کشاورزی و علوم نباتات."),
        ("horticulture", "هارتیکلچر — باغداری", "Horticulture", "degree", 4,
         "باغداری و پرورش میوه و سبزیجات."),
        ("plant-protection", "حفاظۀ نباتات", "Plant Protection", "degree", 4,
         "محافظت نباتات از آفات و بیماری‌ها."),
        ("animal-sciences", "علوم حیوانی", "Animal Sciences", "degree", 4,
         "علوم دامی و پرورش حیوانات."),
        ("agri-economics", "اقتصاد و توسعۀ زراعتی", "Agricultural Economics", "degree", 4,
         "اقتصاد کشاورزی و توسعه روستایی."),
        ("forestry", "جنگلات و منابع طبیعی", "Forestry & Natural Resources", "degree", 4,
         "مدیریت جنگلات و منابع طبیعی."),
        ("soil-irrigation", "خاک‌شناسی و آبیاری", "Soil Science & Irrigation", "degree", 4,
         "مطالعه خاک و سیستم‌های آبیاری."),
        ("food-technology", "تکنالوژی مواد غذایی", "Food Technology", "degree", 4,
         "تکنالوژی فرآوری و نگهداری مواد غذایی."),
    ],
    "veterinary": [
        ("vet-program", "علوم وترنری — برنامه واحد", "Veterinary Science — Unified Program", "degree", 5,
         "برنامه کامل علوم وترنری."),
        ("preclinical-vet", "پری‌کلینیک وترنری", "Preclinical Veterinary", "degree", 3,
         "علوم پایه وترنری."),
        ("clinical-vet", "کلینیک وترنری", "Clinical Veterinary", "degree", 5,
         "درمان و مراقبت از حیوانات."),
    ],
    "literature": [
        ("dari-literature", "زبان و ادبیات دری", "Dari Language & Literature", "degree", 4,
         "مطالعه زبان و ادبیات کلاسیک و معاصر دری."),
        ("pashto-literature", "زبان و ادبیات پشتو", "Pashto Language & Literature", "degree", 4,
         "مطالعه زبان و ادبیات پشتو."),
        ("english-literature", "زبان و ادبیات انگلیسی", "English Language & Literature", "degree", 4,
         "مطالعه زبان و ادبیات انگلیسی."),
        ("arabic-literature", "زبان و ادبیات عربی", "Arabic Language & Literature", "degree", 4,
         "مطالعه زبان و ادبیات عربی."),
        ("german-literature", "زبان و ادبیات آلمانی", "German Language & Literature", "degree", 4,
         "مطالعه زبان و ادبیات آلمانی."),
    ],
    "journalism": [
        ("journalism", "ژورنالیزم", "Journalism", "degree", 4,
         "آموزش روزنامه‌نگاری و خبرنگاری."),
        ("public-relations", "ارتباطات عامه", "Public Relations", "degree", 4,
         "مدیریت ارتباطات و رسانه‌ها."),
    ],
    "sharia": [
        ("fiqh-law", "فقه و قانون", "Fiqh & Law", "degree", 4,
         "مطالعه فقه اسلامی و حقوق شرعی."),
        ("islamic-education", "تعلیمات اسلامی", "Islamic Education", "degree", 4,
         "آموزش علوم و معارف اسلامی."),
        ("islamic-culture", "ثقافت اسلامی", "Islamic Culture", "degree", 4,
         "فرهنگ و تمدن اسلامی."),
    ],
    "arts": [
        ("painting", "نقاشی و رسامی", "Painting & Drawing", "degree", 4,
         "هنرهای تجسمی و نقاشی."),
        ("graphic-design", "گرافیک دیزاین", "Graphic Design", "degree", 4,
         "طراحی گرافیک و بصری."),
        ("calligraphy-minature", "خطاطی و مینیاتوری", "Calligraphy & Miniature", "degree", 4,
         "هنر خوشنویسی و مینیاتور ایرانی."),
        ("music-performing-arts", "موسیقی و هنرهای نمایشی", "Music & Performing Arts", "degree", 4,
         "موسیقی و هنرهای نمایشی."),
    ],
    "social-sciences": [
        ("sociology", "جامعه‌شناسی", "Sociology", "degree", 4,
         "مطالعه جامعه و روابط اجتماعی."),
        ("philosophy", "فلسفه", "Philosophy", "degree", 4,
         "مطالعه تفکر فلسفی و منطق."),
        ("history", "تاریخ", "History", "degree", 4,
         "مطالعه تاریخ افغانستان و جهان."),
        ("archaeology", "باستان‌شناسی", "Archaeology", "degree", 4,
         "مطالعه آثار باستانی و تاریخی."),
    ],
    "public-admin": [
        ("public-administration", "ادارۀ عامه", "Public Administration", "degree", 4,
         "مدیریت اداری و سازمان‌های دولتی."),
        ("public-policy", "پالیسی عامه", "Public Policy", "degree", 4,
         "تدوین و ارزیابی سیاست‌های عامه."),
    ],
}


async def seed():
    async with SessionLocal() as db:
        # Get university
        uni = (await db.execute(select(University))).scalars().first()
        if not uni:
            print("No university found. Run seed.py first!")
            return

        # Get all faculties
        faculties_result = await db.execute(select(Faculty))
        faculties = {f.slug: f for f in faculties_result.scalars()}

        total = 0
        for fac_slug, depts in DEPARTMENTS.items():
            if fac_slug not in faculties:
                print(f"⚠️  Faculty '{fac_slug}' not found, skipping")
                continue

            fac = faculties[fac_slug]
            for dept_slug, name_fa, name_en, dept_type, duration, desc in depts:
                # Check if already exists
                existing = (await db.execute(
                    select(Department).where(Department.slug == dept_slug)
                )).scalars().first()

                if existing:
                    continue

                db.add(Department(
                    id=uuid.uuid4(),
                    faculty_id=fac.id,
                    slug=dept_slug,
                    name_fa=name_fa,
                    name_en=name_en,
                    description_fa=desc,
                    department_type=dept_type,
                    duration_years=duration,
                    degree_type="لیسانس" if duration <= 4 else "لیسانس",
                ))
                total += 1

            await db.commit()
            print(f"  {fac_slug}: {len(depts)} departments")

        print(f"\n✅ Total new departments added: {total}")

        # Count total
        all_depts = (await db.execute(select(Department))).scalars()
        print(f"📊 Total departments in database: {len(list(all_depts))}")


if __name__ == "__main__":
    asyncio.run(seed())
