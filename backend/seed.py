"""
Seed script — 16 faculties with basic profiles + CS full profile.
Run: python seed.py
"""

import asyncio
import uuid

from app.database import SessionLocal, engine, Base
from app.modules.universities.models import University
from app.modules.faculties.models import Faculty
from app.modules.departments.models import Department, StudentProject, AlumniStory, CareerRoadmap
from app.modules.kankor.models import KankorCutoff, KankorGuide


async def seed():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with SessionLocal() as db:
        # --- University ---
        uni = University(
            id=uuid.uuid4(),
            slug="herat-university",
            name_fa="پوهنتون هرات",
            name_en="University of Herat",
            name_ps="د هرات پوهنتون",
            description_fa="پوهنتون هرات یکی از قدیمی‌ترین و بزرگ‌ترین دانشگاه‌های افغانستان است که در سال ۱۳۶۷ تأسیس شده و در شهر تاریخی هرات واقع است.",
            description_en="University of Herat is one of the oldest and largest universities in Afghanistan, established in 1988 in the historic city of Herat.",
            description_ps="د هرات پوهنتون د افغانستان یو له زړه پوهه او لوی پوهنتونونه دي چې په ۱۳۶۷ کې تأسیس شوی دی.",
            history_fa="پوهنتون هرات در سال ۱۳۶۷ (۱۹۸۸ میلادی) تأسیس شد و اکنون با بیش از ۱۶ پوهنځی و ۷۰ دیپارتمنت و هزاران محصل، یکی از مراکز مهم تحصیلی افغانستان است.",
            chancellor_name="پروفیسور محمدرحیم فیروزکوهی",
            established_year=1367,
            stats={"faculties": 16, "departments": 70, "students": 25000, "professors": 400},
            lat=34.3529,
            lng=62.2040,
            is_active=True,
        )
        db.add(uni)
        await db.commit()

        # --- 16 Faculties ---
        faculties_data = [
            {"slug": "medicine", "name_fa": "طب", "name_en": "Medicine", "sort_order": 1,
             "description_fa": "پوهنځی طب پوهنتون هرات یکی از قدیمی‌ترین و معتبرترین پوهنځی‌ها است که داکتران متخصص را برای خدمت در بخش صحی تربیت می‌کند.",
             "established_year": 1367},
            {"slug": "dentistry", "name_fa": "ستوماتولوژی", "name_en": "Dentistry", "sort_order": 2,
             "description_fa": "پوهنځی طب دندان (ستوماتولوژی) متخصصان بهداشت دهان و دندان را تربیت می‌کند.",
             "established_year": 1370},
            {"slug": "engineering", "name_fa": "انجنیری", "name_en": "Engineering", "sort_order": 3,
             "description_fa": "پوهنځی انجنیری با رشته‌های انجنیری ساختمانی، آب و برق، و معدن، متخصصان فنی را برای بازسازی افغانستان تربیت می‌کند.",
             "established_year": 1368},
            {"slug": "computer-science", "name_fa": "کمپیوتر ساینس", "name_en": "Computer Science", "sort_order": 4,
             "description_fa": "پوهنځی کمپیوتر ساینس در سال ۱۳۸۴ تأسیس شد و یکی از پوهنځی‌های پرجمعیت و محبوب دانشگاه است.",
             "established_year": 1384, "dean_name": "پروفیتور احمد شاه فیروزی"},
            {"slug": "economics", "name_fa": "اقتصاد", "name_en": "Economics", "sort_order": 5,
             "description_fa": "پوهنځی اقتصاد متخصصان مالی و اقتصادی را برای بخش‌های دولتی و خصوصی تربیت می‌کند.",
             "established_year": 1369},
            {"slug": "law", "name_fa": "حقوق و علوم سیاسی", "name_en": "Law & Political Science", "sort_order": 6,
             "description_fa": "پوهنځی حقوق و علوم سیاسی وکلا و تحلیلگران سیاسی را برای نظام قضایی و سیاسی کشور تربیت می‌کند.",
             "established_year": 1368},
            {"slug": "education", "name_fa": "تعلیم و تربیه", "name_en": "Education", "sort_order": 7,
             "description_fa": "پوهنځی تعلیم و تربیه آموزگاران و مدیران مکتب را برای نظام تعلیمی کشور تربیت می‌کند.",
             "established_year": 1367},
            {"slug": "science", "name_fa": "ساینس", "name_en": "Science", "sort_order": 8,
             "description_fa": "پوهنځی ساینس شامل رشته‌های ریاضی، فیزیک، کیمیا و بیولوژی است.",
             "established_year": 1368},
            {"slug": "agriculture", "name_fa": "زراعت", "name_en": "Agriculture", "sort_order": 9,
             "description_fa": "پوهنځی زراعت متخصصان کشاورزی و محیط زیست را برای بخش زراعت کشور تربیت می‌کند.",
             "established_year": 1369},
            {"slug": "veterinary", "name_fa": "علوم وترنری", "name_en": "Veterinary Science", "sort_order": 10,
             "description_fa": "پوهنځی علوم وترنری متخصصان حیوانات و صحت دامی را تربیت می‌کند.",
             "established_year": 1375},
            {"slug": "literature", "name_fa": "ادبیات و علوم بشری", "name_en": "Literature & Humanities", "sort_order": 11,
             "description_fa": "پوهنځی ادبیات و علوم بشری شامل رشته‌های ادبیات فارسی، انگلیسی، تاریخ و جغرافیا است.",
             "established_year": 1367},
            {"slug": "journalism", "name_fa": "ژورنالیزم", "name_en": "Journalism", "sort_order": 12,
             "description_fa": "پوهنځی ژورنالیزم روزنامه‌نگاران و خبرنگاران حرفه‌ای را تربیت می‌کند.",
             "established_year": 1372},
            {"slug": "sharia", "name_fa": "شرعیات", "name_en": "Sharia", "sort_order": 13,
             "description_fa": "پوهنځی شرعیات متخصصان فقه و مطالعات اسلامی را تربیت می‌کند.",
             "established_year": 1368},
            {"slug": "arts", "name_fa": "هنرها", "name_en": "Fine Arts", "sort_order": 14,
             "description_fa": "پوهنځی هنرها شامل رشته‌های نقاشی، معماری و هنرهای زیبا است.",
             "established_year": 1370},
            {"slug": "social-sciences", "name_fa": "علوم اجتماعی", "name_en": "Social Sciences", "sort_order": 15,
             "description_fa": "پوهنځی علوم اجتماعی شامل رشته‌های جامعه‌شناسی، روانشناسی و علوم سیاسی است.",
             "established_year": 1371},
            {"slug": "public-admin", "name_fa": "اداره و پالیسی عامه", "name_en": "Public Administration", "sort_order": 16,
             "description_fa": "پوهنځی اداره و پالیسی عامه مدیران دولتی و تحلیلگران پالیسی را تربیت می‌کند.",
             "established_year": 1373},
        ]

        faculties = {}
        for fd in faculties_data:
            f = Faculty(id=uuid.uuid4(), university_id=uni.id, **fd)
            db.add(f)
            faculties[fd["slug"]] = f
        await db.commit()

        # --- CS Faculty: 3 degree departments + 1 service department ---
        cs_faculty = faculties["computer-science"]

        # 1. Database & Information Systems (degree)
        db_dept = Department(
            id=uuid.uuid4(),
            faculty_id=cs_faculty.id,
            slug="database-information-systems",
            name_fa="دیتابیس و سیستم‌های معلوماتی",
            name_en="Database & Information Systems",
            name_ps="د ډیټابیس او معلوماتي سیستمونه",
            description_fa="رشته دیتابیس و سیستم‌های معلوماتی بر طراحی، مدیریت و بهینه‌سازی پایگاه‌های داده تمرکز دارد. دانشجویان یاد می‌گیرند چگونه داده‌های بزرگ را ذخیره، بازیابی و تحلیل کنند.",
            description_en="Database & Information Systems focuses on designing, managing, and optimizing databases for large-scale data storage and retrieval.",
            department_type="degree",
            vision_fa="رهبری در تربیت متخصصان دیتابیس که بتوانند سیستم‌های معلوماتی مؤثر برای افغانستان بسازند.",
            mission_fa="آموزش عملی و نظری طراحی دیتابیس، مدیریت داده‌ها، و تحلیل اطلاعات با استفاده از تکنالوژی‌های روز.",
            duration_years=4,
            subjects=["SQL و پایگاه داده", "مدیریت دیتابیس", "سیستم‌های اطلاعاتی", "داده‌کاوی", "امنیت داده‌ها"],
            career_paths=[
                {"title": "Database Administrator", "desc": "مدیریت و نگهداری پایگاه‌های داده"},
                {"title": "Data Analyst", "desc": "تحلیل داده‌ها و تهیه گزارش"},
                {"title": "Data Engineer", "desc": "طراحی خطوط لوله داده"},
            ],
            required_skills=["تفکر منطقی", "دقت در جزئیات", "آشنایی با SQL"],
            suitable_for=["علاقه‌مندان به سازماندهی داده‌ها", "افراد دقیق و منظم"],
        )

        # 2. Network & IT (degree)
        net_dept = Department(
            id=uuid.uuid4(),
            faculty_id=cs_faculty.id,
            slug="network-information-technology",
            name_fa="نتورک و تکنالوژی معلوماتی",
            name_en="Network & Information Technology",
            name_ps="د نیټورک او معلوماتي تکنالوژي",
            description_fa="رشته نتورک و تکنالوژی معلوماتی بر طراحی، پیاده‌سازی و مدیریت شبکه‌های کامپیوتری تمرکز دارد.",
            description_en="Network & IT focuses on designing, implementing, and managing computer networks and IT infrastructure.",
            department_type="degree",
            vision_fa="تربیت متخصصان شبکه که بتوانند زیرساخت‌های معلوماتی افغانستان را تقویت کنند.",
            mission_fa="آموزش طراحی شبکه، امنیت سایبری، و مدیریت زیرساخت‌های IT.",
            duration_years=4,
            subjects=["شبکه‌های کامپیوتری", "امنیت سایبری", "سیستم‌عامل", "مدیریت شبکه", "اینترنت اشیا"],
            career_paths=[
                {"title": "Network Engineer", "desc": "طراحی و مدیریت شبکه"},
                {"title": "System Administrator", "desc": "مدیریت سرورها و سیستم‌ها"},
                {"title": "Cybersecurity Analyst", "desc": "امنیت سایبری و محافظت از داده‌ها"},
            ],
            required_skills=["تفکر تحلیلی", "حل مسئله", "آشنایی با مفاهیم شبکه"],
            suitable_for=["علاقه‌مندان به شبکه و امنیت", "افراد کنجکاو و فنی"],
        )

        # 3. Software Engineering (degree)
        sw_dept = Department(
            id=uuid.uuid4(),
            faculty_id=cs_faculty.id,
            slug="software-engineering",
            name_fa="انجنیری نرم‌افزار",
            name_en="Software Engineering",
            name_ps="د سافټویر انجنیري",
            description_fa="رشته انجنیری نرم‌افزار بر طراحی، توسعه و آزمایش نرم‌افزارهای با کیفیت تمرکز دارد.",
            description_en="Software Engineering focuses on designing, developing, and testing high-quality software systems.",
            department_type="degree",
            vision_fa="تربیت انجنیران نرم‌افزار که بتوانند راه‌حل‌های دیجیتالی مؤثر برای چالش‌های افغانستان بسازند.",
            mission_fa="آموزش مهندسی نرم‌افزار، برنامه‌نویسی، و توسعه اپلیکیشن‌های وب و موبایل.",
            duration_years=4,
            subjects=["برنامه‌نویسی (Python, Java, C++)", "مهندسی نرم‌افزار", "توسعه وب", "توسعه موبایل", "تست نرم‌افزار"],
            career_paths=[
                {"title": "Backend Developer", "desc": "توسعه سرور و API"},
                {"title": "Frontend Developer", "desc": "توسعه رابط کاربری وب"},
                {"title": "Mobile Developer", "desc": "توسعه اپلیکیشن موبایل"},
            ],
            required_skills=["خلاقیت", "برنامه‌نویسی", "کار تیمی", "یادگیری مداوم"],
            suitable_for=["علاقه‌مندان به برنامه‌نویسی", "افراد خلاق و نوآور"],
        )

        # 4. Computer Education (SERVICE — not selectable in Kankor)
        edu_dept = Department(
            id=uuid.uuid4(),
            faculty_id=cs_faculty.id,
            slug="computer-education",
            name_fa="آموزش کامپیوتر",
            name_en="Computer Education",
            name_ps="د کمپیټر زده‌کړه",
            description_fa="دیپارتمنت آموزش کامپیوتر خدمات آموزشی کامپیوتر را به پوهنځی‌های دیگر ارائه می‌دهد. این دیپارتمنت در کانکور انتخاب نمی‌شود.",
            description_en="Computer Education provides computer training services to other faculties. This department is not selectable in Kankor.",
            department_type="service",
            vision_fa="ارائه آموزش کامپیوتر با کیفیت به تمام پوهنځی‌های پوهنتون.",
            mission_fa="آموزش مهارت‌های پایه و پیشرفته کامپیوتر به محصلان رشته‌های غیرکامپیوتری.",
            duration_years=4,
            subjects=["آموزش کامپیوتر پایه", "پردازش متن", "اینترنت"],
            career_paths=[],
            required_skills=["صبر", "توانایی آموزش"],
            suitable_for=["علاقه‌مندان به تدریس"],
        )

        db.add_all([db_dept, net_dept, sw_dept, edu_dept])
        await db.commit()

        # --- Full profile data for CS departments ---
        # Student projects for DB dept
        db.add(StudentProject(
            department_id=db_dept.id,
            title_fa="اپلیکیشن مدیریت کتابخانه دانشگاه",
            description_fa="سیستم مدیریت کتابخانه با قابلیت جستجوی کتاب، امانت‌گیری آنلاین و گزارش‌گیری خودکار.",
            students="علی احمدی، فاطمه حسینی",
            year=1403,
        ))

        # Alumni for SW dept
        db.add(AlumniStory(
            department_id=sw_dept.id,
            full_name="احمد شاه فیروزی",
            graduation_year=1392,
            current_position="مدیر فنی شرکت افغان تلکام",
            story_fa="بعد از فراغت از پوهنځی کمپیوتر ساینس، اول در یک شرکت کوچک نرم‌افزاری کار کردم. با تلاش مداوم و یادگیری تکنالوژی‌های جدید، اکنون مدیر فنی یکی از بزرگ‌ترین شرکت‌های مخابراتی افغانستان هستم.",
        ))

        # Career Roadmap for SW dept
        db.add(CareerRoadmap(
            department_id=sw_dept.id,
            career_title_fa="توسعه‌دهنده Backend",
            steps=[
                {"title": "Python", "desc": "یادگیری مبانی برنامه‌نویسی پایتون", "resources": [{"name": "Python Tutorial", "url": "https://python.org/tutorial"}]},
                {"title": "Git و GitHub", "desc": "کنترل نسخه و همکاری تیمی", "resources": []},
                {"title": "SQL و پایگاه داده", "desc": "طراحی و مدیریت پایگاه داده", "resources": []},
                {"title": "FastAPI / Django", "desc": "فریم‌ورک وب پایتون", "resources": []},
                {"title": "Docker", "desc": "کانتینرسازی و استقرار", "resources": []},
                {"title": "پروژه واقعی", "desc": "ساخت یک پروژه کامل", "resources": []},
            ],
        ))

        await db.commit()

        # --- Summary ---
        print("Seed complete!")
        print(f"  University: {uni.name_fa}")
        print(f"  Faculties: {len(faculties_data)}")
        print(f"  CS departments: 3 degree + 1 service")
        for d in [db_dept, net_dept, sw_dept, edu_dept]:
            print(f"    - {d.name_fa} ({d.department_type})")


if __name__ == "__main__":
    asyncio.run(seed())
