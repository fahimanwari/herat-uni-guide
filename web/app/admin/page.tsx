"use client";

import { useState, useEffect, useCallback } from "react";
import { Header } from "../components/layout/Header";
import { Footer } from "../components/layout/Footer";
import { adminApi } from "../lib/adminApi";
import { API_BASE } from "../lib/config";

const API = API_BASE;

// --- Menu ---
const menuGroups = [
  { title: "محتوا", items: [
    { id: "faculties", icon: "📚", label: "پوهنځی‌ها" },
    { id: "departments", icon: "🎓", label: "دیپارتمنت‌ها" },
    { id: "news", icon: "📰", label: "اخبار" },
    { id: "faqs", icon: "❓", label: "FAQ" },
    { id: "guides", icon: "📖", label: "راهنمای کانکور" },
  ]},
  { title: "کانکور", items: [
    { id: "kankor", icon: "📊", label: "کات‌آف" },
    { id: "exams", icon: "📝", label: "امتحانات" },
    { id: "questions", icon: "🧩", label: "بانک سوالات" },
    { id: "results", icon: "🏆", label: "نتایج" },
  ]},
  { title: "آزمون رشته", items: [
    { id: "quiz-questions", icon: "🎯", label: "سوالات آزمون" },
    { id: "quiz-profiles", icon: "👤", label: "پروفایل صفات" },
  ]},
  { title: "سیستم", items: [
    { id: "notifications", icon: "📅", label: "رویدادها" },
    { id: "users", icon: "👥", label: "کاربران" },
    { id: "ai-logs", icon: "🤖", label: "لاگ چت AI" },
  ]},
];

const PAGE_SIZE = 20;

// --- Defaults ---
function getDefaults(t: string): any {
  const defaults: Record<string, any> = {
    faculties: { name_fa: "", slug: "", description_fa: "" },
    departments: { name_fa: "", slug: "", description_fa: "", department_type: "degree", duration_years: 4 },
    news: { title_fa: "", body_fa: "", is_published: false },
    faqs: { question_fa: "", answer_fa: "", category: "" },
    guides: { title_fa: "", body_fa: "", category: "", sort_order: 0 },
    exams: { title_fa: "", category: "kankor", duration_minutes: 60, total_questions: 10, passing_score: 50 },
    kankor: { year: 1404, min_score: 200, capacity: 50 },
    "quiz-questions": { question_fa: "", category: "", sort_order: 0, options: [] },
    "quiz-profiles": { department_id: "", trait_weights: { logic: 0, biology: 0, language: 0, art: 0, social: 0, handson: 0 } },
    notifications: { title_fa: "", event_date: "", event_type: "kankor", remind_days_before: 7, is_active: true },
  };
  return defaults[t] || {};
}

// --- Helpers ---
function getName(item: any, type: string): string {
  if (type === "faculties") return item.name_fa || "";
  if (type === "departments") return item.name_fa || "";
  if (type === "news") return item.title_fa || "";
  if (type === "faqs") return item.question_fa || "";
  if (type === "guides") return item.title_fa || "";
  if (type === "exams") return item.title_fa || "";
  if (type === "kankor") return `کات‌آف سال ${item.year}`;
  if (type === "users") return item.full_name || item.email || "";
  if (type === "notifications") return item.title_fa || "";
  if (type === "quiz-questions") return item.question_fa || "";
  if (type === "quiz-profiles") return item.department_id || "";
  return "";
}

function getDeleteEndpoint(type: string, item: any): string {
  if (type === "kankor") return `/kankor/cutoffs/${item.id}`;
  if (type === "notifications") return `/notifications/events/${item.id}`;
  if (type === "quiz-questions") return `/quiz/questions/${item.id}`;
  if (type === "quiz-profiles") return `/quiz/profiles/${item.id}`;
  return `/${type}/${item.id || item.slug}`;
}

function canCreateNew(type: string): boolean {
  return !["questions", "results", "ai-logs", "users"].includes(type);
}

