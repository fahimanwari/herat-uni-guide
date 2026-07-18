# 🗺️ new-plan.md — پلان نسخه ۳ (راهنمای گام‌به‌گام برای تیم)

**تاریخ:** ۱۸ جولای ۲۰۲۶ (۲۷ سرطان ۱۴۰۵) · **مبنا:** b.md + تحقیق انترنتی + کدبیس فعلی
**مخاطب:** توسعه‌دهنده‌ای که شاید تجربه زیاد نداشته باشد — هر گام دقیقاً می‌گوید **کدام فایل را باز کن، چه بنویس، و چطور تست کن که کار می‌کند**. اگر گامی را نفهمیدید، از همان الگوی فایل مشابه که آدرسش داده شده کاپی کنید.

---

# بخش ۰: قبل از هر کاری — محیط کار و قوانین (۱۵ دقیقه بخوانید)

## ۰.۱ راه‌اندازی و اجرا

```bash
# Backend (ترمینال ۱)
cd backend
.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 9000 --reload
# --reload یعنی هر تغییر فایل، سرور خودکار ری‌استارت می‌شود

# Frontend (ترمینال ۲)
cd web
npm run dev        # حالت توسعه — تغییرات فوری دیده می‌شود
# برای production:  npm run build && npm run start   (پورت 4000)
```

- مستندات زنده API: `http://localhost:9000/docs` (Swagger — هر endpoint را همان‌جا تست کنید)
- پنل ادمین: `http://localhost:4000/admin` — ایمیل `admin@herat-uni.edu.af`، رمز در `assist/05-admin.txt`
- دیتابیس: PostgreSQL پورت ۵۴۳۳، دیتابیس `uniguide` (تنظیمات در `backend/.env`)

## ۰.۲ الگوی مقدس ماژول (هر فیچر backend = این ۵ فایل)

```
backend/app/modules/<اسم-فیچر>/
  models.py      ← جدول دیتابیس (SQLAlchemy)
  schemas.py     ← شکل ورودی/خروجی API (Pydantic)
  repository.py  ← فقط خواندن/نوشتن DB
  service.py     ← منطق تجاری
  router.py      ← endpoint ها (هیچ منطقی اینجا نه!)
```
**بهترین نمونه برای کاپی:** ماژول `question_bank` (کامل‌ترین) و زیرجدول‌های `departments` (الگوی projects/alumni).

## ۰.۳ شش قانون آهنین (تخطی = reject شدن PR)

1. **تغییر جدول فقط با Alembic:**
   ```bash
   cd backend
   # ۱) اول ستون/جدول را در models.py اضافه کن، بعد:
   .venv/bin/alembic revision --autogenerate -m "add xyz"
   # ۲) فایل ساخته‌شده در alembic/versions/ را باز کن و بخوان (autogenerate گاهی اشتباه می‌کند!)
   .venv/bin/alembic upgrade head
   ```
2. **هر endpoint نوشتنی (POST/PATCH/DELETE) پشت `admin=Depends(get_current_admin)`** — بدون استثنا.
3. **هر endpoint جدید حداقل ۲ تست:** یکی موفق، یکی «بدون توکن → 401». الگو: `backend/app/tests/test_question_bank_admin.py`. اجرا: `.venv/bin/python -m pytest -q` — **قبل از commit باید همه سبز باشد** (الان ۵۹ تست سبز است).
4. **هیچ رنگ خام Tailwind در فرانت** (`bg-blue-600` ❌) — فقط توکن‌ها: `bg-primary-600`, `text-muted`, `bg-surface-card`, `border-border`, `text-danger`, `bg-success/10`...
5. **بخش خالی در صفحه عمومی = اصلاً render نشود** (نه «داده‌ای نیست»).
6. **بعد از هر تغییر فرانت روی سرور:** `npm run build` + ری‌استارت سرویس web — سرور کهنه build قدیمی را از حافظه سرو می‌کند (دوبار این مشکل را داشتیم!).

## ۰.۴ تعریف «تمام شد» (Definition of Done)

☑ کد نوشته شد ☑ تست‌ها سبز ☑ `npm run build` سبز ☑ در مرورگر با چشم دیده شد ☑ روی موبایل (عرض ۳۷۵px در DevTools) خراب نیست ☑ commit با پیام واضح

---

# بخش ۱: چه چیزی از قبل آماده است؟ (دوباره نسازید!)

| قابلیت | کجاست |
|---|---|
| بانک سوالات با سال (۱۳۹۸-۱۴۰۵)، صنف (۱۰/۱۱/۱۲)، فصل، منبع، تیک تایید | `backend/app/modules/question_bank/` |
| ورود گروهی JSON تراکنشی + UI پنل (چسباندن/آپلود فایل) | پنل → بانک سوالات → «📥 درون‌ریزی JSON» |
| فورم افزودن/ویرایش تک‌سوال با گزینه‌ها و جواب درست | پنل → بانک سوالات → «+ سوال جدید» |
| آمار به تفکیک مضمون/سال/صنف/تاییدشده | `GET /question-bank/stats` |
| کانکور آزمایشی کامل: شروع→تایمر→ثبت→نمره ٪ و از ۳۶۰→تفکیک→مرور→تاریخچه | `backend/app/modules/mock_kankor/` + `web/app/mock-kankor/` |
| الگوی امتحان (blueprint) ۱۶۰ سوالی ۱۰ مضمونه + seed | `backend/seed_blueprint.py` — API کامل: `/mock-kankor/blueprints` |
| فقط سوالات `is_verified=true` وارد آزمون می‌شوند + هر بار ترکیب تصادفی جدید | در کد enforce شده |
| برچسب دینامیک «بر اساس نمرات قبولی سال X» در چانس | خودکار از دیتای کات‌آف |
| ظرفیت DB برای ده‌ها هزار سوال | PostgreSQL + ایندکس — بله، کافی است |

