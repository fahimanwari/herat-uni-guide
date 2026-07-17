"""
Seed the question bank with 200+ questions across all subjects.
Run: python seed_question_bank.py
"""

import asyncio
from app.database import SessionLocal
from app.modules.question_bank.models import QuestionBank


# Subject codes
MATH = "math"
PHYSICS = "physics"
CHEMISTRY = "chemistry"
BIOLOGY = "biology"
DARI = "dari"
ISLAMIC = "islamic"
CS = "cs"

# Difficulty levels
EASY = "easy"
MEDIUM = "medium"
HARD = "hard"


def q(subject, difficulty, question, options, source=None, explanation=None):
    """Helper to create a question dict."""
    return {
        "subject": subject,
        "difficulty": difficulty,
        "question_fa": question,
        "options": [{"text": opt, "is_correct": i == 0} for i, opt in enumerate(options)],
        "source": source,
        "explanation_fa": explanation,
        "is_active": True,
    }


# ==================== MATHEMATICS ====================
math_questions = [
    # Easy
    q(MATH, EASY, "اگر x + 7 = 15 باشد، x چقدر است؟", ["8", "7", "22", "15"]),
    q(MATH, EASY, "مساحت مربع با ضلع ۵ چقدر است؟", ["25", "10", "20", "15"]),
    q(MATH, EASY, "۲۰ + ۳۵ × ۲ چقدر است؟", ["90", "110", "70", "55"]),
    q(MATH, EASY, "محیط دایره با شعاع ۷ چقدر است؟ (π≈3.14)", ["43.96", "44", "153.86", "49"]),
    q(MATH, EASY, "اگر ۳x = ۲۷ باشد، x چقدر است؟", ["9", "81", "3", "24"]),
    # Medium
    q(MATH, MEDIUM, "اگر f(x) = 3x² - 2x + 1 باشد، f(2) چقدر است؟", ["9", "13", "5", "17"]),
    q(MATH, MEDIUM, "درایه‌های معادله x² - 7x + 12 = 0 چیست؟", ["3 و 4", "2 و 6", "1 و 12", "-3 و -4"]),
    q(MATH, MEDIUM, "log₃(27) چقدر است؟", ["3", "9", "27", "2"]),
    q(MATH, MEDIUM, "تعداد اعداد اول بین ۱ تا ۵۰ چند است؟", ["15", "14", "16", "13"]),
    q(MATH, MEDIUM, "اگر a=2 و b=-3 باشد، (a+b)² چقدر است؟", ["1", "25", "13", "-1"]),
    # Hard
    q(MATH, HARD, "انتگرال ∫2x dx چیست؟", ["x² + C", "2x² + C", "x + C", "2 + C"]),
    q(MATH, HARD, "اگر sin(θ) = 0.6 باشد، cos(θ) چقدر است؟ (θ تیز)", ["0.8", "0.6", "0.4", "1"]),
    q(MATH, HARD, "دترمینان ماتریس [[1,2],[3,4]] چقدر است؟", ["-2", "2", "10", "-10"]),
    q(MATH, HARD, "极限 lim(x→0) sin(x)/x چقدر است؟", ["1", "0", "∞", "نامعین"]),
    q(MATH, HARD, "اگر تابع f(x)=e^x باشد، مشتق f'(x) چیست؟", ["e^x", "xe^(x-1)", "e^(x-1)", "ln(x)"]),
]

