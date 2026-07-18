"use client";

import { useState, useEffect } from "react";
import { Header } from "../components/layout/Header";
import { Footer } from "../components/layout/Footer";
import { adminApi } from "../lib/adminApi";

const API = "http://localhost:9000/api/v1";

// Design tokens (Kashi Herati)
const C = {
  primary: "bg-primary-600 text-white",
  primaryHover: "hover:bg-primary-700",
  accent: "bg-accent-500 text-white",
  gold: "bg-gold-500 text-white",
  surface: "bg-surface",
  card: "bg-surface-card",
  text: "text-foreground",
  muted: "text-muted",
  border: "border-border",
  success: "text-success",
  danger: "text-danger",
  warning: "text-warning",
};

export default function AdminPage() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [sidebar, setSidebar] = useState("dashboard");
  const [data, setData] = useState<any>({});
  const [loading, setLoading] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [modalType, setModalType] = useState("");
  const [editItem, setEditItem] = useState<any>(null);
  const [formData, setFormData] = useState<any>({});
  const [toast, setToast] = useState({ text: "", type: "" });
  const [loginForm, setLoginForm] = useState({ email: "", password: "" });
  const [search, setSearch] = useState("");
  const [mounted, setMounted] = useState(false);

  useEffect(() => { setMounted(true); }, []);

  useEffect(() => {
    if (mounted && isLoggedIn) loadTab(sidebar);
  }, [sidebar, mounted, isLoggedIn]);

  const showToast = (text: string, type = "success") => {
    setToast({ text, type });
    setTimeout(() => setToast({ text: "", type: "" }), 3000);
  };

  const loadTab = async (t: string) => {
    setLoading(true);
    try {
      const endpoints: Record<string, string> = {
        faculties: "/faculties",
        departments: "/departments",
        news: "/news",
        faqs: "/faqs",
        exams: "/exam",
        questions: "/question-bank/questions?limit=200",
        results: "/exam/results/all",
        notifications: "/notifications/events",
        kankor: "/kankor/cutoffs",
      };
      if (t === "dashboard") {
        const [fac, dept, exam, qb, news, faq] = await Promise.all([
          adminApi.list("/faculties"),
          adminApi.list("/departments"),
          adminApi.list("/exam"),
          adminApi.list("/question-bank/stats"),
          adminApi.list("/news"),
          adminApi.list("/faqs"),
        ]);
        setData({ faculties: fac, departments: dept, exams: exam, questionBank: qb, news: news, faqs: faq });
      } else if (endpoints[t]) {
        const items = await adminApi.list(endpoints[t]);
        setData({ items: Array.isArray(items) ? items : [] });
      }
    } catch (e) { showToast("خطا در بارگذاری", "error"); }
    setLoading(false);
  };

  const openCreate = (type: string) => { setEditItem(null); setModalType(type); setFormData(getDefaults(type)); setShowModal(true); };
  const openEdit = (type: string, item: any) => { setEditItem(item); setModalType(type); setFormData(item); setShowModal(true); };
  const getDefaults = (t: string) => ({
    faculties: { name_fa: "", slug: "", description_fa: "" },
    departments: { name_fa: "", slug: "", description_fa: "", department_type: "degree", duration_years: 4 },
    news: { title_fa: "", body_fa: "", is_published: false },
    faqs: { question_fa: "", answer_fa: "", category: "" },
    exams: { title_fa: "", category: "kankor", duration_minutes: 60, total_questions: 10, passing_score: 50 },
    kankor: { year: 1404, min_score: 200, capacity: 50 },
  }[t] || {});

  const handleSave = async () => {
    try {
      if (editItem) { await adminApi.update(`/${modalType}/${editItem.id || editItem.slug}`, formData); showToast("ویرایش شد"); }
      else { await adminApi.create(`/${modalType}`, formData); showToast("ایجاد شد"); }
      setShowModal(false); loadTab(sidebar);
    } catch (e) { showToast("خطا در ذخیره", "error"); }
  };

  const handleDelete = async (type: string, id: string) => {
    if (!confirm("آیا مطمئن هستید؟")) return;
    try { await adminApi.delete(`/${type}/${id}`); showToast("حذف شد"); loadTab(sidebar); }
    catch (e) { showToast("خطا در حذف", "error"); }
  };

  const handleReindex = async () => {
    try {
      const token = localStorage.getItem("admin_access");
      const r = await fetch(`${API}/admin/rag/reindex`, { method: "POST", headers: { "Authorization": `Bearer ${token}` } });
      const d = await r.json();
      showToast(`بازسازی: ${d.chunks_created || 0} chunk`);
    } catch (e) { showToast("خطا", "error"); }
  };

  // Login
  if (!isLoggedIn) {
    return (
      <>
        <Header />
        <main className="flex-1 flex items-center justify-center py-12 bg-surface min-h-screen">
          <div className="w-full max-w-md">
            <div className="bg-surface-card rounded-xl shadow-lg p-8 border border-border">
              <h1 className="text-2xl font-bold text-center mb-6 text-foreground">ورود به پنل مدیریت</h1>
              {toast.text && <div className={`p-3 rounded-lg mb-4 text-sm ${toast.type === "error" ? "bg-danger/10 text-danger" : "bg-success/10 text-success"}`}>{toast.text}</div>}
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-muted mb-1">ایمیل</label>
                  <input type="email" value={loginForm.email} onChange={(e) => setLoginForm({ ...loginForm, email: e.target.value })} className="w-full px-4 py-3 border border-border rounded-[10px] bg-surface text-foreground focus:ring-2 focus:ring-primary-500" placeholder="admin@herat-uni.edu.af" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-muted mb-1">رمز عبور</label>
                  <input type="password" value={loginForm.password} onChange={(e) => setLoginForm({ ...loginForm, password: e.target.value })} className="w-full px-4 py-3 border border-border rounded-[10px] bg-surface text-foreground focus:ring-2 focus:ring-primary-500" placeholder="رمز عبور" />
                </div>
                <button onClick={async () => { try { await adminApi.login(loginForm.email, loginForm.password); setIsLoggedIn(true); showToast("ورود موفق"); } catch (e) { showToast("ایمیل یا رمز اشتباه", "error"); } }} className="w-full py-3 bg-primary-600 text-white rounded-[10px] font-medium hover:bg-primary-700 transition-colors min-h-[44px]">
                  ورود
                </button>
              </div>
            </div>
          </div>
        </main>
        <Footer />
      </>
    );
  }

  const menuGroups = [
    { title: "محتوا", items: [
      { id: "faculties", icon: "📚", label: "پوهنځی‌ها" },
      { id: "departments", icon: "🎓", label: "دیپارتمنت‌ها" },
      { id: "news", icon: "📰", label: "اخبار" },
      { id: "faqs", icon: "❓", label: "FAQ" },
    ]},
    { title: "کانکور", items: [
      { id: "kankor", icon: "📊", label: "کات‌آف" },
      { id: "exams", icon: "📝", label: "امتحانات" },
      { id: "questions", icon: "🧩", label: "بانک سوالات" },
      { id: "results", icon: "🏆", label: "نتایج" },
    ]},
    { title: "سیستم", items: [
      { id: "notifications", icon: "📅", label: "رویدادها" },
    ]},
  ];

  const items = data.items || [];

  // Filter items by search
  const filtered = search ? items.filter((item: any) => {
    const s = search.toLowerCase();
    return JSON.stringify(item).toLowerCase().includes(s);
  }) : items;

  // Group departments by faculty
  const groupedDepts = sidebar === "departments" ? (() => {
    const groups: Record<string, any[]> = {};
    filtered.forEach((d: any) => {
      const facName = data.faculties?.find((f: any) => f.id === d.faculty_id)?.name_fa || "نامعلوم";
      if (!groups[facName]) groups[facName] = [];
      groups[facName].push(d);
    });
    return groups;
  })() : null;

  const canCreate = !["questions", "results", "exams"].includes(sidebar);

  return (
    <>
      <Header />
      <div className="flex min-h-screen bg-surface">
        {/* Sidebar */}
        <aside className="w-64 bg-primary-900 text-white flex-shrink-0 hidden md:block">
          <div className="p-4 border-b border-primary-700">
            <h2 className="font-bold text-lg">پنل مدیریت</h2>
          </div>
          <nav className="p-2">
            {menuGroups.map((group) => (
              <div key={group.title} className="mb-4">
                <div className="px-3 py-2 text-xs text-primary-300 uppercase">{group.title}</div>
                {group.items.map((item) => (
                  <button key={item.id} onClick={() => setSidebar(item.id)} className={`w-full text-right px-3 py-2 rounded-lg text-sm transition-all flex items-center gap-2 ${sidebar === item.id ? "bg-primary-700 text-white" : "text-primary-200 hover:bg-primary-800"}`}>
                    <span>{item.icon}</span> {item.label}
                  </button>
                ))}
              </div>
            ))}
          </nav>
          <div className="p-2 border-t border-primary-700">
            <button onClick={handleReindex} className="w-full px-3 py-2 bg-accent-500 text-white rounded-lg text-sm hover:bg-accent-600">🤖 بازسازی دانش</button>
            <button onClick={() => { localStorage.clear(); setIsLoggedIn(false); }} className="w-full px-3 py-2 text-primary-300 hover:text-white text-sm mt-2">خروج</button>
          </div>
        </aside>

        {/* Main */}
        <main className="flex-1 p-6 overflow-auto">
          {/* Toast */}
          {toast.text && <div className={`fixed top-20 left-1/2 -translate-x-1/2 z-50 px-6 py-3 rounded-lg shadow-lg text-sm font-medium ${toast.type === "error" ? "bg-danger text-white" : "bg-success text-white"}`}>{toast.text}</div>}

          {/* Header */}
          <div className="flex items-center justify-between mb-6">
            <h1 className="text-xl font-bold text-foreground">{menuGroups.flatMap(g => g.items).find(i => i.id === sidebar)?.label || "داشبورد"}</h1>
            <div className="flex gap-2 items-center">
              <input type="text" value={search} onChange={(e) => setSearch(e.target.value)} placeholder="جستجو..." className="px-3 py-2 border border-border rounded-[10px] bg-surface text-foreground text-sm w-48 focus:ring-2 focus:ring-primary-500" />
              {canCreate && <button onClick={() => openCreate(sidebar)} className="px-4 py-2 bg-primary-600 text-white rounded-[10px] text-sm hover:bg-primary-700 min-h-[44px]">+ افزودن</button>}
            </div>
          </div>

          {/* Content */}
          {loading ? (
            <div className="text-center py-12 text-muted">در حال بارگذاری...</div>
          ) : (
            <div className="bg-surface-card rounded-xl shadow-sm border border-border p-6">
              {/* Dashboard */}
              {sidebar === "dashboard" && (
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  {[["پوهنځی‌ها", data.faculties?.length || 0], ["دیپارتمنت‌ها", data.departments?.length || 0], ["امتحانات", data.exams?.length || 0], ["اخبار", data.news?.length || 0], ["FAQ", data.faqs?.length || 0], ["سوالات بانک", data.questionBank?.total || 0]].map(([l, v]) => (
                    <div key={String(l)} className="bg-surface rounded-[16px] p-4 text-center border border-border">
                      <div className="text-3xl font-bold text-primary-600">{v}</div>
                      <div className="text-muted text-sm mt-1">{String(l)}</div>
                    </div>
                  ))}
                </div>
              )}

              {/* Grouped Departments */}
              {sidebar === "departments" && groupedDepts && (
                <div className="space-y-4">
                  {Object.entries(groupedDepts).map(([facName, depts]) => (
                    <div key={facName} className="border border-border rounded-[16px] overflow-hidden">
                      <div className="bg-primary-50 px-4 py-3 flex items-center justify-between">
                        <h3 className="font-bold text-foreground">{facName} — {depts.length} دیپارتمنت</h3>
                      </div>
                      <div className="divide-y divide-border">
                        {depts.map((d: any) => (
                          <div key={d.id} className="px-4 py-3 flex items-center justify-between hover:bg-surface">
                            <div className="flex items-center gap-3">
                              <span className="font-medium text-foreground">{d.name_fa}</span>
                              <span className={`px-2 py-1 rounded text-xs ${d.department_type === "degree" ? "bg-success/10 text-success" : "bg-muted/10 text-muted"}`}>{d.department_type === "degree" ? "فارغ‌ده" : "خدماتی"}</span>
                            </div>
                            <div className="flex gap-2">
                              <button onClick={() => openEdit("departments", d)} className="text-primary-600 hover:underline text-sm">ویرایش</button>
                              <button onClick={() => handleDelete("departments", d.id)} className="text-danger hover:underline text-sm">حذف</button>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              )}

              {/* Generic Tables */}
              {sidebar !== "dashboard" && sidebar !== "departments" && (
                <div>
                  <h3 className="font-bold mb-4 text-foreground">{filtered.length} ردیف</h3>
                  {filtered.length === 0 ? (
                    <p className="text-muted text-center py-8">داده‌ای موجود نیست</p>
                  ) : (
                    <div className="overflow-x-auto">
                      <table className="w-full text-sm border-collapse">
                        <thead>
                          <tr className="bg-surface border-b border-border">
                            {sidebar === "faculties" && <><th className="text-right p-3 text-muted">نام</th><th className="text-right p-3 text-muted">Slug</th><th className="text-right p-3 text-muted">عملیات</th></>}
                            {sidebar === "news" && <><th className="text-right p-3 text-muted">عنوان</th><th className="text-right p-3 text-muted">وضعیت</th><th className="text-right p-3 text-muted">عملیات</th></>}
                            {sidebar === "faqs" && <><th className="text-right p-3 text-muted">سوال</th><th className="text-right p-3 text-muted">دسته</th><th className="text-right p-3 text-muted">عملیات</th></>}
                            {sidebar === "exams" && <><th className="text-right p-3 text-muted">عنوان</th><th className="text-right p-3 text-muted">سوالات</th><th className="text-right p-3 text-muted">مدت</th><th className="text-right p-3 text-muted">عملیات</th></>}
                            {sidebar === "questions" && <><th className="text-right p-3 text-muted">موضوع</th><th className="text-right p-3 text-muted">سطح</th><th className="text-right p-3 text-muted">سوال</th></>}
                            {sidebar === "results" && <><th className="text-right p-3 text-muted">نمره</th><th className="text-right p-3 text-muted">درست</th><th className="text-right p-3 text-muted">وضعیت</th></>}
                            {sidebar === "notifications" && <><th className="text-right p-3 text-muted">عنوان</th><th className="text-right p-3 text-muted">تاریخ</th><th className="text-right p-3 text-muted">عملیات</th></>}
                            {sidebar === "kankor" && <><th className="text-right p-3 text-muted">سال</th><th className="text-right p-3 text-muted">نمره</th><th className="text-right p-3 text-muted">ظرفیت</th><th className="text-right p-3 text-muted">عملیات</th></>}
                          </tr>
                        </thead>
                        <tbody>
                          {filtered.map((item: any) => (
                            <tr key={item.id || item.slug} className="border-b border-border hover:bg-surface">
                              {sidebar === "faculties" && <><td className="p-3 font-medium text-foreground">{item.name_fa}</td><td className="p-3 text-muted">{item.slug}</td><td className="p-3"><button onClick={() => openEdit("faculties", item)} className="text-primary-600 hover:underline text-sm ml-2">ویرایش</button><button onClick={() => handleDelete("faculties", item.id)} className="text-danger hover:underline text-sm">حذف</button></td></>}
                              {sidebar === "news" && <><td className="p-3 text-foreground">{item.title_fa}</td><td className="p-3"><span className={`px-2 py-1 rounded text-xs ${item.is_published ? "bg-success/10 text-success" : "bg-warning/10 text-warning"}`}>{item.is_published ? "منتشر" : "پیش‌نویس"}</span></td><td className="p-3"><button onClick={() => openEdit("news", item)} className="text-primary-600 hover:underline text-sm ml-2">ویرایش</button><button onClick={() => handleDelete("news", item.id)} className="text-danger hover:underline text-sm">حذف</button></td></>}
                              {sidebar === "faqs" && <><td className="p-3 text-foreground">{item.question_fa}</td><td className="p-3 text-muted">{item.category || "-"}</td><td className="p-3"><button onClick={() => openEdit("faqs", item)} className="text-primary-600 hover:underline text-sm ml-2">ویرایش</button><button onClick={() => handleDelete("faqs", item.id)} className="text-danger hover:underline text-sm">حذف</button></td></>}
                              {sidebar === "exams" && <><td className="p-3 font-medium text-foreground">{item.title_fa}</td><td className="p-3 text-foreground">{item.total_questions}</td><td className="p-3 text-foreground">{item.duration_minutes} دقیقه</td><td className="p-3"><button onClick={() => openEdit("exams", item)} className="text-primary-600 hover:underline text-sm ml-2">ویرایش</button><button onClick={() => handleDelete("exams", item.id)} className="text-danger hover:underline text-sm">حذف</button></td></>}
                              {sidebar === "questions" && <><td className="p-3"><span className="px-2 py-1 rounded text-xs bg-primary-100 text-primary-700">{item.subject}</span></td><td className="p-3"><span className={`px-2 py-1 rounded text-xs ${item.difficulty === "easy" ? "bg-success/10 text-success" : item.difficulty === "hard" ? "bg-danger/10 text-danger" : "bg-warning/10 text-warning"}`}>{item.difficulty}</span></td><td className="p-3 text-foreground max-w-md truncate">{item.question_fa}</td></>}
                              {sidebar === "results" && <><td className="p-3 font-bold text-foreground">{item.score}%</td><td className="p-3 text-success">{item.correct_answers}/{item.total_answers}</td><td className="p-3"><span className={`px-2 py-1 rounded text-xs ${item.passed ? "bg-success/10 text-success" : "bg-danger/10 text-danger"}`}>{item.passed ? "قبول" : "مردود"}</span></td></>}
                              {sidebar === "notifications" && <><td className="p-3 text-foreground">{item.title_fa}</td><td className="p-3 text-muted">{new Date(item.event_date).toLocaleDateString("fa-AF")}</td><td className="p-3"><button onClick={() => handleDelete("notifications/events", item.id)} className="text-danger hover:underline text-sm">حذف</button></td></>}
                              {sidebar === "kankor" && <><td className="p-3 text-foreground">{item.year}</td><td className="p-3 text-foreground">{item.min_score}</td><td className="p-3 text-foreground">{item.capacity}</td><td className="p-3"><button onClick={() => handleDelete("kankor/cutoffs", item.id)} className="text-danger hover:underline text-sm">حذف</button></td></>}
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  )}
                </div>
              )}
            </div>
          )}
        </main>
      </div>

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-surface-card rounded-xl shadow-xl max-w-lg w-full max-h-[90vh] overflow-y-auto border border-border">
            <div className="p-6">
              <h3 className="text-lg font-bold mb-4 text-foreground">{editItem ? "ویرایش" : "افزودن"} {modalType}</h3>
              <div className="space-y-4">
                {Object.entries(formData).map(([key, value]) => (
                  <div key={key}>
                    <label className="block text-sm font-medium text-muted mb-1">{key}</label>
                    {typeof value === "boolean" ? (
                      <input type="checkbox" checked={value as boolean} onChange={(e) => setFormData({ ...formData, [key]: e.target.checked })} className="w-4 h-4" />
                    ) : typeof value === "string" && value.length > 100 ? (
                      <textarea value={value as string} onChange={(e) => setFormData({ ...formData, [key]: e.target.value })} className="w-full px-3 py-2 border border-border rounded-[10px] text-sm bg-surface text-foreground" rows={4} />
                    ) : (
                      <input type="text" value={String(value)} onChange={(e) => setFormData({ ...formData, [key]: e.target.value })} className="w-full px-3 py-2 border border-border rounded-[10px] text-sm bg-surface text-foreground" />
                    )}
                  </div>
                ))}
              </div>
              <div className="flex gap-3 mt-6">
                <button onClick={handleSave} className="flex-1 py-2 bg-primary-600 text-white rounded-[10px] hover:bg-primary-700 min-h-[44px]">{editItem ? "ذخیره" : "ایجاد"}</button>
                <button onClick={() => setShowModal(false)} className="flex-1 py-2 bg-surface border border-border text-foreground rounded-[10px] hover:bg-border min-h-[44px]">انصراف</button>
              </div>
            </div>
          </div>
        </div>
      )}
      <Footer />
    </>
  );
}