**منابع سوالات واقعی (نتیجه تحقیق):** فورمت رسمی = ۱۶۰ سوال چهارجوابه، نمره کل ۳۶۰، ~۳ ساعت ([NEXA](https://nexa.gov.af/fa/index)).
فورم‌های ۱۳۹۲-۱۳۹۹ با کلید جواب: [anis.af/category/kankor-questions](https://anis.af/category/kankor-questions/) · فورم‌های ۱۴۰۱: [Scribd](https://www.scribd.com/document/619096122/) · بانک دسته‌بندی‌شده: [kankor.io](https://kankor.io/) · سال‌های ۱۴۰۲-۱۴۰۵: کتاب‌های بازار هرات + کانال‌های تلگرام + مراکز کانکور (آنلاین رسمی منتشر نمی‌شود).
کات‌آف‌های رسمی: [۱۴۰۰](https://anis.af/kankor-official-results/112973/) · [۱۴۰۱](https://anis.af/kankor-official-results/129173/) · ۱۴۰۲ در anis.af.

---

# فاز ۱ — جمع‌آوری سوالات ۱۳۹۸-۱۴۰۵ (تیم محتوا — کد لازم ندارد)

**هدف:** ~۳,۰۰۰-۵,۰۰۰ سوال verified.

## گام‌به‌گام برای هر عضو تیم محتوا

1. PDF سال مربوطه را دانلود کن (لینک‌های بالا).
2. فایل `scripts/question_format.json` را باز کن — این قالب هر سوال است:
   ```json
   {
     "subject": "ریاضی",
     "year": 1398,
     "grade": "11",
     "chapter": "مثلثات",
     "source": "کانکور ۱۳۹۸ — آرشیف انیس",
     "difficulty": "medium",
     "question_fa": "متن سوال...",
     "options": [
       {"text": "جواب درست", "is_correct": true},
       {"text": "گزینه ۲"}, {"text": "گزینه ۳"}, {"text": "گزینه ۴"}
     ],
     "explanation_fa": "چرا این جواب درست است (اختیاری ولی خیلی مفید)"
   }
   ```
   ⚠️ نام مضمون‌ها دقیقاً یکدست: `ریاضی، فزیک، کیمیا، بیولوژی، دری، پشتو، تعلیمات اسلامی، تاریخ، جغرافیه، انگلیسی`
3. ۵۰-۱۰۰ سوال را در یک فایل JSON (آرایه `[...]`) جمع کن.
4. پنل ادمین → بانک سوالات → «📥 درون‌ریزی JSON» → فایل را بچسبان/آپلود کن → «بررسی و درون‌ریزی».
   - اگر حتی ۱ ردیف خطا داشته باشد، **هیچ‌چیز ذخیره نمی‌شود** و شماره ردیف خطا را می‌گوید — همان ردیف را اصلاح کن و دوباره.
5. **بازبینی (نفر دوم — نه واردکننده!):** پنل → بانک سوالات → هر سوال را با PDF مقایسه → دکمه ویرایش → تیک «تایید شده». فقط بعد از این تیک، سوال وارد آزمون‌ها می‌شود.
6. پیشرفت: داشبورد پنل آمار به تفکیک سال/صنف را نشان می‌دهد.

**ترتیب:** هفته ۱: ۱۳۹۸+۱۳۹۹ (انیس، کلید جواب دارد) → هفته ۲: ۱۴۰۰+۱۴۰۱ → هفته ۳-۴: ۱۴۰۲-۱۴۰۵ (کتاب بازار). سهم هر نفر: ~۲۰۰ سوال/هفته.

**معیار پذیرش:** هر سال هدف ≥۳۰۰ سوال verified · هر مضمونِ blueprint حداقل ۳×count سوال verified · ۱۰ آزمون پشت‌سرهم بدون تکرار فورم.

---

# فاز ۲ — تطبیق دقیق با فورم واقعی + تب «الگوهای امتحان» در پنل (۲-۳ روز)

## ۲.۱ تایید اعداد (نیم روز — با تیم محتوا)

فورم PDF سال ۱۴۰۱ (یا ۱۳۹۹ انیس) را باز کنید و **تعداد سوال هر مضمون را بشمارید.** اعداد فعلی blueprint تخمینی است: ریاضی۳۰/فزیک۲۴/کیمیا۲۴/بیولوژی۲۴/دری۱۲/پشتو۶/اسلامی۱۲/تاریخ۱۰/جغرافیه۸/انگلیسی۱۰ = ۱۶۰.
اگر فرق داشت، در فایل `backend/seed_blueprint.py` لیست `SECTIONS` را اصلاح و دوباره اجرا کنید:
```bash
cd backend && .venv/bin/python seed_blueprint.py   # اگر وجود داشته باشد آپدیت می‌کند
```

## ۲.۲ تب «الگوهای امتحان» در پنل ادمین (۱-۲ روز)

API از قبل کامل است (`GET/POST/PATCH/DELETE /mock-kankor/blueprints`) — فقط UI می‌خواهد. فایل: `web/app/admin/page.tsx`

گام ۱ — به آرایه `menuGroups` (خط ~۱۲)، در گروه «کانکور» اضافه کنید:
```ts
{ id: "blueprints", icon: "📐", label: "الگوهای امتحان" },
```

گام ۲ — در تابع `loadTab`، به آبجکت `endpoints` اضافه کنید:
```ts
blueprints: "/mock-kankor/blueprints",
```

گام ۳ — چون `sections` یک JSON است و فورم عمومی مودال آن را نمی‌فهمد، مثل «بانک سوالات» یک **مودال اختصاصی** بسازید. الگوی کامل: state ها و توابع `showQuestionModal / openQuestionCreate / handleQuestionSave` در همین فایل را کاپی و تغییر نام دهید (`showBlueprintModal / ...`). فورم مودال:
- `name_fa` (input متن) · `description_fa` (textarea) · `total_minutes` (input عدد)
- **بخش‌ها (sections):** لیست ردیف‌های «مضمون + تعداد» با دکمه «+ افزودن مضمون» و «حذف» — عین الگوی گزینه‌های سوال در مودال بانک سوالات
- زیر فورم جمع زنده نشان دهید: `مجموع سوالات: {sections.reduce((s,x)=>s+Number(x.count||0),0)}` و اگر ≠۱۶۰ با `text-warning` هشدار دهید

گام ۴ — ستون‌های جدول لیست (در بخش GENERIC TABLES، عین `sidebar === "exams"` را کاپی کنید):
نام | مدت (دقیقه) | تعداد بخش‌ها | مجموع سوالات | عملیات (ویرایش/حذف)

گام ۵ — تست دستی: تب جدید → «+ افزودن» → الگوی ۲۰ سوالی بسازید → صفحه `/mock-kankor` سایت باید کارت «کامل» را با همین الگو نشان دهد (فرانت خودکار اولین blueprint فعال را می‌گیرد) → حذفش کنید.

## ۲.۳ نمایش ترکیب مضامین به شاگرد (۱ ساعت)

فایل: `web/app/mock-kankor/page.tsx` — آبجکت `fullBlueprint` از قبل fetch می‌شود. داخل کارت گزینه «کامل»، زیر توضیحات اضافه کنید:
```tsx
{opt.id === "full" && fullBlueprint && (
  <p className="text-muted text-xs mt-2">
    {fullBlueprint.sections.map(s => `${s.subject} ${s.count}`).join(" · ")}
  </p>
)}
```

**معیار پذیرش فاز ۲:** اسکرین‌شات فورم واقعی کنار صفحه آزمون قابل دفاع باشد · ادمین بتواند بدون دست زدن به کد، الگو بسازد/اصلاح کند.

---

# فاز ۳ — ورود کات‌آف‌های ۱۴۰۰-۱۴۰۵ (تیم محتوا — کد لازم ندارد)

1. PDF های انیس (لینک‌های بخش ۱) را دانلود کنید.
2. فقط ردیف‌های **پوهنتون هرات** را پیدا کنید.
3. پنل → کات‌آف → «+ افزودن» → دیپارتمنت + سال + پایین‌ترین نمره + ظرفیت.
4. نتایج ۱۴۰۳/۱۴۰۴/۱۴۰۵ را از nexa.gov.af پیگیری و به محض انتشار وارد کنید — برچسب «بر اساس سال X» در سایت **خودکار** عوض می‌شود، کد نمی‌خواهد.

**معیار پذیرش:** هر دیپارتمنت فارغ‌ده ≥۳ سال کات‌آف.

---

# فاز ۴.۱ — رهنمای جامع آشنایی با رشته (۴-۶ روز کد + کار محتوایی موازی)

**هدف:** شاگرد بداند (الف) این رشته برای او هست یا نه، (ب) سمستر به سمستر چه می‌خواند، (ج) نمونه درس واقعی استادان را ببیند.

## گام ۱ — backend: دو فیلد + یک جدول (۱ روز)

**فایل `backend/app/modules/departments/models.py`** — داخل class `Department` بعد از `difficulty_level` اضافه کنید:
```python
    # ⭐ آشنایی برای شاگرد مکتب: «آیا این رشته برای من است؟»
    intro_fa: Mapped[str | None] = mapped_column(Text)
    # مضامین سمستروار: [{"semester": 1, "subjects": ["ریاضی ۱", "فزیک ۱"]}, ...]
    curriculum: Mapped[list] = mapped_column(JSON, default=list)
```
و به relationship های Department اضافه کنید:
```python
    lecture_videos = relationship("DepartmentVideo", back_populates="department", cascade="all, delete-orphan")
```
و در انتهای فایل، جدول جدید (الگوی `StudentProject` همین فایل):
```python
class DepartmentVideo(Base):
    """ویدیوهای درسی — منبع اصلی: ویدیوهای ترفیع علمی استادان."""
    __tablename__ = "department_videos"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    department_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("departments.id", ondelete="CASCADE"))
    title_fa: Mapped[str] = mapped_column(String(300))
    subject: Mapped[str | None] = mapped_column(String(150))
    semester: Mapped[int | None] = mapped_column(Integer)
    lecturer_name: Mapped[str | None] = mapped_column(String(200))
    video_url: Mapped[str] = mapped_column(String(500))
    description_fa: Mapped[str | None] = mapped_column(Text)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    department = relationship("Department", back_populates="lecture_videos")
```
⚠️ بالای فایل `Boolean` را به import های sqlalchemy اضافه کنید.

بعد migration (قانون ۰.۳-۱):
```bash
cd backend
.venv/bin/alembic revision --autogenerate -m "department intro curriculum videos"
# فایل ساخته‌شده را باز کنید و مطمئن شوید فقط این ۳ تغییر است
.venv/bin/alembic upgrade head
```

**فایل `backend/app/modules/departments/schemas.py`:**
```python
# --- Department Video ---
class DepartmentVideoSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    title_fa: str
    subject: str | None
    semester: int | None
    lecturer_name: str | None
    video_url: str
    description_fa: str | None
    sort_order: int

class DepartmentVideoCreate(BaseModel):
    title_fa: str
    video_url: str
    subject: str | None = None
    semester: int | None = None
    lecturer_name: str | None = None
    description_fa: str | None = None
    sort_order: int = 0
```
و به `DepartmentDetail` اضافه کنید: `intro_fa: str | None = None` · `curriculum: list = []` · `lecture_videos: list[DepartmentVideoSchema] = []`
و به `DepartmentCreate`/`DepartmentUpdate`: `intro_fa` و `curriculum` (اختیاری، مثل بقیه فیلدها).

**فایل `router.py`** — سه endpoint، دقیقاً عین `add_student_project` موجود در همین فایل (کاپی کنید و نام‌ها را عوض کنید):
`POST /{slug}/videos` · `PATCH /{slug}/videos/{video_id}` · `DELETE /{slug}/videos/{video_id}` — هر سه با `admin: AdminUser = Depends(get_current_admin)`.
**فایل‌های `service.py` و `repository.py`** — متدهای `add_video / update_video / delete_video` عین `add_student_project` موجود.
⚠️ در repository جایی که دیپارتمنت با جزئیات لود می‌شود (`selectinload`)، `Department.lecture_videos` را هم اضافه کنید.

**تست** — فایل جدید `backend/app/tests/test_department_videos.py` (الگوی `test_question_bank_admin.py`):
۱) POST بدون توکن → 401 ۲) POST با توکن → 201 و بعد GET دیپارتمنت شامل ویدیو ۳) DELETE → از GET حذف شود.
```bash
.venv/bin/python -m pytest app/tests/test_department_videos.py -q
```

## گام ۲ — پنل ادمین (۱ روز)

فایل: `web/app/admin/page.tsx` — مودال «زیرمجموعه‌های دیپارتمنت» از قبل ۳ تب دارد (`subTab`: projects/alumni/roadmaps). دو تب اضافه کنید:

1. **تب «ویدیوها»:** به type و آرایه تب‌ها `"videos"` اضافه کنید؛ در `loadSubItems`: `if (tab === "videos") setSubItems(dept.lecture_videos || []);`؛ در defaults فورم:
   ```ts
   videos: { title_fa: "", video_url: "", subject: "", semester: 1, lecturer_name: "", description_fa: "" },
   ```
   endpoint در `handleSubSave`/`handleSubDelete`: `videos`.
2. **تب «مضامین سمستروار»:** UI ساده — برای هر سمستر یک ردیف: شماره سمستر + textarea مضامین (هر خط یک مضمون) + دکمه «+ سمستر». موقع ذخیره تبدیل کنید و PATCH خود دیپارتمنت بزنید:
   ```ts
   const curriculum = rows.map(r => ({ semester: Number(r.sem), subjects: r.text.split("\n").map(s=>s.trim()).filter(Boolean) }));
   await adminApi.update(`/departments/${subDept.slug}`, { curriculum });
   ```
3. `intro_fa` خودش در فورم ویرایش دیپارتمنت می‌آید (string است). ⚠️ ولی `curriculum` را از فورم عمومی مخفی کنید تا JSON خام نشان ندهد — در حلقه `Object.entries(formData)` مودال عمومی: `if (key === "curriculum") return null;`

## گام ۳ — صفحه عمومی رشته (۱ روز)

فایل: `web/app/faculties/[slug]/[dept]/page.tsx` — سه بخش جدید (قانون: خالی بود، render نکن):

```tsx
{/* آیا این رشته برای من است؟ */}
{dept.intro_fa && (
  <Card className="mb-8">
    <h2 className="font-bold text-xl text-foreground mb-3">🤔 آیا این رشته برای من است؟</h2>
    <p className="text-foreground leading-8 whitespace-pre-line">{dept.intro_fa}</p>
    <div className="flex gap-3 mt-4">
      <Link href="/quiz"><Button variant="outline">🎯 آزمون علاقه بده</Button></Link>
      <Link href="/chat"><Button variant="outline">💬 از مشاور AI بپرس</Button></Link>
    </div>
  </Card>
)}

{/* مضامین سمستر به سمستر */}
{dept.curriculum?.length > 0 && (
  <Card className="mb-8">
    <h2 className="font-bold text-xl text-foreground mb-3">📚 چه می‌خوانید؟ — سمستر به سمستر</h2>
    {dept.curriculum.map((c: any, i: number) => (
      <details key={c.semester} open={i === 0} className="border-b border-border py-3">
        <summary className="cursor-pointer font-medium text-foreground">سمستر {c.semester} — {c.subjects.length} مضمون</summary>
        <ul className="mt-2 pr-6 list-disc text-muted">
          {c.subjects.map((s: string) => <li key={s}>{s}</li>)}
        </ul>
      </details>
    ))}
  </Card>
)}

{/* نمونه درس استادان */}
{dept.lecture_videos?.length > 0 && (
  <Card className="mb-8">
    <h2 className="font-bold text-xl text-foreground mb-3">🎬 نمونه درس‌های استادان</h2>
    <div className="grid md:grid-cols-2 gap-4">
      {dept.lecture_videos.map((v: any) => (
        <div key={v.id} className="border border-border rounded-[10px] overflow-hidden">
          <iframe loading="lazy" className="w-full aspect-video"
            src={`https://www.youtube.com/embed/${v.video_url.split("v=")[1]?.split("&")[0] || v.video_url.split("/").pop()}`}
            title={v.title_fa} allowFullScreen />
          <div className="p-3">
            <p className="font-medium text-foreground">{v.title_fa}</p>
            <p className="text-muted text-sm">{v.lecturer_name}{v.subject ? ` · ${v.subject}` : ""}{v.semester ? ` · سمستر ${v.semester}` : ""}</p>
          </div>
        </div>
      ))}
    </div>
  </Card>
)}
```
type های `web/app/lib/types.ts` را هم آپدیت کنید (`intro_fa?`, `curriculum?`, `lecture_videos?`).

## گام ۴ — اتصال به چت‌بات (نیم روز)

فایل: `backend/app/modules/ai/indexer.py` — متد `_department_to_text` را گسترش دهید (به آخر رشته برگشتی اضافه کنید):
```python
        intro = f" آشنایی: {d.intro_fa}" if d.intro_fa else ""
        curriculum = ""
        for c in (d.curriculum or []):
            curriculum += f" مضامین سمستر {c['semester']}: {'، '.join(c['subjects'])}."
        videos = ""
        if d.lecture_videos:
            names = "، ".join(f"{v.title_fa} (استاد {v.lecturer_name or 'نامشخص'})" for v in d.lecture_videos if v.is_active)
            videos = f" ویدیوهای درسی موجود: {names}."
        return (متن_قبلی + intro + curriculum + videos)