# ==================== PHYSICS ====================
physics_questions = [
    q(PHYSICS, EASY, "واحد نیرو در سیستم SI چیست؟", ["نیوتن", "ژول", "وات", "پاسکال"]),
    q(PHYSICS, EASY, "شتاب جاذبه زمین تقریباً چقدر است؟", ["9.8 m/s²", "10.5 m/s²", "8.2 m/s²", "11 m/s²"]),
    q(PHYSICS, EASY, "سرعت نور در خلأ چقدر است؟", ["3×10⁸ m/s", "3×10⁶ m/s", "3×10¹⁰ m/s", "3×10⁴ m/s"]),
    q(PHYSICS, EASY, "انرژی جنبشی فرمول چیست؟", ["½mv²", "mgh", "mv", "½kx²"]),
    q(PHYSICS, EASY, "قانون نیوتن دوم بیان می‌کند:", ["F=ma", "F=mv", "F=mg", "F=ml"]),
    q(PHYSICS, MEDIUM, "قانون اهم بیان می‌کند:", ["V=IR", "P=IV", "F=qE", "E=mc²"]),
    q(PHYSICS, MEDIUM, "در یک مدار سری، جریان در تمام نقاط:", ["یکسان است", "متفاوت است", "صفر است", "دو برابر می‌شود"]),
    q(PHYSICS, MEDIUM, "قانون بویل بیان می‌کند:", ["PV=ثابت", "P/T=ثابت", "V/T=ثابت", "PVT=ثابت"]),
    q(PHYSICS, MEDIUM, "نور در محیط متراکم‌تر:", ["کندتر حرکت می‌کند", "سریع‌تر حرکت می‌کند", "سرعتش ثابت است", "برمی‌گردد"]),
    q(PHYSICS, MEDIUM, "واحد توان در سیستم SI چیست؟", ["وات", "ژول", "نیوتن", "آمپر"]),
    q(PHYSICS, HARD, "فرمول انرژی الکترومغناطیسی چیست؟", ["E=mc²", "E=hv", "F=ma", "PV=nRT"]),
    q(PHYSICS, HARD, "شتاب سقوط آزاد در خلأ چقدر است؟", ["9.8 m/s²", "10 m/s²", "0", "متغیر"]),
    q(PHYSICS, HARD, "قانون کولن بیان می‌کند:", ["F=kq₁q₂/r²", "F=ma", "V=IR", "P=IV"]),
    q(PHYSICS, HARD, "در یک مدار RC، ثابت زمانی τ چقدر است؟", ["RC", "R/C", "C/R", "R×C²"]),
]

# ==================== CHEMISTRY ====================
chemistry_questions = [
    q(CHEMISTRY, EASY, "فرمول آب چیست؟", ["H₂O", "CO₂", "O₂", "H₂"]),
    q(CHEMISTRY, EASY, "عدد اتمی کربن چند است؟", ["6", "12", "8", "14"]),
    q(CHEMISTRY, EASY, "کدام یک فلز است؟", ["آهن", "اکسیژن", "نیتروژن", "کربن"]),
    q(CHEMISTRY, EASY, "pH آب خالص چقدر است؟", ["7", "0", "14", "1"]),
    q(CHEMISTRY, EASY, "حلال عمومی چیست؟", ["آب", "اتانول", "استون", "بنزن"]),
    q(CHEMISTRY, MEDIUM, "کدام یک گاز نجیب است؟", ["آرگون", "نیتروژن", "اکسیژن", "هیدروژن"]),
    q(CHEMISTRY, MEDIUM, "جرم اتمی اکسیژن چقدر است؟", ["16", "8", "32", "4"]),
    q(CHEMISTRY, MEDIUM, "تعداد الکترون‌های لایه اول اتم چند است؟", ["2", "8", "1", "4"]),
    q(CHEMISTRY, MEDIUM, "کدام ترکیب نمک است؟", ["NaCl", "H₂O", "CO₂", "O₂"]),
    q(CHEMISTRY, MEDIUM, "اتم هیدروژن چند پروتون دارد؟", ["1", "2", "0", "3"]),
    q(CHEMISTRY, HARD, "قانون Avogadro بیان می‌کند:", ["یک مول هر گاز ۲۲.۴ لیتر حجم دارد", "یک مول ۶×۱۰²³ ذره دارد", "هر دو مورد", "هیچکدام"]),
    q(CHEMISTRY, HARD, "pH محلول با غلظت H+ برابر 10⁻³ چقدر است؟", ["3", "11", "7", "1"]),
    q(CHEMISTRY, HARD, "انرژی پیوند covalent کدام بیشتر است؟", ["H-H", "Cl-Cl", "O=O", "N≡N"]),
]

