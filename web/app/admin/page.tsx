"use client";

import { useState, useEffect } from "react";
import { Header } from "../components/layout/Header";
import { Footer } from "../components/layout/Footer";

const API = "http://localhost:9000/api/v1";

export default function AdminPage() {
  const [tab, setTab] = useState("dashboard");
  const [data, setData] = useState<any>({});
  const [loading, setLoading] = useState(false);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  useEffect(() => {
    if (!mounted) return;
    loadTab(tab);
  }, [tab, mounted]);

  const loadTab = async (t: string) => {
    setLoading(true);
    try {
      const endpoints: Record<string, string> = {
        dashboard: "",
        universities: "universities",
        faculties: "faculties",
        departments: "departments",
        news: "news",
        faqs: "faqs",
        exams: "exam",
        questions: "question-bank/questions?limit=200",
        results: "exam/results/all",
        notifications: "notifications/events",
      };

      if (t === "dashboard") {
        const [uni, fac, dept, exam, qb, news, faq, notif] = await Promise.all([
          fetch(`${API}/universities`).then(r => r.json()).catch(() => []),
          fetch(`${API}/faculties`).then(r => r.json()).catch(() => []),
          fetch(`${API}/departments`).then(r => r.json()).catch(() => []),
          fetch(`${API}/exam`).then(r => r.json()).catch(() => []),
          fetch(`${API}/question-bank/stats`).then(r => r.json()).catch(() => ({})),
          fetch(`${API}/news`).then(r => r.json()).catch(() => []),
          fetch(`${API}/faqs`).then(r => r.json()).catch(() => []),
          fetch(`${API}/notifications/events`).then(r => r.json()).catch(() => []),
        ]);
        setData({ type: "dashboard", universities: uni, faculties: fac, departments: dept, exams: exam, questionBank: qb, news: news, faqs: faq, notifications: notif });
      } else {
        const items = await fetch(`${API}/${endpoints[t]}`).then(r => r.json()).catch(() => []);
        setData({ type: t, items: Array.isArray(items) ? items : [] });
      }
    } catch (e) {
      setData({ type: t, items: [], error: "خطا در بارگذاری" });
    }
    setLoading(false);
  };

  if (!mounted) {
    return (
      <>
        <Header />
        <main className="flex-1 py-6 bg-gray-50 min-h-screen">
          <div className="max-w-7xl mx-auto px-4">
            <h1 className="text-2xl font-bold mb-6">پنل مدیریت</h1>
            <div className="text-center py-12 text-gray-500">در حال بارگذاری...</div>
          </div>
        </main>
        <Footer />
      </>
    );
  }

  const tabs = [
    { id: "dashboard", label: "داشبورد", icon: "📊" },
    { id: "universities", label: "پوهنتون‌ها", icon: "🏛️" },
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
          <div className="flex items-center justify-between mb-6">
            <h1 className="text-2xl font-bold text-gray-900">پنل مدیریت</h1>
            <a href="http://localhost:9000/docs" target="_blank" className="text-blue-600 hover:underline text-sm">📄 مستندات API</a>
          </div>

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

          {loading ? (
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <div className="text-center py-12 text-gray-500">در حال بارگذاری...</div>
            </div>
          ) : (
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              {data.error && <div className="bg-red-50 border border-red-200 rounded-lg p-3 mb-4 text-red-600 text-sm">{data.error}</div>}

              {/* Dashboard */}
              {tab === "dashboard" && (
                <div>
                  <h2 className="text-lg font-bold mb-4">آمار کلی</h2>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    {[
                      ["پوهنتون‌ها", data.universities?.length || 0],
                      ["پوهنځی‌ها", data.faculties?.length || 0],
                      ["دیپارتمنت‌ها", data.departments?.length || 0],
                      ["امتحانات", data.exams?.length || 0],
                      ["اخبار", data.news?.length || 0],
                      ["FAQ", data.faqs?.length || 0],
                      ["رویدادها", data.notifications?.length || 0],
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

              {/* Tables */}
              {tab !== "dashboard" && (
                <div>
                  <h2 className="text-lg font-bold mb-4">{tabs.find(t => t.id === tab)?.label} ({items.length})</h2>
                  {items.length === 0 ? (
                    <p className="text-gray-500 text-center py-8">داده‌ای موجود نیست</p>
                  ) : (
                    <div className="overflow-x-auto">
                      <table className="w-full text-sm border-collapse">
                        <thead>
                          <tr className="bg-gray-50 border-b">
                            {tab === "universities" && <><th className="text-right p-3">نام</th><th className="text-right p-3">Slug</th><th className="text-right p-3">سال</th></>}
                            {tab === "faculties" && <><th className="text-right p-3">نام</th><th className="text-right p-3">Slug</th></>}
                            {tab === "departments" && <><th className="text-right p-3">نام</th><th className="text-right p-3">Slug</th><th className="text-right p-3">نوع</th><th className="text-right p-3">مدت</th></>}
                            {tab === "news" && <><th className="text-right p-3">عنوان</th><th className="text-right p-3">وضعیت</th></>}
                            {tab === "faqs" && <><th className="text-right p-3">سوال</th><th className="text-right p-3">دسته</th></>}
                            {tab === "exams" && <><th className="text-right p-3">عنوان</th><th className="text-right p-3">سوالات</th><th className="text-right p-3">مدت</th></>}
                            {tab === "questions" && <><th className="text-right p-3">موضوع</th><th className="text-right p-3">سطح</th><th className="text-right p-3">سوال</th></>}
                            {tab === "results" && <><th className="text-right p-3">نمره</th><th className="text-right p-3">درست</th><th className="text-right p-3">وضعیت</th></>}
                            {tab === "notifications" && <><th className="text-right p-3">عنوان</th><th className="text-right p-3">تاریخ</th><th className="text-right p-3">نوع</th></>}
                          </tr>
                        </thead>
                        <tbody>
                          {items.map((item: any, i: number) => (
                            <tr key={item.id || i} className="border-b hover:bg-gray-50">
                              {tab === "universities" && <><td className="p-3 font-medium">{item.name_fa}</td><td className="p-3 text-gray-500">{item.slug}</td><td className="p-3">{item.established_year || "-"}</td></>}
                              {tab === "faculties" && <><td className="p-3 font-medium">{item.name_fa}</td><td className="p-3 text-gray-500">{item.slug}</td></>}
                              {tab === "departments" && <><td className="p-3 font-medium">{item.name_fa}</td><td className="p-3 text-gray-500">{item.slug}</td><td className="p-3"><span className={`px-2 py-1 rounded text-xs ${item.department_type === "degree" ? "bg-green-100 text-green-700" : "bg-gray-100 text-gray-600"}`}>{item.department_type}</span></td><td className="p-3">{item.duration_years} سال</td></>}
                              {tab === "news" && <><td className="p-3">{item.title_fa}</td><td className="p-3"><span className={`px-2 py-1 rounded text-xs ${item.is_published ? "bg-green-100 text-green-700" : "bg-yellow-100 text-yellow-700"}`}>{item.is_published ? "منتشر" : "پیش‌نویس"}</span></td></>}
                              {tab === "faqs" && <><td className="p-3">{item.question_fa}</td><td className="p-3 text-gray-500">{item.category || "-"}</td></>}
                              {tab === "exams" && <><td className="p-3 font-medium">{item.title_fa}</td><td className="p-3">{item.total_questions}</td><td className="p-3">{item.duration_minutes} دقیقه</td></>}
                              {tab === "questions" && <><td className="p-3"><span className="px-2 py-1 rounded text-xs bg-blue-100 text-blue-700">{item.subject}</span></td><td className="p-3"><span className={`px-2 py-1 rounded text-xs ${item.difficulty === "easy" ? "bg-green-100 text-green-700" : item.difficulty === "hard" ? "bg-red-100 text-red-700" : "bg-yellow-100 text-yellow-700"}`}>{item.difficulty}</span></td><td className="p-3 max-w-md truncate">{item.question_fa}</td></>}
                              {tab === "results" && <><td className="p-3 font-bold">{item.score}%</td><td className="p-3 text-green-600">{item.correct_answers}/{item.total_answers}</td><td className="p-3"><span className={`px-2 py-1 rounded text-xs ${item.passed ? "bg-green-100 text-green-700" : "bg-red-100 text-red-700"}`}>{item.passed ? "قبول" : "مردود"}</span></td></>}
                              {tab === "notifications" && <><td className="p-3">{item.title_fa}</td><td className="p-3">{new Date(item.event_date).toLocaleDateString("fa-AF")}</td><td className="p-3"><span className="px-2 py-1 rounded text-xs bg-purple-100 text-purple-700">{item.event_type}</span></td></>}
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
      <Footer />
    </>
  );
}