```
⚠️ در query ایندکسر `selectinload(Department.lecture_videos)` را اضافه کنید. بعد: پنل → «🤖 بازسازی دانش».

**تست پذیرش:** از چت‌بات بپرسید «در سمستر اول کمپیوتر ساینس چه می‌خوانم؟» و «آیا انجنیری برای من مناسب است؟» — جواب باید از دیتای واقعی باشد.

## گام ۵ — کار سازمانی موازی (تیم محتوا — از امروز)

1. نامه رسمی به معاونیت علمی: دسترسی به آرشیف ویدیوهای ترفیع + **اجازه کتبی نشر** (بدون اجازه کتبی = نشر ممنوع).
2. از ۱۶ رابط پوهنځی: لیست ویدیوها + رضایت استاد + عکس کریکولم رسمی هر دیپارتمنت.
3. معیار ویدیو: صدای واضح + مضمون سمستر ۱-۲ + ترجیحاً <۳۰ دقیقه. آپلود: کانال YouTube پروژه (unlisted کافی است). نام استاد همیشه ذکر شود.
4. هدف موج اول: هر پوهنځی ≥۱ ویدیو (۱۶ ویدیو).

**معیار پذیرش ۴.۱:** ۳ دیپارتمنت نمونه (کمپیوتر ساینس، طب، حقوق) با intro + کریکولم ≥۴ سمستر + ≥۱ ویدیو · دو سوال محک چت‌بات درست جواب داده شود · تست‌ها و build سبز.

---

# فاز ۴.۲ — Gamification (۳-۴ روز)

## Backend (۱ روز) — ماژول جدید `backend/app/modules/achievements/` (الگوی ۵ فایلی)

```python
# models.py
class UserAchievement(Base):
    __tablename__ = "user_achievements"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    session_id: Mapped[str] = mapped_column(String(100), index=True)  # همان session ناشناس مرورگر
    badge_key: Mapped[str] = mapped_column(String(50))   # 'first_exam', 'five_exams', 'score_200', 'streak_7', 'math_master'
    earned_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