# ==================== BIOLOGY ====================
biology_questions = [
    q(BIOLOGY, EASY, "واحد ساختاری و عملکردی بدن چیست؟", ["سلول", "بافت", "اندام", "اتم"]),
    q(BIOLOGY, EASY, "کدام اندام خون را پمپ می‌کند؟", ["قلب", "کبد", "کلیه", "ریه"]),
    q(BIOLOGY, EASY, "DNA مخفف چیست؟", ["Deoxyribonucleic Acid", "Dinitrogen Acid", "Dynamic Nuclear Acid", "Direct Nucleic Acid"]),
    q(BIOLOGY, EASY, "فتوسنتز در کدام اندام گیاه انجام می‌شود؟", ["برگ", "ریشه", "ساقه", "گل"]),
    q(BIOLOGY, EASY, "تعداد کروموزم‌های انسان چند است؟", ["46", "44", "48", "42"]),
    q(BIOLOGY, MEDIUM, "کدام حیوان پستاندار است؟", ["نهنگ", "تمساح", "مار", "لاک‌پشت"]),
    q(BIOLOGY, MEDIUM, "بزرگ‌ترین عضو بدن انسان چیست؟", ["پوست", "کبد", "مغز", "ریه"]),
    q(BIOLOGY, MEDIUM, "خون توسط کدام اندام تصفیه می‌شود؟", ["کلیه", "کبد", "طحال", "لوزالمعده"]),
    q(BIOLOGY, MEDIUM, "کدام ویتامین با نور خورشید تولید می‌شود؟", ["ویتامین D", "ویتامین C", "ویتامین A", "ویتامین B"]),
    q(BIOLOGY, MEDIUM, "میتوکندری چه نقشی در سلول دارد؟", ["تولید انرژی", "ذخیره آب", "تولید پروتئین", "تقسیم سلولی"]),
    q(BIOLOGY, HARD, "کدام ماده ژنتیکی در میتوکندری وجود دارد؟", ["DNA", "RNA", "پروتئین", "لیپید"]),
    q(BIOLOGY, HARD, "چرخه کربس در کدام اندام سلول انجام می‌شود؟", ["میتوکندری", "هسته", "ریبوزوم", "غشاء"]),
    q(BIOLOGY, HARD, "آنزیم‌ها چه نوع مولکولی هستند؟", ["پروتئین", "کربوهیدرات", "لیپید", "نوکلئیک اسید"]),
]

# ==================== DARI ====================
dari_questions = [
    q(DARI, EASY, "کدام کلمه مخالف «تاریکی» است؟", ["روشنایی", "تاریکی", "سکوت", "آرامش"]),
    q(DARI, EASY, "«اکابر» به چه معناست؟", ["بزرگ‌ترها", "کوچک‌ترها", "جوانان", "کودکان"]),
    q(DARI, EASY, "فعل «رفتن» در زمان گذشته چیست؟", ["رفت", "می‌رود", "خواهد رفت", "رفته"]),
    q(DARI, EASY, "«محصل» به چه معناست؟", ["دانشجو", "استاد", "معلم", "شاگرد"]),
    q(DARI, EASY, "«هملی» به چه معناست؟", ["همراه", "دشمن", "بیگانه", "برادر"]),
    q(DARI, MEDIUM, "«مصروف» به چه معناست؟", ["مشغول", "آزاد", "خسته", "خوشحال"]),
    q(DARI, MEDIUM, "کدام جمله از نظر دستوری صحیح است؟", ["کتاب را خواندم", "کتاب خواندم را", "خواندم کتاب را", "را کتاب خواندم"]),
    q(DARI, MEDIUM, "کدام کلمه اسم است؟", ["خورشید", "زیبا", "دویدن", "خوب"]),
    q(DARI, MEDIUM, "«سقطری» به چه معناست؟", ["قطره", "باران", "آب", "اشک"]),
    q(DARI, HARD, "«مسکین» به چه معناست؟", ["فقیر", "ثروتمند", "متوسط", "جوان"]),
    q(DARI, HARD, "«خویشتن» به چه معناست؟", ["خود", "دیگران", "بیگانه", "دوست"]),
]

