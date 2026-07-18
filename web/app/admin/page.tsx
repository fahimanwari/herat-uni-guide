"use client";

import { useState, useEffect } from "react";
import { Header } from "../components/layout/Header";
import { Footer } from "../components/layout/Footer";
import { adminApi } from "../lib/adminApi";

import { API_BASE, API_ORIGIN } from "../lib/config";
const API = API_BASE;

export default function AdminPage() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [tab, setTab] = useState("dashboard");
  const [data, setData] = useState<any>({});
  const [loading, setLoading] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [modalType, setModalType] = useState("");
  const [editItem, setEditItem] = useState<any>(null);
  const [formData, setFormData] = useState<any>({});
  const [message, setMessage] = useState({ text: "", type: "" });
  const [loginForm, setLoginForm] = useState({ email: "", password: "" });
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    const token = localStorage.getItem("admin_access");
    if (token) setIsLoggedIn(true);
  }, []);

  useEffect(() => {
    if (mounted && isLoggedIn) loadTab(tab);
  }, [tab, mounted, isLoggedIn]);

  const showMessage = (text: string, type: string = "success") => {
    setMessage({ text, type });
    setTimeout(() => setMessage({ text: "", type: "" }), 3000);
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
    } catch (e) {
      showMessage("خطا در بارگذاری", "error");
    }
    setLoading(false);
  };

  const openCreate = (type: string) => {
    setEditItem(null);
    setModalType(type);
    setFormData(getDefaultFormData(type));
    setShowModal(true);
  };

  const openEdit = (type: string, item: any) => {
    setEditItem(item);
    setModalType(type);
    setFormData(item);
    setShowModal(true);
  };

  const getDefaultFormData = (type: string) => {
    const defaults: Record<string, any> = {
      faculties: { name_fa: "", slug: "", description_fa: "", university_id: "" },
      departments: { name_fa: "", slug: "", description_fa: "", faculty_id: "", department_type: "degree", duration_years: 4 },
      news: { title_fa: "", body_fa: "", university_id: "", is_published: false },
      faqs: { question_fa: "", answer_fa: "", category: "" },
      exams: { title_fa: "", description_fa: "", category: "kankor", duration_minutes: 60, total_questions: 10, passing_score: 50 },
    };
    return defaults[type] || {};
  };

  const handleSave = async () => {
    try {
      if (editItem) {
        await adminApi.update(`/${modalType}/${editItem.id || editItem.slug || editItem.slug}`, formData);
        showMessage("با موفقیت ویرایش شد");
      } else {
        await adminApi.create(`/${modalType}`, formData);
        showMessage("با موفقیت ایجاد شد");
      }
      setShowModal(false);
      loadTab(tab);
    } catch (e) {
      showMessage("خطا در ذخیره", "error");
    }
  };

  const handleDelete = async (type: string, id: string) => {
    if (!confirm("آیا مطمئن هستید؟")) return;
    try {
      await adminApi.delete(`/${type}/${id}`);
      showMessage("با موفقیت حذف شد");
      loadTab(tab);
    } catch (e) {
      showMessage("خطا در حذف", "error");
    }
  };

  // Login page
  if (!isLoggedIn) {
    return (
      <>
        <Header />
        <main className="flex-1 flex items-center justify-center py-12 bg-gray-50 min-h-screen">
          <div className="w-full max-w-md">
            <div className="bg-white rounded-xl shadow-lg p-8">
              <h1 className="text-2xl font-bold text-center mb-6">ورود به پنل مدیریت</h1>
              {message.text && (
                <div className={`p-3 rounded-lg mb-4 text-sm ${message.type === "error" ? "bg-red-50 text-red-600" : "bg-green-50 text-green-600"}`}>
                  {message.text}
                </div>
              )}
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">ایمیل</label>
                  <input
                    type="email"
                    value={loginForm.email}
                    onChange={(e) => setLoginForm({ ...loginForm, email: e.target.value })}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    placeholder="admin@herat-uni.edu.af"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">رمز عبور</label>
                  <input
                    type="password"
                    value={loginForm.password}
                    onChange={(e) => setLoginForm({ ...loginForm, password: e.target.value })}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    placeholder="رمز عبور"
                  />
                </div>
                <button
                  onClick={async () => {
                    try {
                      await adminApi.login(loginForm.email, loginForm.password);
                      setIsLoggedIn(true);
                      showMessage("ورود موفق");
                    } catch (e) {
                      showMessage("ایمیل یا رمز اشتباه است", "error");
                    }
                  }}
                  className="w-full py-3 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition-colors"
                >
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

  const tabs = [
    { id: "dashboard", label: "داشبورد", icon: "📊" },
    { id: "faculties", label: "پوهنځی‌ها", icon: "📚" },
    { id: "departments", label: "دیپارتمنت‌ها", icon: "🎓" },
    { id: "news", label: "اخبار", icon: "📰" },
    { id: "faqs", label: "FAQ", icon: "❓" },
    { id: "exams", label: "امتحانات", icon: "📝" },
    { id: "questions", label: "بانک سوالات", icon: "🧩" },
    { id: "results", label: "نتایج", icon: "🏆" },
    { id: "notifications", label: "رویدادها", icon: "📅" },
  ];

  const items = data.items || [];

  return (
    <>
      <Header />
      <main className="flex-1 py-6 bg-gray-50 min-h-screen">
        <div className="max-w-7xl mx-auto px-4">
          {/* Header */}
          <div className="flex items-center justify-between mb-6">
            <h1 className="text-2xl font-bold text-gray-900">پنل مدیریت</h1>
            <div className="flex gap-2">
              <a href="${API_ORIGIN}/docs" target="_blank" className="text-blue-600 hover:underline text-sm">📄 API</a>
              <button onClick={async () => { try { const r = await fetch(`${API}/admin/rag/reindex`, {method:"POST", headers:{"Authorization":`Bearer ${localStorage.getItem("admin_access")}`}}); const d = await r.json(); showMessage(`بازسازی: ${d.chunks_created || 0} chunk`); } catch(e) { showMessage("خطا", "error"); } }} className="px-3 py-1 bg-green-600 text-white rounded text-sm hover:bg-green-700">🤖 بازسازی</button>
              <button onClick={() => { localStorage.clear(); setIsLoggedIn(false); }} className="text-red-600 hover:underline text-sm">خروج</button>
            </div>
          </div>

          {/* Message */}
          {message.text && (
            <div className={`p-3 rounded-lg mb-4 text-sm ${message.type === "error" ? "bg-red-50 text-red-600" : "bg-green-50 text-green-600"}`}>
              {message.text}
            </div>
          )}

          {/* Tabs */}
          <div className="flex flex-wrap gap-2 mb-6">
            {tabs.map((t) => (
              <button
                key={t.id}
                onClick={() => setTab(t.id)}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                  tab === t.id
                    ? "bg-blue-600 text-white shadow-md"
                    : "bg-white border border-gray-200 text-gray-600 hover:bg-blue-50"
                }`}
              >
                {t.icon} {t.label}
              </button>
            ))}
          </div>

          {/* Content */}
          {loading ? (
            <div className="bg-white rounded-xl shadow-sm border p-6 text-center py-12 text-gray-500">در حال بارگذاری...</div>
          ) : (
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              {/* Dashboard */}
              {tab === "dashboard" && (
                <div>
                  <h2 className="text-lg font-bold mb-4">آمار کلی</h2>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    {[
                      ["پوهنځی‌ها", data.faculties?.length || 0],
                      ["دیپارتمنت‌ها", data.departments?.length || 0],
                      ["امتحانات", data.exams?.length || 0],
                      ["اخبار", data.news?.length || 0],
                      ["FAQ", data.faqs?.length || 0],
                      ["سوالات بانک", data.questionBank?.total || 0],
                    ].map(([label, value]) => (
                      <div key={String(label)} className="bg-gray-50 rounded-lg p-4 text-center">
                        <div className="text-3xl font-bold text-blue-600">{value}</div>
                        <div className="text-gray-500 text-sm mt-1">{String(label)}</div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* CRUD Tables */}
              {tab !== "dashboard" && (
                <div>
                  <div className="flex items-center justify-between mb-4">
                    <h2 className="text-lg font-bold">{tabs.find(t => t.id === tab)?.label} ({items.length})</h2>
                    {!["questions", "results", "exams"].includes(tab) && (
                      <button onClick={() => openCreate(tab)} className="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm hover:bg-blue-700">
                        + افزودن
                      </button>
                    )}
                  </div>
                  {items.length === 0 ? (
                    <p className="text-gray-500 text-center py-8">داده‌ای موجود نیست</p>
                  ) : (
                    <div className="overflow-x-auto">
                      <table className="w-full text-sm border-collapse">
                        <thead>
                          <tr className="bg-gray-50 border-b">
                            {tab === "faculties" && <><th className="text-right p-3">نام</th><th className="text-right p-3">Slug</th><th className="text-right p-3">عملیات</th></>}
                            {tab === "departments" && <><th className="text-right p-3">نام</th><th className="text-right p-3">Slug</th><th className="text-right p-3">نوع</th><th className="text-right p-3">عملیات</th></>}
                            {tab === "news" && <><th className="text-right p-3">عنوان</th><th className="text-right p-3">وضعیت</th><th className="text-right p-3">عملیات</th></>}
                            {tab === "faqs" && <><th className="text-right p-3">سوال</th><th className="text-right p-3">دسته</th><th className="text-right p-3">عملیات</th></>}
                            {tab === "exams" && <><th className="text-right p-3">عنوان</th><th className="text-right p-3">سوالات</th><th className="text-right p-3">مدت</th><th className="text-right p-3">عملیات</th></>}
                            {tab === "questions" && <><th className="text-right p-3">موضوع</th><th className="text-right p-3">سطح</th><th className="text-right p-3">سوال</th></>}
                            {tab === "results" && <><th className="text-right p-3">نمره</th><th className="text-right p-3">درست</th><th className="text-right p-3">وضعیت</th></>}
                            {tab === "notifications" && <><th className="text-right p-3">عنوان</th><th className="text-right p-3">تاریخ</th><th className="text-right p-3">عملیات</th></>}
                          </tr>
                        </thead>
                        <tbody>
                          {items.map((item: any) => (
                            <tr key={item.id || item.slug} className="border-b hover:bg-gray-50">
                              {tab === "faculties" && <><td className="p-3 font-medium">{item.name_fa}</td><td className="p-3 text-gray-500">{item.slug}</td><td className="p-3"><button onClick={() => openEdit("faculties", item)} className="text-blue-600 hover:underline text-sm ml-2">ویرایش</button><button onClick={() => handleDelete("faculties", item.id)} className="text-red-600 hover:underline text-sm">حذف</button></td></>}
                              {tab === "departments" && <><td className="p-3 font-medium">{item.name_fa}</td><td className="p-3 text-gray-500">{item.slug}</td><td className="p-3"><span className={`px-2 py-1 rounded text-xs ${item.department_type === "degree" ? "bg-green-100 text-green-700" : "bg-gray-100 text-gray-600"}`}>{item.department_type}</span></td><td className="p-3"><button onClick={() => openEdit("departments", item)} className="text-blue-600 hover:underline text-sm ml-2">ویرایش</button><button onClick={() => handleDelete("departments", item.id)} className="text-red-600 hover:underline text-sm">حذف</button></td></>}
                              {tab === "news" && <><td className="p-3">{item.title_fa}</td><td className="p-3"><span className={`px-2 py-1 rounded text-xs ${item.is_published ? "bg-green-100 text-green-700" : "bg-yellow-100 text-yellow-700"}`}>{item.is_published ? "منتشر" : "پیش‌نویس"}</span></td><td className="p-3"><button onClick={() => openEdit("news", item)} className="text-blue-600 hover:underline text-sm ml-2">ویرایش</button><button onClick={() => handleDelete("news", item.id)} className="text-red-600 hover:underline text-sm">حذف</button></td></>}
                              {tab === "faqs" && <><td className="p-3">{item.question_fa}</td><td className="p-3 text-gray-500">{item.category || "-"}</td><td className="p-3"><button onClick={() => openEdit("faqs", item)} className="text-blue-600 hover:underline text-sm ml-2">ویرایش</button><button onClick={() => handleDelete("faqs", item.id)} className="text-red-600 hover:underline text-sm">حذف</button></td></>}
                              {tab === "exams" && <><td className="p-3 font-medium">{item.title_fa}</td><td className="p-3">{item.total_questions}</td><td className="p-3">{item.duration_minutes} دقیقه</td><td className="p-3"><button onClick={() => openEdit("exams", item)} className="text-blue-600 hover:underline text-sm ml-2">ویرایش</button><button onClick={() => handleDelete("exams", item.id)} className="text-red-600 hover:underline text-sm">حذف</button></td></>}
                              {tab === "questions" && <><td className="p-3"><span className="px-2 py-1 rounded text-xs bg-blue-100 text-blue-700">{item.subject}</span></td><td className="p-3"><span className={`px-2 py-1 rounded text-xs ${item.difficulty === "easy" ? "bg-green-100 text-green-700" : item.difficulty === "hard" ? "bg-red-100 text-red-700" : "bg-yellow-100 text-yellow-700"}`}>{item.difficulty}</span></td><td className="p-3 max-w-md truncate">{item.question_fa}</td></>}
                              {tab === "results" && <><td className="p-3 font-bold">{item.score}%</td><td className="p-3 text-green-600">{item.correct_answers}/{item.total_answers}</td><td className="p-3"><span className={`px-2 py-1 rounded text-xs ${item.passed ? "bg-green-100 text-green-700" : "bg-red-100 text-red-700"}`}>{item.passed ? "قبول" : "مردود"}</span></td></>}
                              {tab === "notifications" && <><td className="p-3">{item.title_fa}</td><td className="p-3">{new Date(item.event_date).toLocaleDateString("fa-AF")}</td><td className="p-3"><button onClick={() => handleDelete("notifications/events", item.id)} className="text-red-600 hover:underline text-sm">حذف</button></td></>}
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
        </div>
      </main>

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl shadow-xl max-w-lg w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <h3 className="text-lg font-bold mb-4">{editItem ? "ویرایش" : "افزودن"} {modalType}</h3>
              <div className="space-y-4">
                {Object.entries(formData).map(([key, value]) => (
                  <div key={key}>
                    <label className="block text-sm font-medium text-gray-700 mb-1">{key}</label>
                    {typeof value === "boolean" ? (
                      <input
                        type="checkbox"
                        checked={value as boolean}
                        onChange={(e) => setFormData({ ...formData, [key]: e.target.checked })}
                        className="w-4 h-4"
                      />
                    ) : typeof value === "string" && value.length > 100 ? (
                      <textarea
                        value={value as string}
                        onChange={(e) => setFormData({ ...formData, [key]: e.target.value })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm"
                        rows={4}
                      />
                    ) : (
                      <input
                        type="text"
                        value={String(value)}
                        onChange={(e) => setFormData({ ...formData, [key]: e.target.value })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm"
                      />
                    )}
                  </div>
                ))}
              </div>
              <div className="flex gap-3 mt-6">
                <button onClick={handleSave} className="flex-1 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
                  {editItem ? "ذخیره" : "ایجاد"}
                </button>
                <button onClick={() => setShowModal(false)} className="flex-1 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300">
                  انصراف
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      <Footer />
    </>
  );
}