```
- `GET /achievements?session_id=` → لیست نشان‌های کسب‌شده (عمومی)
- منطق اهدا در `service.py`: تابع `check_and_award(session_id)` که بعد از هر ثبت آزمون از `mock_kankor/service.py` صدا زده می‌شود — تعداد آزمون‌ها و نمرات را از `mock_exam_sessions` می‌خواند و نشان جدید می‌دهد.
- تعریف نشان‌ها یک dict ثابت در service (اسم + شرط + ایموجی) — جدول جدا لازم نیست.
- Streak: از تاریخ‌های `mock_exam_sessions.created_at` همان session حساب کنید (روزهای پشت‌سرهم دارای حداقل ۱ آزمون).
- Leaderboard هفتگی: `GET /achievements/leaderboard` → ۱۰ نمره برتر ۷ روز اخیر از `mock_exam_sessions` (فقط `score_360` و یک نام مستعار `شاگرد ۱، شاگرد ۲...` — **هیچ session_id به بیرون داده نشود**).
- در `main.py` دو خط include (عین بقیه). تست: ۲ تست حداقل.

## Frontend (۱-۲ روز)

- صفحه نتیجه آزمون: اگر نشان جدید کسب شد، کارت «🏅 نشان جدید گرفتی!» (backend در جواب submit فیلد `new_badges: []` برگرداند — به `MockExamResult` اضافه کنید).
- صفحه `/mock-kankor/history`: ردیف نشان‌ها بالای تاریخچه + **نمودار پیشرفت نمره** (بدون کتابخانه — SVG ساده: هر آزمون یک نقطه، خط بین‌شان؛ یا `<div>` های میله‌ای با ارتفاع `score%`).
- کامپوننت leaderboard در صفحه `/mock-kankor` (پایین صفحه، جدول ساده).

**معیار پذیرش:** بعد از اولین آزمون نشان «اولین قدم» ظاهر شود · نمودار با ≥۲ آزمون خط روند نشان دهد · leaderboard هیچ اطلاعات شناسایی‌کننده نشان ندهد.

---

# فاز ۴.۳ — AI Study Planner (۲ روز)

## Backend — endpoint جدید در `backend/app/modules/ai/router.py`

```python
class StudyPlanRequest(BaseModel):
    session_id: str