export default function AdminPage() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [sidebar, setSidebar] = useState("dashboard");
  const [sidebarOpen, setSidebarOpen] = useState(false);
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
  const [page, setPage] = useState(1);
  const [deleteConfirm, setDeleteConfirm] = useState<{ type: string; id: string; name: string } | null>(null);
  const [subDept, setSubDept] = useState<any>(null);
  const [subTab, setSubTab] = useState<"projects" | "alumni" | "roadmaps">("projects");
  const [subItems, setSubItems] = useState<any[]>([]);
  const [subLoading, setSubLoading] = useState(false);
  const [subForm, setSubForm] = useState<any>(null);
  const [sortCol, setSortCol] = useState<string | null>(null);
  const [sortDir, setSortDir] = useState<"asc" | "desc">("asc");

  // --- Question bank: dedicated create/edit modal (options need custom UI) ---
  const [showQuestionModal, setShowQuestionModal] = useState(false);
  const [questionEditItem, setQuestionEditItem] = useState<any>(null);
  const [questionForm, setQuestionForm] = useState<any>(null);
  const [questionSaving, setQuestionSaving] = useState(false);

  // --- Question bank: bulk JSON import ---
  const [showImportModal, setShowImportModal] = useState(false);
  const [importText, setImportText] = useState("");
  const [importErrors, setImportErrors] = useState<{ row: number; message: string }[]>([]);
  const [importBusy, setImportBusy] = useState(false);

  useEffect(() => { setMounted(true); }, []);

  useEffect(() => {
    if (mounted && isLoggedIn) {
      setPage(1);
      setSortCol(null);
      setSortDir("asc");
      loadTab(sidebar);
    }
  }, [sidebar, mounted, isLoggedIn]);

  const showToast = useCallback((text: string, type = "success") => {
    setToast({ text, type });
    setTimeout(() => setToast({ text: "", type: "" }), 3000);
  }, []);

  const loadTab = async (t: string) => {
    setLoading(true);
    try {
      const endpoints: Record<string, string> = {
        faculties: "/faculties",
        departments: "/departments",
        news: "/news",
        faqs: "/faqs",
        guides: "/kankor/guides",
        exams: "/exam",
        questions: "/question-bank/questions?limit=200",
        results: "/exam/results/all",
        notifications: "/notifications/events",
        kankor: "/kankor/cutoffs",
        "quiz-questions": "/quiz/questions",
        "quiz-profiles": "/quiz/profiles",
        users: "/users/admin/list",
        "ai-logs": "/admin/ai/logs?page=1&limit=20",
      };
      if (t === "dashboard") {
        const [fac, dept, exam, qb, news, faq, cutoffs, aiStatus, aiLogs] = await Promise.allSettled([
          adminApi.list("/faculties"),
          adminApi.list("/departments"),
          adminApi.list("/exam"),
          adminApi.list("/question-bank/stats"),
          adminApi.list("/news"),
          adminApi.list("/faqs"),
          adminApi.list("/kankor/cutoffs"),
          adminApi.list("/admin/ai/status"),
          adminApi.list("/admin/ai/logs?page=1&limit=5"),
        ]);
        setData({
          faculties: fac.status === "fulfilled" ? fac.value : [],
          departments: dept.status === "fulfilled" ? dept.value : [],
          exams: exam.status === "fulfilled" ? exam.value : [],
          questionBank: qb.status === "fulfilled" ? qb.value : {},
          news: news.status === "fulfilled" ? news.value : [],
          faqs: faq.status === "fulfilled" ? faq.value : [],
          cutoffs: cutoffs.status === "fulfilled" ? cutoffs.value : [],
          aiStatus: aiStatus.status === "fulfilled" ? aiStatus.value : null,
          aiLogs: aiLogs.status === "fulfilled" ? aiLogs.value : [],
        });
      } else if (endpoints[t]) {
        const items = await adminApi.list(endpoints[t]);
        setData({ items: Array.isArray(items) ? items : [] });
      }
    } catch (e: any) {
      showToast(e?.message || "خطا در بارگذاری", "error");
    }
    setLoading(false);
  };

  const openCreate = (type: string) => { setEditItem(null); setModalType(type); setFormData(getDefaults(type)); setShowModal(true); };
  const openEdit = (type: string, item: any) => { setEditItem(item); setModalType(type); setFormData(item); setShowModal(true); };

  const handleSave = async () => {
    try {
      if (editItem) {
        const res = await adminApi.update(getDeleteEndpoint(modalType, editItem), formData);
        showToast("ویرایش شد");
      } else {
        const res = await adminApi.create(`/${modalType}`, formData);
        showToast("ایجاد شد");
      }
      setShowModal(false);
      loadTab(sidebar);
    } catch (e: any) {
      const msg = e?.message || "خطا در ذخیره";
      showToast(msg.includes("Failed") ? `خطا: ${msg}` : msg, "error");
    }
  };

  const handleDelete = async () => {
    if (!deleteConfirm) return;
    try {
      await adminApi.delete(`/${deleteConfirm.type}/${deleteConfirm.id}`);
      showToast(`«${deleteConfirm.name}» حذف شد`);
      setDeleteConfirm(null);
      loadTab(sidebar);
    } catch (e: any) {
      showToast(e?.message || "خطا در حذف", "error");
      setDeleteConfirm(null);
    }
  };

  const confirmDelete = (type: string, id: string, name: string) => {
    setDeleteConfirm({ type, id, name });
  };

  const handleReindex = async () => {
    try {
      const token = localStorage.getItem("admin_access");
      const r = await fetch(`${API}/admin/ai/reindex`, { method: "POST", headers: { "Authorization": `Bearer ${token}` } });
      const d = await r.json();
      showToast(`بازسازی: ${d.chunks_created || 0} chunk`);
    } catch { showToast("خطا در بازسازی", "error"); }
  };

  // --- Question bank: dedicated modal ---
  const defaultQuestionForm = () => ({
    subject: "",
    difficulty: "medium",
    question_fa: "",
    year: "",
    grade: "",
    chapter: "",
    source: "",
    explanation_fa: "",
    is_verified: false,
    options: [
      { text: "", is_correct: true },
      { text: "", is_correct: false },
      { text: "", is_correct: false },
      { text: "", is_correct: false },
    ],
  });

  const openQuestionCreate = () => {
    setQuestionEditItem(null);
    setQuestionForm(defaultQuestionForm());
    setShowQuestionModal(true);
  };

  const openQuestionEdit = (item: any) => {
    setQuestionEditItem(item);
    setQuestionForm({
      subject: item.subject || "",
      difficulty: item.difficulty || "medium",
      question_fa: item.question_fa || "",
      year: item.year ?? "",
      grade: item.grade ?? "",
      chapter: item.chapter ?? "",
      source: item.source ?? "",
      explanation_fa: item.explanation_fa ?? "",
      is_verified: !!item.is_verified,
      options: item.options && item.options.length >= 2
        ? item.options.map((o: any) => ({ text: o.text || "", is_correct: !!o.is_correct }))
        : defaultQuestionForm().options,
    });
    setShowQuestionModal(true);
  };

  const setOptionText = (i: number, text: string) => {
    setQuestionForm((f: any) => ({ ...f, options: f.options.map((o: any, idx: number) => idx === i ? { ...o, text } : o) }));
  };
  const setCorrectOption = (i: number) => {
    setQuestionForm((f: any) => ({ ...f, options: f.options.map((o: any, idx: number) => ({ ...o, is_correct: idx === i })) }));
  };
  const addOption = () => {
    setQuestionForm((f: any) => f.options.length >= 6 ? f : { ...f, options: [...f.options, { text: "", is_correct: false }] });
  };
  const removeOption = (i: number) => {
    setQuestionForm((f: any) => {
      if (f.options.length <= 2) return f;
      const options = f.options.filter((_: any, idx: number) => idx !== i);
      if (!options.some((o: any) => o.is_correct)) options[0].is_correct = true;
      return { ...f, options };
    });
  };

  const handleQuestionSave = async () => {
    const opts = questionForm.options.filter((o: any) => o.text.trim() !== "");
    if (!questionForm.subject.trim()) { showToast("موضوع الزامی است", "error"); return; }
    if (!questionForm.question_fa.trim()) { showToast("متن سوال الزامی است", "error"); return; }
    if (opts.length < 2) { showToast("حداقل ۲ گزینه با متن لازم است", "error"); return; }
    if (!opts.some((o: any) => o.is_correct)) { showToast("یک گزینه باید به‌عنوان جواب درست انتخاب شود", "error"); return; }

    const payload: any = {
      subject: questionForm.subject.trim(),
      difficulty: questionForm.difficulty,
      question_fa: questionForm.question_fa.trim(),
      options: opts,
      source: questionForm.source?.trim() || null,
      year: questionForm.year ? Number(questionForm.year) : null,
      grade: questionForm.grade || null,
      chapter: questionForm.chapter?.trim() || null,
      explanation_fa: questionForm.explanation_fa?.trim() || null,
      is_verified: !!questionForm.is_verified,
    };

    setQuestionSaving(true);
    try {
      if (questionEditItem) {
        await adminApi.update(`/question-bank/questions/${questionEditItem.id}`, { id: questionEditItem.id, ...payload });
        showToast("سوال ویرایش شد");
      } else {
        await adminApi.create("/question-bank/questions", payload);
        showToast("سوال ایجاد شد");
      }
      setShowQuestionModal(false);
      loadTab(sidebar);
    } catch (e: any) {
      showToast(e?.message || "خطا در ذخیره سوال", "error");
    }
    setQuestionSaving(false);
  };

  // --- Question bank: bulk JSON import ---
  const handleImportFile = (file: File) => {
    const reader = new FileReader();
    reader.onload = () => setImportText(String(reader.result || ""));
    reader.readAsText(file, "utf-8");
  };

  const handleImport = async () => {
    setImportErrors([]);
    let parsed: any;
    try {
      parsed = JSON.parse(importText);
    } catch {
      showToast("JSON نامعتبر است — فرمت فایل را بررسی کنید", "error");
      return;
    }
    if (!Array.isArray(parsed)) parsed = [parsed];
    if (parsed.length === 0) {
      showToast("هیچ سوالی در فایل نیست", "error");
      return;
    }

    setImportBusy(true);
    try {
      const result = await adminApi.create("/question-bank/import", parsed);
      if (result.errors && result.errors.length > 0) {
        setImportErrors(result.errors);
        showToast(`${result.errors.length} ردیف خطا دارد — هیچ سوالی ذخیره نشد (همه یا هیچ)`, "error");
      } else {
        showToast(`✅ ${result.imported} سوال با موفقیت وارد شد`);
        setShowImportModal(false);
        setImportText("");
        loadTab(sidebar);
      }
    } catch (e: any) {
      showToast(e?.message || "خطا در درون‌ریزی", "error");
    }
    setImportBusy(false);
  };

  // --- Sub-items (projects, alumni, roadmaps) ---
  const openSubDept = async (dept: any) => {
    setSubDept(dept);
    setSubTab("projects");
    setSubItems([]);
    setSubForm(null);
    await loadSubItems(dept.slug, "projects");
  };

  const loadSubItems = async (slug: string, tab: string) => {
    setSubLoading(true);
    try {
      const dept = await adminApi.get(`/departments/${slug}`);
      if (tab === "projects") setSubItems(dept.student_projects || []);
      else if (tab === "alumni") setSubItems(dept.alumni_stories || []);
      else if (tab === "roadmaps") setSubItems(dept.career_roadmaps || []);
    } catch { showToast("خطا در بارگذاری", "error"); }
    setSubLoading(false);
  };

  const handleSubSave = async () => {
    if (!subDept || !subForm) return;
    try {
      const endpoint = `/departments/${subDept.slug}/${subTab === "projects" ? "projects" : subTab === "alumni" ? "alumni" : "roadmaps"}`;
      await adminApi.create(endpoint, subForm);
      showToast("ایجاد شد");
      setSubForm(null);
      await loadSubItems(subDept.slug, subTab);
    } catch (e: any) { showToast(e?.message || "خطا", "error"); }
  };

  const handleSubDelete = async (itemId: string) => {
    if (!subDept) return;
    try {
      await adminApi.delete(`/departments/${subDept.slug}/${subTab === "projects" ? "projects" : subTab === "alumni" ? "alumni" : "roadmaps"}/${itemId}`);
      showToast("حذف شد");
      await loadSubItems(subDept.slug, subTab);
    } catch (e: any) { showToast(e?.message || "خطا", "error"); }
  };

  // --- Login ---
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
                <button onClick={async () => { try { await adminApi.login(loginForm.email, loginForm.password); setIsLoggedIn(true); showToast("ورود موفق"); } catch { showToast("ایمیل یا رمز اشتباه", "error"); } }} className="w-full py-3 bg-primary-600 text-white rounded-[10px] font-medium hover:bg-primary-700 transition-colors min-h-[44px]">
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

  const items = data.items || [];
  const filtered = search ? items.filter((item: any) => JSON.stringify(item).toLowerCase().includes(search.toLowerCase())) : items;

  // Sort
  const sorted = sortCol ? [...filtered].sort((a: any, b: any) => {
    const av = a[sortCol] ?? "";
    const bv = b[sortCol] ?? "";
    const cmp = typeof av === "number" ? av - bv : String(av).localeCompare(String(bv), "fa");
    return sortDir === "asc" ? cmp : -cmp;
  }) : filtered;

  const totalPages = Math.ceil(sorted.length / PAGE_SIZE);
  const paginated = sorted.slice((page - 1) * PAGE_SIZE, page * PAGE_SIZE);

  const toggleSort = (col: string) => {
    if (sortCol === col) setSortDir(d => d === "asc" ? "desc" : "asc");
    else { setSortCol(col); setSortDir("asc"); }
  };
  const sortIcon = (col: string) => sortCol === col ? (sortDir === "asc" ? " ▲" : " ▼") : "";

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

  return (
    <>
      <Header />
      <div className="flex min-h-screen bg-surface">
        {/* Mobile sidebar overlay */}
        {sidebarOpen && <div className="fixed inset-0 bg-black/50 z-40 md:hidden" onClick={() => setSidebarOpen(false)} />}

        {/* Sidebar */}
        <aside className={`fixed md:static inset-y-0 right-0 z-50 w-64 bg-primary-900 text-white flex-shrink-0 transform transition-transform duration-200 ${sidebarOpen ? "translate-x-0" : "translate-x-full md:translate-x-0"}`}>
          <div className="p-4 border-b border-primary-700 flex items-center justify-between">
            <h2 className="font-bold text-lg">پنل مدیریت</h2>
            <button onClick={() => setSidebarOpen(false)} className="md:hidden text-primary-300 hover:text-white">✕</button>
          </div>
          <nav className="p-2 overflow-y-auto max-h-[calc(100vh-160px)]">
            <button onClick={() => { setSidebar("dashboard"); setSidebarOpen(false); }} className={`w-full text-right px-3 py-2 rounded-lg text-sm transition-all flex items-center gap-2 mb-2 ${sidebar === "dashboard" ? "bg-primary-700 text-white" : "text-primary-200 hover:bg-primary-800"}`}>
              📊 داشبورد
            </button>
            {menuGroups.map((group) => (
              <div key={group.title} className="mb-3">
                <div className="px-3 py-1 text-xs text-primary-400 uppercase">{group.title}</div>
                {group.items.map((item) => (
                  <button key={item.id} onClick={() => { setSidebar(item.id); setSidebarOpen(false); }} className={`w-full text-right px-3 py-2 rounded-lg text-sm transition-all flex items-center gap-2 ${sidebar === item.id ? "bg-primary-700 text-white" : "text-primary-200 hover:bg-primary-800"}`}>
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
        <main className="flex-1 p-4 md:p-6 overflow-auto">
          {/* Toast */}
          {toast.text && <div className={`fixed top-20 left-1/2 -translate-x-1/2 z-50 px-6 py-3 rounded-lg shadow-lg text-sm font-medium ${toast.type === "error" ? "bg-danger text-white" : "bg-success text-white"}`}>{toast.text}</div>}

          {/* Header */}
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-3">
              <button onClick={() => setSidebarOpen(true)} className="md:hidden p-2 bg-primary-600 text-white rounded-lg">☰</button>
              <h1 className="text-xl font-bold text-foreground">{menuGroups.flatMap(g => g.items).find(i => i.id === sidebar)?.label || "داشبورد"}</h1>
            </div>
            <div className="flex gap-2 items-center">
              {sidebar !== "dashboard" && (
                <input type="text" value={search} onChange={(e) => { setSearch(e.target.value); setPage(1); }} placeholder="جستجو..." className="px-3 py-2 border border-border rounded-[10px] bg-surface text-foreground text-sm w-36 md:w-48 focus:ring-2 focus:ring-primary-500" />
              )}
              {canCreateNew(sidebar) && (
                <button onClick={() => openCreate(sidebar)} className="px-4 py-2 bg-primary-600 text-white rounded-[10px] text-sm hover:bg-primary-700 min-h-[44px]">+ افزودن</button>
              )}
              {sidebar === "questions" && (
                <>
                  <button onClick={() => setShowImportModal(true)} className="px-4 py-2 bg-accent-500 text-white rounded-[10px] text-sm hover:bg-accent-600 min-h-[44px]">📥 درون‌ریزی JSON</button>
                  <button onClick={openQuestionCreate} className="px-4 py-2 bg-primary-600 text-white rounded-[10px] text-sm hover:bg-primary-700 min-h-[44px]">+ سوال جدید</button>
                </>
              )}
            </div>
          </div>

          {/* Content */}
          {loading ? (
            <div className="text-center py-12 text-muted">در حال بارگذاری...</div>
          ) : (
            <div className="bg-surface-card rounded-xl shadow-sm border border-border p-4 md:p-6">

              {/* === DASHBOARD === */}
              {sidebar === "dashboard" && (
                <div className="space-y-6">
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    {[["پوهنځی‌ها", data.faculties?.length || 0], ["دیپارتمنت‌ها", data.departments?.length || 0], ["امتحانات", data.exams?.length || 0], ["کات‌آف", data.cutoffs?.length || 0], ["اخبار", data.news?.length || 0], ["FAQ", data.faqs?.length || 0], ["سوالات بانک", data.questionBank?.total || 0]].map(([l, v]) => (
                      <div key={String(l)} className="bg-surface rounded-[16px] p-4 text-center border border-border">
                        <div className="text-3xl font-bold text-primary-600">{v}</div>
                        <div className="text-muted text-sm mt-1">{String(l)}</div>
                      </div>
                    ))}
                  </div>
                  {/* AI Status */}
                  {data.aiStatus && (
                    <div className="bg-surface rounded-[16px] p-4 border border-border">
                      <h3 className="font-bold text-foreground mb-2">وضعیت هوش مصنوعی</h3>
                      <div className="flex gap-4 text-sm">
                        <span className="text-muted">Provider: <strong className="text-foreground">{data.aiStatus.provider}</strong></span>
                        <span className="text-muted">Model: <strong className="text-foreground">{data.aiStatus.model}</strong></span>
                        <span className="text-muted">API Key: <strong className={data.aiStatus.has_api_key ? "text-success" : "text-danger"}>{data.aiStatus.has_api_key ? "موجود" : "ندارد"}</strong></span>
                      </div>
                    </div>
                  )}
                  {/* Recent AI Logs */}
                  {data.aiLogs && data.aiLogs.length > 0 && (
                    <div className="bg-surface rounded-[16px] p-4 border border-border">
                      <h3 className="font-bold text-foreground mb-2">۵ سوال اخیر چت AI</h3>
                      <div className="space-y-2">
                        {data.aiLogs.map((log: any) => (
                          <div key={log.id} className="flex items-start gap-3 text-sm p-2 rounded-lg bg-surface-card border border-border">
                            <span className="text-primary-600 font-medium shrink-0">👤</span>
                            <div className="flex-1 min-w-0">
                              <p className="text-foreground truncate">{log.user_message}</p>
                              <p className="text-muted text-xs truncate">{log.ai_response}</p>
                            </div>
                            {log.was_cached && <span className="text-xs text-accent-500 shrink-0">⚡</span>}
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}

              {/* === DEPARTMENTS (grouped) === */}
              {sidebar === "departments" && groupedDepts && (
                <div className="space-y-4">
                  {Object.entries(groupedDepts).map(([facName, depts]) => {
                    const facId = depts[0]?.faculty_id || "";
                    return (
                      <details key={facName} open className="border border-border rounded-[16px] overflow-hidden group">
                        <summary className="bg-primary-50 px-4 py-3 cursor-pointer flex items-center justify-between hover:bg-primary-100 transition-colors">
                          <div className="flex items-center gap-3">
                            <h3 className="font-bold text-foreground">{facName} — {depts.length} دیپارتمنت</h3>
                            <button onClick={(e) => { e.preventDefault(); setEditItem(null); setModalType("departments"); setFormData({ ...getDefaults("departments"), faculty_id: facId }); setShowModal(true); }} className="px-2 py-1 bg-primary-600 text-white rounded text-xs hover:bg-primary-700">+ دیپارتمنت</button>
                          </div>
                          <span className="text-muted text-sm group-open:rotate-180 transition-transform">▼</span>
                        </summary>
                      <div className="divide-y divide-border">
                        {depts.map((d: any) => (
                          <div key={d.id} className="px-4 py-3 flex items-center justify-between hover:bg-surface">
                            <div className="flex items-center gap-3">
                              <span className="font-medium text-foreground">{d.name_fa}</span>
                              <span className={`px-2 py-1 rounded text-xs ${d.department_type === "degree" ? "bg-success/10 text-success" : "bg-muted/10 text-muted"}`}>{d.department_type === "degree" ? "فارغ‌ده" : "خدماتی"}</span>
                            </div>
                            <div className="flex gap-2">
                              <button onClick={() => openSubDept(d)} className="text-accent-600 hover:underline text-sm">مدیریت</button>
                              <button onClick={() => openEdit("departments", d)} className="text-primary-600 hover:underline text-sm">ویرایش</button>
                              <button onClick={() => confirmDelete("departments", d.id, d.name_fa)} className="text-danger hover:underline text-sm">حذف</button>
                            </div>
                          </div>
                        ))}
                      </div>
                    </details>
                    );
                  })}
                </div>
              )}

              {/* === GENERIC TABLES === */}
              {sidebar !== "dashboard" && sidebar !== "departments" && (
                <div>
                  <div className="flex items-center justify-between mb-4">
                    <span className="text-sm text-muted">{filtered.length} ردیف</span>
                    {totalPages > 1 && (
                      <div className="flex items-center gap-2 text-sm">
                        <button onClick={() => setPage(Math.max(1, page - 1))} disabled={page === 1} className="px-3 py-1 rounded border border-border disabled:opacity-40">قبلی</button>
                        <span className="text-muted">{page} / {totalPages}</span>
                        <button onClick={() => setPage(Math.min(totalPages, page + 1))} disabled={page === totalPages} className="px-3 py-1 rounded border border-border disabled:opacity-40">بعدی</button>
                      </div>
                    )}
                  </div>
                  {paginated.length === 0 ? (
                    <p className="text-muted text-center py-8">داده‌ای موجود نیست</p>
                  ) : (
                    <div className="overflow-x-auto">
                      <table className="w-full text-sm border-collapse">
                        <thead>
                          <tr className="bg-surface border-b border-border">
                            {sidebar === "faculties" && <><th onClick={() => toggleSort("name_fa")} className="text-right p-3 text-muted cursor-pointer hover:text-foreground">نام{sortIcon("name_fa")}</th><th className="text-right p-3 text-muted">Slug</th><th className="text-right p-3 text-muted">عملیات</th></>}
                            {sidebar === "news" && <><th onClick={() => toggleSort("title_fa")} className="text-right p-3 text-muted cursor-pointer hover:text-foreground">عنوان{sortIcon("title_fa")}</th><th className="text-right p-3 text-muted">وضعیت</th><th className="text-right p-3 text-muted">عملیات</th></>}
                            {sidebar === "faqs" && <><th onClick={() => toggleSort("question_fa")} className="text-right p-3 text-muted cursor-pointer hover:text-foreground">سوال{sortIcon("question_fa")}</th><th className="text-right p-3 text-muted">دسته</th><th className="text-right p-3 text-muted">عملیات</th></>}
                            {sidebar === "guides" && <><th onClick={() => toggleSort("title_fa")} className="text-right p-3 text-muted cursor-pointer hover:text-foreground">عنوان{sortIcon("title_fa")}</th><th className="text-right p-3 text-muted">دسته</th><th className="text-right p-3 text-muted">عملیات</th></>}
                            {sidebar === "exams" && <><th onClick={() => toggleSort("title_fa")} className="text-right p-3 text-muted cursor-pointer hover:text-foreground">عنوان{sortIcon("title_fa")}</th><th onClick={() => toggleSort("total_questions")} className="text-right p-3 text-muted cursor-pointer hover:text-foreground">سوالات{sortIcon("total_questions")}</th><th onClick={() => toggleSort("duration_minutes")} className="text-right p-3 text-muted cursor-pointer hover:text-foreground">مدت{sortIcon("duration_minutes")}</th><th className="text-right p-3 text-muted">عملیات</th></>}
                            {sidebar === "questions" && <><th onClick={() => toggleSort("subject")} className="text-right p-3 text-muted cursor-pointer hover:text-foreground">موضوع{sortIcon("subject")}</th><th onClick={() => toggleSort("difficulty")} className="text-right p-3 text-muted cursor-pointer hover:text-foreground">سطح{sortIcon("difficulty")}</th><th className="text-right p-3 text-muted">سوال</th><th onClick={() => toggleSort("year")} className="text-right p-3 text-muted cursor-pointer hover:text-foreground">سال{sortIcon("year")}</th><th onClick={() => toggleSort("is_verified")} className="text-right p-3 text-muted cursor-pointer hover:text-foreground">وضعیت{sortIcon("is_verified")}</th><th className="text-right p-3 text-muted">عملیات</th></>}
                            {sidebar === "results" && <><th onClick={() => toggleSort("score")} className="text-right p-3 text-muted cursor-pointer hover:text-foreground">نمره{sortIcon("score")}</th><th className="text-right p-3 text-muted">درست</th><th className="text-right p-3 text-muted">وضعیت</th></>}
                            {sidebar === "kankor" && <><th onClick={() => toggleSort("year")} className="text-right p-3 text-muted cursor-pointer hover:text-foreground">سال{sortIcon("year")}</th><th onClick={() => toggleSort("min_score")} className="text-right p-3 text-muted cursor-pointer hover:text-foreground">نمره{sortIcon("min_score")}</th><th onClick={() => toggleSort("capacity")} className="text-right p-3 text-muted cursor-pointer hover:text-foreground">ظرفیت{sortIcon("capacity")}</th><th className="text-right p-3 text-muted">عملیات</th></>}
                            {sidebar === "quiz-questions" && <><th onClick={() => toggleSort("question_fa")} className="text-right p-3 text-muted cursor-pointer hover:text-foreground">سوال{sortIcon("question_fa")}</th><th className="text-right p-3 text-muted">دسته</th><th className="text-right p-3 text-muted">عملیات</th></>}
                            {sidebar === "quiz-profiles" && <><th className="text-right p-3 text-muted">شناسه رشته</th><th className="text-right p-3 text-muted">وزن صفات</th><th className="text-right p-3 text-muted">عملیات</th></>}
                            {sidebar === "notifications" && <><th onClick={() => toggleSort("title_fa")} className="text-right p-3 text-muted cursor-pointer hover:text-foreground">عنوان{sortIcon("title_fa")}</th><th onClick={() => toggleSort("event_date")} className="text-right p-3 text-muted cursor-pointer hover:text-foreground">تاریخ{sortIcon("event_date")}</th><th className="text-right p-3 text-muted">عملیات</th></>}
                            {sidebar === "users" && <><th onClick={() => toggleSort("full_name")} className="text-right p-3 text-muted cursor-pointer hover:text-foreground">نام{sortIcon("full_name")}</th><th onClick={() => toggleSort("email")} className="text-right p-3 text-muted cursor-pointer hover:text-foreground">ایمیل{sortIcon("email")}</th><th className="text-right p-3 text-muted">وضعیت</th><th className="text-right p-3 text-muted">عملیات</th></>}
                            {sidebar === "ai-logs" && <><th className="text-right p-3 text-muted">سوال</th><th className="text-right p-3 text-muted">پاسخ</th><th className="text-right p-3 text-muted">کش</th><th onClick={() => toggleSort("created_at")} className="text-right p-3 text-muted cursor-pointer hover:text-foreground">زمان{sortIcon("created_at")}</th></>}
                          </tr>
                        </thead>
                        <tbody>
                          {paginated.map((item: any) => (
                            <tr key={item.id || item.slug} className="border-b border-border hover:bg-surface">
                              {sidebar === "faculties" && <><td className="p-3 font-medium text-foreground">{item.name_fa}</td><td className="p-3 text-muted">{item.slug}</td><td className="p-3"><button onClick={() => openEdit("faculties", item)} className="text-primary-600 hover:underline text-sm ml-2">ویرایش</button><button onClick={() => confirmDelete("faculties", item.id, item.name_fa)} className="text-danger hover:underline text-sm">حذف</button></td></>}
                              {sidebar === "news" && <><td className="p-3 text-foreground">{item.title_fa}</td><td className="p-3"><span className={`px-2 py-1 rounded text-xs ${item.is_published ? "bg-success/10 text-success" : "bg-warning/10 text-warning"}`}>{item.is_published ? "منتشر" : "پیش‌نویس"}</span></td><td className="p-3"><button onClick={() => openEdit("news", item)} className="text-primary-600 hover:underline text-sm ml-2">ویرایش</button><button onClick={() => confirmDelete("news", item.id, item.title_fa)} className="text-danger hover:underline text-sm">حذف</button></td></>}
                              {sidebar === "faqs" && <><td className="p-3 text-foreground">{item.question_fa}</td><td className="p-3 text-muted">{item.category || "-"}</td><td className="p-3"><button onClick={() => openEdit("faqs", item)} className="text-primary-600 hover:underline text-sm ml-2">ویرایش</button><button onClick={() => confirmDelete("faqs", item.id, item.question_fa)} className="text-danger hover:underline text-sm">حذف</button></td></>}
                              {sidebar === "guides" && <><td className="p-3 font-medium text-foreground">{item.title_fa}</td><td className="p-3 text-muted">{item.category || "-"}</td><td className="p-3"><button onClick={() => openEdit("guides", item)} className="text-primary-600 hover:underline text-sm ml-2">ویرایش</button><button onClick={() => confirmDelete("kankor/guides", item.id, item.title_fa)} className="text-danger hover:underline text-sm">حذف</button></td></>}
                              {sidebar === "exams" && <><td className="p-3 font-medium text-foreground">{item.title_fa}</td><td className="p-3 text-foreground">{item.total_questions}</td><td className="p-3 text-foreground">{item.duration_minutes} دقیقه</td><td className="p-3"><button onClick={() => openEdit("exams", item)} className="text-primary-600 hover:underline text-sm ml-2">ویرایش</button><button onClick={() => confirmDelete("exam", item.id, item.title_fa)} className="text-danger hover:underline text-sm">حذف</button></td></>}
                              {sidebar === "questions" && <><td className="p-3"><span className="px-2 py-1 rounded text-xs bg-primary-100 text-primary-700">{item.subject}</span></td><td className="p-3"><span className={`px-2 py-1 rounded text-xs ${item.difficulty === "easy" ? "bg-success/10 text-success" : item.difficulty === "hard" ? "bg-danger/10 text-danger" : "bg-warning/10 text-warning"}`}>{item.difficulty}</span></td><td className="p-3 text-foreground max-w-md truncate">{item.question_fa}</td><td className="p-3 text-muted">{item.year || "-"}</td><td className="p-3"><span className={`px-2 py-1 rounded text-xs ${item.is_verified ? "bg-success/10 text-success" : "bg-warning/10 text-warning"}`}>{item.is_verified ? "تایید شده" : "بازبینی‌نشده"}</span></td><td className="p-3"><button onClick={() => openQuestionEdit(item)} className="text-primary-600 hover:underline text-sm ml-2">ویرایش</button><button onClick={() => confirmDelete("question-bank/questions", item.id, item.question_fa)} className="text-danger hover:underline text-sm">حذف</button></td></>}
                              {sidebar === "results" && <><td className="p-3 font-bold text-foreground">{item.score}%</td><td className="p-3 text-success">{item.correct_answers}/{item.total_answers}</td><td className="p-3"><span className={`px-2 py-1 rounded text-xs ${item.passed ? "bg-success/10 text-success" : "bg-danger/10 text-danger"}`}>{item.passed ? "قبول" : "مردود"}</span></td></>}
                              {sidebar === "kankor" && <><td className="p-3 text-foreground">{item.year}</td><td className="p-3 text-foreground">{item.min_score}</td><td className="p-3 text-foreground">{item.capacity || "-"}</td><td className="p-3"><button onClick={() => confirmDelete("kankor/cutoffs", item.id, `کات‌آف سال ${item.year}`)} className="text-danger hover:underline text-sm">حذف</button></td></>}
                              {sidebar === "quiz-questions" && <><td className="p-3 text-foreground max-w-md truncate">{item.question_fa}</td><td className="p-3 text-muted">{item.category || "-"}</td><td className="p-3"><button onClick={() => openEdit("quiz-questions", item)} className="text-primary-600 hover:underline text-sm ml-2">ویرایش</button><button onClick={() => confirmDelete("quiz/questions", item.id, item.question_fa)} className="text-danger hover:underline text-sm">حذف</button></td></>}
                              {sidebar === "quiz-profiles" && <><td className="p-3 text-foreground font-mono text-xs">{item.department_id?.slice(0, 8)}...</td><td className="p-3 text-muted text-xs">{JSON.stringify(item.trait_weights)}</td><td className="p-3"><button onClick={() => openEdit("quiz-profiles", item)} className="text-primary-600 hover:underline text-sm ml-2">ویرایش</button><button onClick={() => confirmDelete("quiz/profiles", item.id, "پروفایل صفات")} className="text-danger hover:underline text-sm">حذف</button></td></>}
                              {sidebar === "notifications" && <><td className="p-3 text-foreground">{item.title_fa}</td><td className="p-3 text-muted">{item.event_date}</td><td className="p-3"><button onClick={() => confirmDelete("notifications/events", item.id, item.title_fa)} className="text-danger hover:underline text-sm">حذف</button></td></>}
                              {sidebar === "users" && <><td className="p-3 font-medium text-foreground">{item.full_name}</td><td className="p-3 text-muted">{item.email}</td><td className="p-3"><span className={`px-2 py-1 rounded text-xs ${item.is_active ? "bg-success/10 text-success" : "bg-danger/10 text-danger"}`}>{item.is_active ? "فعال" : "غیرفعال"}</span></td><td className="p-3"><button onClick={async () => { await adminApi.update(`/users/admin/${item.id}`, { is_active: !item.is_active }); loadTab(sidebar); }} className="text-primary-600 hover:underline text-sm">{item.is_active ? "غیرفعال" : "فعال"} کردن</button></td></>}
                              {sidebar === "ai-logs" && <><td className="p-3 text-foreground max-w-xs truncate">{item.user_message}</td><td className="p-3 text-muted max-w-xs truncate">{item.ai_response}</td><td className="p-3">{item.was_cached ? "⚡" : "-"}</td><td className="p-3 text-muted text-xs">{item.created_at ? new Date(item.created_at).toLocaleDateString("fa-AF") : "-"}</td></>}
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

      {/* Delete Confirmation Modal */}
      {deleteConfirm && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-surface-card rounded-xl shadow-xl max-w-sm w-full border border-border p-6">
            <h3 className="text-lg font-bold text-foreground mb-2">تایید حذف</h3>
            <p className="text-muted mb-1">آیا از حذف مطمئن هستید؟</p>
            <p className="text-foreground font-bold mb-4">«{deleteConfirm.name}»</p>
            <p className="text-danger text-sm mb-4">⚠️ این عمل غیرقابل بازگشت است.</p>
            <div className="flex gap-3">
              <button onClick={handleDelete} className="flex-1 py-2 bg-danger text-white rounded-[10px] hover:bg-danger/90 min-h-[44px] font-medium">بله، حذف شود</button>
              <button onClick={() => setDeleteConfirm(null)} className="flex-1 py-2 bg-surface border border-border text-foreground rounded-[10px] hover:bg-border min-h-[44px]">انصراف</button>
            </div>
          </div>
        </div>
      )}

      {/* Create/Edit Modal */}
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
                      <input type={key.includes("date") ? "date" : "text"} value={String(value)} onChange={(e) => setFormData({ ...formData, [key]: e.target.value })} className="w-full px-3 py-2 border border-border rounded-[10px] text-sm bg-surface text-foreground" />
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

      {/* Sub-items Modal (projects / alumni / roadmaps) */}
      {subDept && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-surface-card rounded-xl shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto border border-border">
            <div className="p-6">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-bold text-foreground">زیرمجموعه‌های {subDept.name_fa}</h3>
                <button onClick={() => setSubDept(null)} className="text-muted hover:text-foreground text-xl">✕</button>
              </div>

              {/* Tabs */}
              <div className="flex gap-1 mb-4 bg-surface rounded-lg p-1">
                {([["projects", "پروژه‌ها"], ["alumni", "فارغان"], ["roadmaps", "نقشه شغلی"]] as const).map(([k, l]) => (
                  <button key={k} onClick={() => { setSubTab(k); loadSubItems(subDept.slug, k); setSubForm(null); }} className={`flex-1 py-2 rounded-md text-sm font-medium transition-colors ${subTab === k ? "bg-primary-600 text-white" : "text-muted hover:bg-surface-card"}`}>{l}</button>
                ))}
              </div>

              {/* Items list */}
              {subLoading ? (
                <div className="text-center py-8 text-muted">در حال بارگذاری...</div>
              ) : subItems.length === 0 ? (
                <div className="text-center py-8 text-muted">آیتمی موجود نیست</div>
              ) : (
                <div className="space-y-2 mb-4">
                  {subItems.map((item: any) => (
                    <div key={item.id} className="flex items-center justify-between p-3 bg-surface rounded-lg border border-border">
                      <div className="flex-1 min-w-0">
                        <p className="text-foreground font-medium truncate">{subTab === "projects" ? item.title_fa : subTab === "alumni" ? item.full_name : item.career_title_fa}</p>
                        <p className="text-muted text-xs truncate">{subTab === "projects" ? item.description_fa : subTab === "alumni" ? item.current_position : `${item.steps?.length || 0} گام`}</p>
                      </div>
                      <button onClick={() => handleSubDelete(item.id)} className="text-danger hover:underline text-sm mr-2 shrink-0">حذف</button>
                    </div>
                  ))}
                </div>
              )}

              {/* Add form */}
              {subForm ? (
                <div className="border border-accent-500 rounded-lg p-4 bg-surface">
                  <h4 className="font-bold text-foreground mb-3">افزودن جدید</h4>
                  <div className="space-y-3">
                    {Object.entries(subForm).map(([key, value]) => (
                      <div key={key}>
                        <label className="block text-xs font-medium text-muted mb-1">{key}</label>
                        {typeof value === "string" && value.length > 50 ? (
                          <textarea value={value as string} onChange={(e) => setSubForm({ ...subForm, [key]: e.target.value })} className="w-full px-3 py-2 border border-border rounded-[10px] text-sm bg-surface text-foreground" rows={3} />
                        ) : (
                          <input type={key.includes("year") ? "number" : "text"} value={String(value)} onChange={(e) => setSubForm({ ...subForm, [key]: e.target.value })} className="w-full px-3 py-2 border border-border rounded-[10px] text-sm bg-surface text-foreground" />
                        )}
                      </div>
                    ))}
                  </div>
                  <div className="flex gap-2 mt-3">
                    <button onClick={handleSubSave} className="px-4 py-2 bg-primary-600 text-white rounded-[10px] text-sm hover:bg-primary-700 min-h-[44px]">ذخیره</button>
                    <button onClick={() => setSubForm(null)} className="px-4 py-2 bg-surface border border-border text-foreground rounded-[10px] text-sm hover:bg-border min-h-[44px]">انصراف</button>
                  </div>
                </div>
              ) : (
                <button onClick={() => {
                  const defaults: Record<string, any> = {
                    projects: { title_fa: "", description_fa: "", students: "", year: 1404 },
                    alumni: { full_name: "", graduation_year: 1395, current_position: "", story_fa: "" },
                    roadmaps: { career_title_fa: "", steps: [] },
                  };
                  setSubForm(defaults[subTab] || {});
                }} className="w-full py-2 border-2 border-dashed border-border rounded-lg text-muted hover:border-primary-400 hover:text-primary-600 transition-colors text-sm">
                  + افزودن {subTab === "projects" ? "پروژه" : subTab === "alumni" ? "داستان فارغ" : "نقشه شغلی"}
                </button>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Question Bank — dedicated create/edit modal */}
      {showQuestionModal && questionForm && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-surface-card rounded-xl shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto border border-border">
            <div className="p-6">
              <h3 className="text-lg font-bold mb-4 text-foreground">{questionEditItem ? "ویرایش سوال" : "سوال جدید"}</h3>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                <div>
                  <label className="block text-sm font-medium text-muted mb-1">موضوع *</label>
                  <input type="text" value={questionForm.subject} onChange={(e) => setQuestionForm({ ...questionForm, subject: e.target.value })} placeholder="ریاضی، فزیک، کیمیا..." className="w-full px-3 py-2 border border-border rounded-[10px] text-sm bg-surface text-foreground" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-muted mb-1">سطح دشواری</label>
                  <select value={questionForm.difficulty} onChange={(e) => setQuestionForm({ ...questionForm, difficulty: e.target.value })} className="w-full px-3 py-2 border border-border rounded-[10px] text-sm bg-surface text-foreground">
                    <option value="easy">آسان</option>
                    <option value="medium">متوسط</option>
                    <option value="hard">دشوار</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-muted mb-1">سال کانکور (اختیاری)</label>
                  <input type="number" value={questionForm.year} onChange={(e) => setQuestionForm({ ...questionForm, year: e.target.value })} placeholder="مثلاً ۱۴۰۳" className="w-full px-3 py-2 border border-border rounded-[10px] text-sm bg-surface text-foreground" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-muted mb-1">منبع (اختیاری)</label>
                  <input type="text" value={questionForm.source} onChange={(e) => setQuestionForm({ ...questionForm, source: e.target.value })} placeholder="کانکور ۱۴۰۳ دور اول" className="w-full px-3 py-2 border border-border rounded-[10px] text-sm bg-surface text-foreground" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-muted mb-1">صنف کتاب درسی (اختیاری)</label>
                  <select value={questionForm.grade} onChange={(e) => setQuestionForm({ ...questionForm, grade: e.target.value })} className="w-full px-3 py-2 border border-border rounded-[10px] text-sm bg-surface text-foreground">
                    <option value="">نامشخص</option>
                    <option value="10">صنف ۱۰</option>
                    <option value="11">صنف ۱۱</option>
                    <option value="12">صنف ۱۲</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-muted mb-1">فصل/باب کتاب (اختیاری)</label>
                  <input type="text" value={questionForm.chapter} onChange={(e) => setQuestionForm({ ...questionForm, chapter: e.target.value })} placeholder="مثلاً مثلثات" className="w-full px-3 py-2 border border-border rounded-[10px] text-sm bg-surface text-foreground" />
                </div>
              </div>

              <div className="mb-4">
                <label className="block text-sm font-medium text-muted mb-1">متن سوال *</label>
                <textarea value={questionForm.question_fa} onChange={(e) => setQuestionForm({ ...questionForm, question_fa: e.target.value })} rows={3} className="w-full px-3 py-2 border border-border rounded-[10px] text-sm bg-surface text-foreground" />
              </div>

              <div className="mb-4">
                <label className="block text-sm font-medium text-muted mb-2">گزینه‌ها * (جواب درست را با دکمه رادیویی مشخص کنید)</label>
                <div className="space-y-2">
                  {questionForm.options.map((opt: any, i: number) => (
                    <div key={i} className="flex items-center gap-2">
                      <input type="radio" name="correct-option" checked={opt.is_correct} onChange={() => setCorrectOption(i)} className="w-4 h-4 shrink-0" aria-label="گزینه درست" />
                      <input type="text" value={opt.text} onChange={(e) => setOptionText(i, e.target.value)} placeholder={`گزینه ${i + 1}`} className={`flex-1 px-3 py-2 border rounded-[10px] text-sm bg-surface text-foreground ${opt.is_correct ? "border-success ring-1 ring-success" : "border-border"}`} />
                      <button onClick={() => removeOption(i)} disabled={questionForm.options.length <= 2} className="text-danger hover:underline text-sm disabled:opacity-30 disabled:cursor-not-allowed shrink-0">حذف</button>
                    </div>
                  ))}
                </div>
                {questionForm.options.length < 6 && (
                  <button onClick={addOption} className="mt-2 text-sm text-primary-600 hover:underline">+ افزودن گزینه</button>
                )}
              </div>

              <div className="mb-4">
                <label className="block text-sm font-medium text-muted mb-1">توضیح جواب (اختیاری — برای صفحه مرور بعد از امتحان)</label>
                <textarea value={questionForm.explanation_fa} onChange={(e) => setQuestionForm({ ...questionForm, explanation_fa: e.target.value })} rows={2} className="w-full px-3 py-2 border border-border rounded-[10px] text-sm bg-surface text-foreground" />
              </div>

              <label className="flex items-center gap-2 mb-6 cursor-pointer">
                <input type="checkbox" checked={questionForm.is_verified} onChange={(e) => setQuestionForm({ ...questionForm, is_verified: e.target.checked })} className="w-4 h-4" />
                <span className="text-sm text-foreground">تایید شده — این سوال در کانکور آزمایشی استفاده شود</span>
              </label>
              {!questionForm.is_verified && (
                <p className="text-xs text-warning -mt-4 mb-6">⚠️ تا تیک نخورد، این سوال هرگز در آزمون‌های کانکور آزمایشی انتخاب نمی‌شود (کنترل کیفیت دومرحله‌ای).</p>
              )}

              <div className="flex gap-3">
                <button onClick={handleQuestionSave} disabled={questionSaving} className="flex-1 py-2 bg-primary-600 text-white rounded-[10px] hover:bg-primary-700 min-h-[44px] disabled:opacity-60">{questionSaving ? "در حال ذخیره..." : questionEditItem ? "ذخیره" : "ایجاد"}</button>
                <button onClick={() => setShowQuestionModal(false)} className="flex-1 py-2 bg-surface border border-border text-foreground rounded-[10px] hover:bg-border min-h-[44px]">انصراف</button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Question Bank — bulk JSON import */}
      {showImportModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-surface-card rounded-xl shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto border border-border">
            <div className="p-6">
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-lg font-bold text-foreground">درون‌ریزی گروهی سوالات (JSON)</h3>
                <button onClick={() => { setShowImportModal(false); setImportErrors([]); }} className="text-muted hover:text-foreground text-xl">✕</button>
              </div>
              <p className="text-sm text-muted mb-4">
                یک آرایه JSON از سوالات وارد یا فایل را انتخاب کنید. درون‌ریزی <strong className="text-foreground">همه یا هیچ</strong> است — اگر حتی یک ردیف خطا داشته باشد، هیچ سوالی ذخیره نمی‌شود.
              </p>

              <details className="mb-4 bg-surface border border-border rounded-lg p-3">
                <summary className="cursor-pointer text-sm font-medium text-primary-600">نمونه فرمت هر سوال</summary>
                <pre className="mt-2 text-xs text-muted overflow-x-auto" dir="ltr">{`{
  "subject": "ریاضی",
  "year": 1402,
  "source": "کانکور ۱۴۰۲",
  "difficulty": "medium",
  "question_fa": "...",
  "options": [
    {"text": "...", "is_correct": true},
    {"text": "..."},
    {"text": "..."}
  ],
  "explanation_fa": "..."
}`}</pre>
              </details>

              <div className="mb-3">
                <input
                  type="file"
                  accept=".json,application/json"
                  onChange={(e) => { if (e.target.files?.[0]) handleImportFile(e.target.files[0]); }}
                  className="block w-full text-sm text-muted file:ml-3 file:py-2 file:px-4 file:rounded-[10px] file:border-0 file:bg-primary-50 file:text-primary-700 hover:file:bg-primary-100"
                />
              </div>

              <textarea
                value={importText}
                onChange={(e) => setImportText(e.target.value)}
                rows={10}
                placeholder="آرایه JSON سوالات را اینجا بچسبانید..."
                dir="ltr"
                className="w-full px-3 py-2 border border-border rounded-[10px] text-xs bg-surface text-foreground font-mono"
              />

              {importErrors.length > 0 && (
                <div className="mt-4 bg-danger/10 border border-danger/30 rounded-lg p-3 max-h-48 overflow-y-auto">
                  <p className="text-sm font-bold text-danger mb-2">{importErrors.length} ردیف خطا دارد:</p>
                  <ul className="space-y-1">
                    {importErrors.map((err, i) => (
                      <li key={i} className="text-xs text-danger">ردیف {err.row}: {err.message}</li>
                    ))}
                  </ul>
                </div>
              )}

              <div className="flex gap-3 mt-4">
                <button onClick={handleImport} disabled={importBusy || !importText.trim()} className="flex-1 py-2 bg-accent-500 text-white rounded-[10px] hover:bg-accent-600 min-h-[44px] disabled:opacity-60">{importBusy ? "در حال بررسی..." : "بررسی و درون‌ریزی"}</button>
                <button onClick={() => { setShowImportModal(false); setImportErrors([]); }} className="flex-1 py-2 bg-surface border border-border text-foreground rounded-[10px] hover:bg-border min-h-[44px]">انصراف</button>
              </div>
            </div>
          </div>
        </div>
      )}

      <Footer />
    </>
  );
}
