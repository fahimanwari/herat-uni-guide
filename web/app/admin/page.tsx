"use client";

import { useState, useEffect, useCallback } from "react";
import { Header } from "../components/layout/Header";
import { Footer } from "../components/layout/Footer";

const API = "http://localhost:9000/api/v1";

// Safe fetch helper
async function safeFetch(url: string): Promise<any> {
  try {
    const res = await fetch(url, { cache: "no-store" });
    if (!res.ok) return [];
    const data = await res.json();
    return Array.isArray(data) ? data : (typeof data === "object" && data !== null ? data : []);
  } catch {
    return [];
  }
}

// Table component
function DataTable({ columns, data }: { columns: { key: string; label: string; render?: (val: any, row: any) => React.ReactNode }[]; data: any[] }) {
  if (!data || data.length === 0) {
    return <p className="text-gray-500 text-center py-8">داده‌ای موجود نیست</p>;
  }
  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm border-collapse">
        <thead>
          <tr className="bg-gray-50 border-b">
            {columns.map((col) => (
              <th key={col.key} className="text-right p-3 font-medium text-gray-700">{col.label}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, i) => (
            <tr key={row.id || i} className="border-b hover:bg-gray-50">
              {columns.map((col) => (
                <td key={col.key} className="p-3">
                  {col.render ? col.render(row[col.key], row) : (row[col.key] ?? "-")}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default function AdminPage() {
  const [tab, setTab] = useState("dashboard");
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const loadData = useCallback(async (t: string) => {
    setLoading(true);
    setError("");
    setData(null);
    try {
      if (t === "dashboard") {
        const [uni, fac, dept, exam, qb, news, faq, notif] = await Promise.all([
          safeFetch(`${API}/universities`),
          safeFetch(`${API}/faculties`),
          safeFetch(`${API}/departments`),
          safeFetch(`${API}/exam`),
          safeFetch(`${API}/question-bank/stats`),
          safeFetch(`${API}/news`),
          safeFetch(`${API}/faqs`),
          safeFetch(`${API}/notifications/events`),
        ]);
        setData({ universities: uni, faculties: fac, departments: dept, exams: exam, questionBank: qb, news: news, faqs: faq, notifications: notif });
      } else if (t === "universities") {
        setData({ items: await safeFetch(`${API}/universities`) });
      } else if (t === "faculties") {
        setData({ items: await safeFetch(`${API}/faculties`) });
      } else if (t === "departments") {
        setData({ items: await safeFetch(`${API}/departments`) });
      } else if (t === "news") {
        setData({ items: await safeFetch(`${API}/news`) });
      } else if (t === "faqs") {
        setData({ items: await safeFetch(`${API}/faqs`) });
      } else if (t === "exams") {
        setData({ items: await safeFetch(`${API}/exam`) });
      } else if (t === "questions") {
        setData({ items: await safeFetch(`${API}/question-bank/questions?limit=200`) });
      } else if (t === "results") {
        setData({ items: await safeFetch(`${API}/exam/results/all`) });
      } else if (t === "notifications") {
        setData({ items: await safeFetch(`${API}/notifications/events`) });
      }
    } catch (e) {
      setError("خطا در بارگذاری داده");
    }
    setLoading(false);
  }, []);

  useEffect(() => {
    loadData(tab);
  }, [tab, loadData]);

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

  const items = data?.items || [];

  return (
    <>
      <Header />
      <main className="flex-1 py-6 bg-gray-50 min-h-screen">
        <div className="max-w-7xl mx-auto px-4">
          {/* Header */}
          <div className="flex items-center justify-between mb-6">
            <h1 className="text-2xl font-bold text-gray-900">پنل مدیریت</h1>
            <a href="http://localhost:9000/docs" target="_blank" className="text-blue-600 hover:underline text-sm">📄 مستندات API</a>
          </div>

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

          {/* Error */}
          {error && <div className="bg-red-50 border border-red-200 rounded-lg p-3 mb-4 text-red-600 text-sm">{error}</div>}

          {/* Content */}
          {loading ? (
            <div className="text-center py-12 text-gray-500">در حال بارگذاری...</div>
          ) : (
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              {/* Dashboard */}
              {tab === "dashboard" && data && (
                <div>
                  <h2 className="text-lg font-bold mb-4">آمار کلی سیستم</h2>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                    {[
                      { label: "پوهنتون‌ها", value: Array.isArray(data.universities) ? data.universities.length : 0, color: "text-blue-600" },
                      { label: "پوهنځی‌ها", value: Array.isArray(data.faculties) ? data.faculties.length : 0, color: "text-blue-600" },
                      { label: "دیپارتمنت‌ها", value: Array.isArray(data.departments) ? data.departments.length : 0, color: "text-blue-600" },
                      { label: "امتحانات", value: Array.isArray(data.exams) ? data.exams.length : 0, color: "text-blue-600" },
                      { label: "اخبار", value: Array.isArray(data.news) ? data.news.length : 0, color: "text-green-600" },
                      { label: "FAQ", value: Array.isArray(data.faqs) ? data.faqs.length : 0, color: "text-green-600" },
                      { label: "رویدادها", value: Array.isArray(data.notifications) ? data.notifications.length : 0, color: "text-purple-600" },
                      { label: "سوالات بانک", value: data.questionBank?.total || 0, color: "text-orange-600" },
                    ].map((s) => (
                      <div key={s.label} className="bg-gray-50 rounded-lg p-4 text-center">
                        <div className={`text-3xl font-bold ${s.color}`}>{s.value}</div>
                        <div className="text-gray-500 text-sm mt-1">{s.label}</div>
                      </div>
                    ))}
                  </div>

                  {/* Question Bank Breakdown */}
                  {data.questionBank && typeof data.questionBank === "object" && (
                    <div>
                      <h3 className="font-bold mb-3">توزیع سوالات به تفکیک موضوع</h3>
                      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                        {Object.entries(data.questionBank).filter(([k]) => k !== "total").map(([subject, count]) => (
                          <div key={subject} className="bg-blue-50 rounded-lg p-3 text-center">
                            <div className="font-bold text-blue-600">{count as number}</div>
                            <div className="text-xs text-gray-600">{subject}</div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}

              {/* Universities */}
              {tab === "universities" && (
                <DataTable
                  columns={[
                    { key: "name_fa", label: "نام" },
                    { key: "slug", label: "Slug" },
                    { key: "established_year", label: "سال تأسیس" },
                  ]}
                  data={items}
                />
              )}

              {/* Faculties */}
              {tab === "faculties" && (
                <DataTable
                  columns={[
                    { key: "name_fa", label: "نام" },
                    { key: "slug", label: "Slug" },
                  ]}
                  data={items}
                />
              )}

              {/* Departments */}
              {tab === "departments" && (
                <DataTable
                  columns={[
                    { key: "name_fa", label: "نام" },
                    { key: "slug", label: "Slug" },
                    { key: "department_type", label: "نوع", render: (v: string) => (
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${v === "degree" ? "bg-green-100 text-green-700" : "bg-gray-100 text-gray-600"}`}>
                        {v === "degree" ? "فارغ‌ده" : "خدماتی"}
                      </span>
                    )},
                    { key: "duration_years", label: "مدت", render: (v: number) => `${v} سال` },
                  ]}
                  data={items}
                />
              )}

              {/* News */}
              {tab === "news" && (
                <DataTable
                  columns={[
                    { key: "title_fa", label: "عنوان" },
                    { key: "is_published", label: "وضعیت", render: (v: boolean) => (
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${v ? "bg-green-100 text-green-700" : "bg-yellow-100 text-yellow-700"}`}>
                        {v ? "منتشر شده" : "پیش‌نویس"}
                      </span>
                    )},
                  ]}
                  data={items}
                />
              )}

              {/* FAQs */}
              {tab === "faqs" && (
                <DataTable
                  columns={[
                    { key: "question_fa", label: "سوال" },
                    { key: "category", label: "دسته", render: (v: string) => v || "-" },
                  ]}
                  data={items}
                />
              )}

              {/* Exams */}
              {tab === "exams" && (
                <DataTable
                  columns={[
                    { key: "title_fa", label: "عنوان" },
                    { key: "total_questions", label: "سوالات" },
                    { key: "duration_minutes", label: "مدت", render: (v: number) => `${v} دقیقه` },
                    { key: "passing_score", label: "قبولی", render: (v: number) => `${v}%` },
                  ]}
                  data={items}
                />
              )}

              {/* Questions */}
              {tab === "questions" && (
                <DataTable
                  columns={[
                    { key: "subject", label: "موضوع", render: (v: string) => (
                      <span className="px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-700">{v}</span>
                    )},
                    { key: "difficulty", label: "سطح", render: (v: string) => (
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                        v === "easy" ? "bg-green-100 text-green-700" :
                        v === "hard" ? "bg-red-100 text-red-700" :
                        "bg-yellow-100 text-yellow-700"
                      }`}>{v}</span>
                    )},
                    { key: "question_fa", label: "سوال" },
                  ]}
                  data={items}
                />
              )}

              {/* Results */}
              {tab === "results" && (
                <DataTable
                  columns={[
                    { key: "score", label: "نمره", render: (v: number) => <span className="font-bold">{v}%</span> },
                    { key: "correct_answers", label: "درست", render: (v: number) => <span className="text-green-600">{v}</span> },
                    { key: "wrong_answers", label: "نادرست", render: (v: number) => <span className="text-red-600">{v}</span> },
                    { key: "passed", label: "وضعیت", render: (v: boolean) => (
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${v ? "bg-green-100 text-green-700" : "bg-red-100 text-red-700"}`}>
                        {v ? "قبول" : "مردود"}
                      </span>
                    )},
                  ]}
                  data={items}
                />
              )}

              {/* Notifications */}
              {tab === "notifications" && (
                <DataTable
                  columns={[
                    { key: "title_fa", label: "عنوان" },
                    { key: "event_date", label: "تاریخ", render: (v: string) => new Date(v).toLocaleDateString("fa-AF") },
                    { key: "event_type", label: "نوع", render: (v: string) => (
                      <span className="px-2 py-1 rounded-full text-xs font-medium bg-purple-100 text-purple-700">{v}</span>
                    )},
                  ]}
                  data={items}
                />
              )}
            </div>
          )}
        </div>
      </main>
      <Footer />
    </>
  );
}