@router.post("/study-plan")
async def study_plan(payload: StudyPlanRequest, request: Request, db: AsyncSession = Depends(get_db)):
    client_ip = request.client.host
    await rate_limiter.check_rate_limit(f"plan:{client_ip}", limit=5, window=86400)
    return await StudyPlanService(db).generate(payload.session_id)
```

`StudyPlanService` (فایل جدید `study_plan.py` در همان ماژول ai):
1. آخرین ۵ ردیف `mock_exam_sessions` این session را بخوان → میانگین درصد هر مضمون از `subject_scores`.
2. نزدیک‌ترین رویداد کانکور از `academic_events` (چند روز مانده).
3. پرامپت به `get_ai_provider().chat(...)` (الگوی `service.py` همین ماژول):
   ```
   تو مشاور تحصیلی کانکور هستی. نقاط ضعف شاگرد: {ضعیف‌ترین ۳ مضمون با درصد}.
   تا کانکور {X} روز مانده. یک برنامه مطالعه هفتگی واقع‌بینانه به دری بساز:
   هر روز حداکثر ۳ ساعت، مضامین ضعیف‌تر وقت بیشتر، هر هفته یک آزمون آزمایشی کامل.
   خروجی: جدول روز-به-روز ساده.
   ```
4. اگر session هیچ آزمونی ندارد → پیام «اول یک کانکور آزمایشی بده تا نقاط ضعفت را بشناسم» (نه خطا).

## Frontend

- دکمه «📅 برنامه مطالعه بساز» در صفحه نتیجه آزمون → مودال/صفحه‌ای که جواب را نمایش می‌دهد (متن چندخطی، `whitespace-pre-line`) + دکمه کاپی.

**معیار پذیرش:** با ≥۱ آزمون قبلی، برنامه شخصی برگردد که اسم مضامین ضعیف واقعی شاگرد در آن باشد.

---

# فاز ۴.۴ — تقویت هوش مصنوعی (۲-۳ روز + کار مستمر)

## ۴.۴.الف — ایندکس همه‌چیز (۱ روز)

فایل `backend/app/modules/ai/indexer.py`: به `reindex_all` متدهای جدید اضافه کنید — دقیقاً به سبک `_index_departments` موجود:
```python
        count += await self._index_news()        # فقط is_published=true → عنوان + متن
        count += await self._index_faqs()        # سوال + جواب
        count += await self._index_guides()      # KankorGuide: عنوان + متن
        count += await self._index_events()      # رویداد + تاریخ («ثبت‌نام کانکور: ۱۵ حوت ۱۴۰۵»)