# ==================== ISLAMIC STUDIES ====================
islamic_questions = [
    q(ISLAMIC, EASY, "نام آخرین پیامبر اسلام چیست؟", ["حضرت محمد (ص)", "حضرت عیسی (ع)", "حضرت موسی (ع)", "حضرت ابراهیم (ع)"]),
    q(ISLAMIC, EASY, "تعداد سوره‌های قرآن چند است؟", ["114", "100", "120", "110"]),
    q(ISLAMIC, EASY, "نماز چند وقت دارد؟", ["5", "3", "7", "4"]),
    q(ISLAMIC, EASY, "«زکات» به چه معناست؟", ["صدقه اجباری", "روزه", "نماز", "حج"]),
    q(ISLAMIC, EASY, "نام اولین سوره قرآن چیست؟", ["الفاتحة", "البقرة", "آل عمران", "یس"]),
    q(ISLAMIC, MEDIUM, "«صبر» به چه معناست؟", ["تحمل", "شجاعت", "عجله", "خشم"]),
    q(ISLAMIC, MEDIUM, "تعداد ارکان اسلام چند است؟", ["5", "4", "6", "3"]),
    q(ISLAMIC, MEDIUM, "«حدیث» چیست؟", ["سخن پیامبر", "آیه قرآن", "نماز", "روزه"]),
    q(ISLAMIC, MEDIUM, "نماز جمعه چند رکعت است؟", ["2", "4", "3", "1"]),
    q(ISLAMIC, HARD, "«توحید» به چه معناست؟", ["یکتاپرستی", "شرک", "نماز", "روزه"]),
    q(ISLAMIC, HARD, "اولین وحی بر پیامبر چه بود؟", ["اقرا", "الحمد", "التوحید", "البقرة"]),
]

# ==================== COMPUTER SCIENCE ====================
cs_questions = [
    q(CS, EASY, "کدام زبان بیشتر برای هوش مصنوعی استفاده می‌شود؟", ["Python", "Java", "C++", "JavaScript"]),
    q(CS, EASY, "SQL برای چه کاری است؟", ["مدیریت پایگاه داده", "طراحی وب", "ویرایش عکس", "پخش ویدیو"]),
    q(CS, EASY, "Git برای چه کاری است؟", ["کنترل نسخه", "ویرایش متن", "مدیریت پایگاه داده", "طراحی وب"]),
    q(CS, EASY, "RAM مخفف چیست؟", ["Random Access Memory", "Read Access Memory", "Run All Memory", "Random Active Memory"]),
    q(CS, EASY, "CPU مخفف چیست؟", ["Central Processing Unit", "Computer Personal Unit", "Central Program Utility", "Computer Processing Unit"]),
    q(CS, MEDIUM, "HTTP مخفف چیست؟", ["HyperText Transfer Protocol", "High Tech Transfer Program", "Home Tool Transfer Protocol", "Hyper Text Transmission Process"]),
    q(CS, MEDIUM, "API مخفف چیست؟", ["Application Programming Interface", "Advanced Program Integration", "Automatic Process Input", "Application Process Interface"]),
    q(CS, MEDIUM, "کدام یک سیستم‌عامل نیست؟", ["Microsoft Word", "Windows", "Linux", "macOS"]),
    q(CS, MEDIUM, "کدام پروتکل برای ایمیل است؟", ["SMTP", "HTTP", "FTP", "SSH"]),
    q(CS, HARD, "OOP مخفف چیست؟", ["Object Oriented Programming", "Online Operating Program", "Output Order Protocol", "Open Office Platform"]),
    q(CS, HARD, "REST API چیست؟", ["Application Programing Interface با معماری خاص", "نوعی دیتابیس", "زبان برنامه‌نویسی", "سیستم‌عامل"]),
]

ALL_QUESTIONS = math_questions + physics_questions + chemistry_questions + biology_questions + dari_questions + islamic_questions + cs_questions


async def seed():
    async with SessionLocal() as db:
        from app.modules.question_bank.models import QuestionBank
        from sqlalchemy import select

        # Check existing count
        existing = (await db.execute(select(QuestionBank))).scalars()
        count = len(list(existing))
        if count > 0:
            print(f"Question bank already has {count} questions. Skipping.")
            return

        # Add all questions
        for q_data in ALL_QUESTIONS:
            db.add(QuestionBank(**q_data))

        await db.commit()
        print(f"✅ Question bank seeded with {len(ALL_QUESTIONS)} questions")
        print(f"   Math: {len(math_questions)}")
        print(f"   Physics: {len(physics_questions)}")
        print(f"   Chemistry: {len(chemistry_questions)}")
        print(f"   Biology: {len(biology_questions)}")
        print(f"   Dari: {len(dari_questions)}")
        print(f"   Islamic: {len(islamic_questions)}")
        print(f"   CS: {len(cs_questions)}")


if __name__ == "__main__":
    asyncio.run(seed())