```
هر متد: select از جدول مربوطه → متن دری بساز → `_split` → `RagChunk(source_type="news", ...)`. تست: reindex از پنل → تعداد chunk ها باید چند برابر شود → از چت‌بات یک سوال خبری/FAQ بپرسید.

## ۴.۴.ب — خط لوله فورم‌های `question/` (وقتی جواب‌ها رسید — تیم محتوا)

نگاشت جواب فورم → سیستم: بخش ۳.۴+۵.۱+۵.۲ → فیلد `intro_fa` · بخش ۳.۳ → `subjects` · بخش ۴ → `career_paths` و `job_market_fa` · بخش ۶ → کات‌آف‌ها · بخش ۷ → پروژه‌ها/فارغان · بخش ۸.۱ → FAQ (category = نام دیپارتمنت). هر ۵-۱۰ دیپارتمنت → یک reindex.

## ۴.۴.ج — ست ۲۰ سوال محک (Golden Set)

فایل `assist/golden-questions.md`: ۲۰ سوال واقعی (از لاگ چت پنل + بخش ۸.۱ فورم‌ها) + جواب درست مورد انتظار. بعد از هر reindex، هر ۲۰ سوال را از چت‌بات بپرسید و نمره دهید (درست/ناقص/غلط) و تاریخ‌دار ثبت کنید — روند باید صعودی باشد. لاگ چت پنل را هفتگی مرور کنید: سوال بی‌جواب = محتوایی که باید اضافه شود.

---

# فاز ۴.۵ — خبرچین هوشمند: جمع‌آوری خودکار اخبار پوهنتون هرات (۲-۳ روز)

**قانون خط قرمز: هیچ خبری بدون تایید انسان منتشر نمی‌شود.** (پلتفرم زیر نام پوهنتون است — یک خبر غلط خودکار = اعتبار بربادرفته.)

## گام ۱ — دو ستون جدید روی جدول news (+migration، قانون ۰.۳-۱)

```python
    source_url: Mapped[str | None] = mapped_column(String(500), unique=True)  # جلوگیری از تکرار
    is_ai_draft: Mapped[bool] = mapped_column(Boolean, default=False)
```

## گام ۲ — اسکریپت `backend/jobs/fetch_news.py` (پوشه jobs جدید)

نصب: `pip install beautifulsoup4` (+ به `requirements.txt` اضافه کنید).
```python
"""هفتگی با cron اجرا می‌شود: crontab -e →
0 6 * * 6  cd /path/backend && .venv/bin/python jobs/fetch_news.py"""
SOURCES = [
    "https://hu.edu.af",        # اخبار خود پوهنتون
    "https://mohe.gov.af",      # وزارت تحصیلات عالی
    "https://nexa.gov.af/fa",   # اداره ملی امتحانات
]
KEYWORDS = ["هرات", "کانکور", "پوهنتون"]
```
منطق (ساده نگه دارید):
1. با `httpx` هر صفحه را بگیر → با BeautifulSoup لینک‌ها و عنوان‌های خبر را دربیاور.
2. فقط آیتم‌هایی که حداقل یک KEYWORD دارند.
3. اگر `source_url` قبلاً در جدول news هست → رد شو (تکراری).
4. متن صفحه خبر را بگیر → به `get_ai_provider().chat()` بده:
   «این متن را به یک خبر کوتاه دری (حداکثر ۱۵۰ کلمه) برای داوطلبان کانکور هرات بازنویسی کن. فقط واقعیت‌های داخل متن — چیزی اضافه نکن.»
5. ذخیره: `News(title_fa=عنوان, body_fa=خلاصه + "\n\nمنبع: " + url, source_url=url, is_published=False, is_ai_draft=True, university_id=هرات)`
6. آخر کار print کن: چند خبر جدید پیدا شد (برای لاگ cron).

## گام ۳ — پنل ادمین

تب اخبار: کنار عنوان درفت‌های AI نشان `🤖 پیشنهاد AI` (وقتی `is_ai_draft && !is_published` — با `bg-accent-500/10 text-accent-600`). ادمین باز می‌کند → ویرایش → تیک انتشار، یا حذف. داشبورد: شمارنده «X پیش‌نویس در انتظار تایید».

**معیار پذیرش:** یک هفته اجرا → ≥۳ درفت مرتبط · صفر انتشار خودکار · هر خبر منتشره لینک منبع دارد · اجرای دوباره اسکریپت تکراری نمی‌سازد.

---

# فاز ۴.۶ — تقویم خودکار کانکور + بنر شمارش معکوس صفحه اصلی (۲ روز)

## گام ۱ — اسکریپت `backend/jobs/fetch_kankor_dates.py`

مثل ۴.۵ ولی فقط اطلاعیه‌های NEXA/وزارت را می‌خواند و از AI می‌خواهد این ۴ تاریخ را برای **زون هرات** استخراج کند (خروجی JSON بخواهید):
```
ثبت‌نام/فورم‌گیری · بایومتریک · روز امتحان · اعلان نتایج
جواب فقط JSON: [{"event_type":"kankor_registration","title_fa":"...","date":"YYYY-MM-DD","source_url":"..."}]
اگر تاریخی در متن نبود، آن را از خودت نساز — حذفش کن.
```
ذخیره در `academic_events` با `is_active=False` (= پیش‌نویس، در سایت دیده نمی‌شود چون endpoint عمومی فقط active ها را می‌دهد — بررسی کنید و اگر فیلتر نبود اضافه کنید) + `description_fa` شامل لینک اطلاعیه. **تایید ادمین:** در تب رویدادها فعالش می‌کند. تکراری‌گیری: عنوان+تاریخ یکسان → رد.
⚠️ تاریخ غلط امتحان برای شاگرد فاجعه است — به همین دلیل تایید انسانی الزامی و لینک منبع اجباری است.

## گام ۲ — بنر برجسته صفحه اصلی

فایل `web/app/page.tsx` — رویدادها از قبل fetch می‌شوند. بالای صفحه (زیر Header):
```tsx
{nextKankorEvent && (
  <div className="bg-gold-500 text-white text-center py-3 px-4 font-bold">
    ⏰ {daysLeft} روز تا {nextKankorEvent.title_fa} —
    <Link href="/kankor" className="underline mr-2">جزئیات</Link>
  </div>
)}
```
`nextKankorEvent` = نزدیک‌ترین رویداد آینده با `event_type` شروع‌شونده با `kankor` · `daysLeft` = تفاوت روز با امروز.

**معیار پذیرش:** تاریخ‌های کانکور ۱۴۰۶ قبل از موج اعلان عمومی در سایت باشد · بنر فقط وقتی رویداد آینده هست دیده شود · هر رویداد لینک اطلاعیه رسمی دارد.

---

# فاز ۵ — موج دوم (بعد از فاز ۴ — هر آیتم مستقل)

## ۵.۱ OCR سوالات (اول این! — سرعت فاز ۱ را چند برابر می‌کند) — ۲ روز
ابزار داخل پنل: تب بانک سوالات → دکمه «📷 استخراج از عکس»:
- Backend: `POST /question-bank/ocr` (admin) — عکس base64 بگیرد → به Gemini flash با پرامپت «سوالات چهارجوابه این عکس را به این JSON دربیاور: {فورمت question_format.json}» → JSON خام برگرداند. (provider فعلی متد تصویر ندارد — متد `chat_with_image` به `GeminiProvider` اضافه کنید؛ برای Groq همان endpoint پیام «فقط با Gemini» بدهد.)
- Frontend: عکس آپلود → JSON استخراجی داخل **همان textarea مودال درون‌ریزی موجود** ریخته شود → انسان اصلاح → دکمه درون‌ریزی موجود. (هیچ ذخیره مستقیم بدون چشم انسان!)

## ۵.۲ صدای AI — Whisper — ۱ روز
- Backend: `POST /ai/transcribe` — فایل صوتی → Groq API آدرس `https://api.groq.com/openai/v1/audio/transcriptions` مدل `whisper-large-v3` (همان `AI_API_KEY` فعلی!) → متن.
- Frontend صفحه چت: دکمه 🎤 با `MediaRecorder` مرورگر → ارسال → متن داخل input چت.
- Rate limit مثل چت (۲۰/روز).

## ۵.۳ اکانت اختیاری کاربر — ۲-۳ روز
Backend کامل است (`/users/register,login,refresh`). فرانت: صفحه `/login` و `/register` (فورم ساده، الگوی فورم لاگین ادمین در `admin/page.tsx`) + ذخیره توکن مثل `adminApi.ts` (کاپی → `userApi.ts`) + بعد از لاگین، `session_id` ناشناس فعلی به حساب لینک شود (endpoint کوچک `POST /users/link-session` بسازید که ردیف‌های `mock_exam_sessions` آن session را به `user_id` وصل کند — ستون `user_id` nullable به جدول اضافه کنید + migration). **قانون:** هیچ قابلیتی پشت لاگین قفل نشود — فقط مزیت «تاریخچه دائمی + نمودار پیشرفت».

## ۵.۴ چندپوهنتونی — ۳-۴ روز
معماری آماده است. گام‌ها: (۱) تب پوهنتون‌ها در پنل برگردد (کامنت راهنما در کد هست) (۲) دیتای ۲-۳ پوهنتون بزرگ (کابل/بلخ/ننگرهار — فقط رشته‌ها + کات‌آف از همان PDF های انیس که همه پوهنتون‌ها را دارد) (۳) سوئیچر در Header (۴) چانس قبولی: گروه‌بندی نتایج بر اساس پوهنتون.

## ۵.۵ Resume Builder + تمرین مصاحبه — ۳ روز
- CV: صفحه فورم چندگامی → خروجی چاپی با CSS `@media print` (کتابخانه PDF لازم نیست — دکمه «چاپ/ذخیره PDF» مرورگر).
- مصاحبه: در صفحه چت حالت «تمرین مصاحبه» — system prompt: «تو مصاحبه‌گر شغل X هستی؛ ۵ سوال یکی‌یکی بپرس، آخر بازخورد بده».

## ۵.۶ تور مجازی / نقشه کمپس — ۲-۳ روز MVP
عکس پاناروما با موبایل از هر پوهنځی → نمایش با `<model-viewer>` یا viewer سبک 360 (فایل local، بدون CDN) + نقشه SVG کمپس با پین هر پوهنځی → کلیک = صفحه پوهنځی. Indoor map دقیق طبقه‌به‌طبقه: فقط بعد از موفقیت MVP.

---

# بخش ویژه: فورم‌های پوشه `question/` — آپدیت لازم است؟ بله، با «ضمیمه نسخه ۲»

بررسی شد: فورم‌ها معرفی ساده، «چه کسی انتخاب نکند»، مسیر شغلی، کات‌آف و FAQ را عالی پوشش می‌دهند ✅ ولی **دو چیز را نمی‌پرسند** چون قبل از درخواست‌های جدید طراحی شده‌اند: (۱) کریکولم سمستروار (۲) ویدیوهای ترفیع استادان.

**راه‌حل: یک فایل ضمیمه کوتاه واحد** `question/ضمیمه-فورم-نسخه۲.txt` (~۱۰ دقیقه پر کردن) — نه ویرایش ۹۰ فایل:
- **بخش ۹ — کریکولم سمستروار:** «مضامین هر سمستر (هر سمستر یک سطر) — یا عکس کریکولم رسمی را ضمیمه کنید [آپلود]» (آپشن عکس مهم است: آمریت‌ها کریکولم چاپی دارند)
- **بخش ۱۰ — ویدیوهای درسی:** کدام استادان ویدیو (به‌خصوص ترفیع) دارند؟ نام + مضمون + سمستر + لینک/فایل + «آیا استاد اجازه کتبی نشر می‌دهد؟ ○ بله ○ باید پرسیده شود»
- **بخش ۱۱ (اختیاری):** نمره ۰-۵ به شش ویژگی رشته (منطق/ریاضی · علوم زیستی · زبان · هنر · اجتماعی · عملی-فنی) [جدول] → مستقیم `trait_weights` آزمون علاقه را دقیق می‌کند (الان حدسی است)

ارسال به همان ۱۶ رابط + جدول پیگیری (دیپارتمنت / فورم اصلی ✓✗ / ضمیمه ✓✗).

---

# بخش پایانی: ریسک‌ها و ترتیب اجرا

| ریسک | پاسخ |
|---|---|
| سوالات ۱۴۰۲-۱۴۰۵ آنلاین نیست | کتاب بازار + مراکز کانکور + OCR (۵.۱)؛ لانچ با ۱۳۹۸-۱۴۰۱ هم ارزشمند است |
| سوال/جواب غلط وارد شود | بازبینی دومرحله‌ای + فیلد source + (backlog) دکمه «گزارش خطا» زیر هر سوال مرور |
| خبر یا تاریخ غلط خودکار منتشر شود | **هرگز انتشار بدون تایید انسان** — در ۴.۵ و ۴.۶ enforce شده |
| ادعای «عین فورم رسمی» بدون سند | تا فاز ۲ تمام نشده بنویسید «بر اساس سوالات سال‌های قبل» |
| ویدیوی استاد بدون اجازه | اجازه کتبی الزامی — بخش ۱۰ ضمیمه |
| سرور فرانت build کهنه سرو کند | بعد از هر deploy: build + restart (قانون ۰.۳-۶) |

**ترتیب اجرا:**
فاز ۱ (محتوا — از امروز، موازی همیشگی) ∥ فاز ۳ (محتوا)
کد: فاز ۲ → ۴.۱ → ۴.۴.الف → ۴.۶ → ۴.۵ → ۴.۲ → ۴.۳ → ۵.۱ → ۵.۲ → ۵.۳ → ۵.۴ → ۵.۵ → ۵.۶
