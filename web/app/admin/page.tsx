"use client";

import { useState, useEffect } from "react";
import { Header } from "../components/layout/Header";
import { Footer } from "../components/layout/Footer";
import { Card, Button, Badge, SectionTitle } from "../components/ui";

const API = "http://localhost:9000/api/v1";

type Tab = "dashboard" | "universities" | "faculties" | "departments" | "news" | "faqs" | "exams" | "questions" | "results" | "users" | "notifications";

export default function AdminPage() {
  const [tab, setTab] = useState<Tab>("dashboard");
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  useEffect(() => {
    loadTab(tab);
  }, [tab]);

  const loadTab = async (t: Tab) => {
    setLoading(true);
    setMessage("");
    try {
      switch (t) {
        case "dashboard":
          const [uni, fac, dept, exam, qb, news, faq, notif] = await Promise.all([
            fetch(`${API}/universities`).then(r => r.json()),
            fetch(`${API}/faculties`).then(r => r.json()),
            fetch(`${API}/departments`).then(r => r.json()),
            fetch(`${API}/exam`).then(r => r.json()),
            fetch(`${API}/question-bank/stats`).then(r => r.json()),
            fetch(`${API}/news`).then(r => r.json()),
            fetch(`${API}/faqs`).then(r => r.json()),
            fetch(`${API}/notifications/events`).then(r => r.json()),
          ]);
          setData({ universities: uni, faculties: fac, departments: dept, exams: exam, questionBank: qb, news: news, faqs: faq, notifications: notif });
          break;
        case "universities":
          setData(await fetch(`${API}/universities`).then(r => r.json()));
          break;
        case "faculties":
          setData(await fetch(`${API}/faculties`).then(r => r.json()));
          break;
        case "departments":
          setData(await fetch(`${API}/departments`).then(r => r.json()));
          break;
        case "news":
          setData(await fetch(`${API}/news`).then(r => r.json()));
          break;
        case "faqs":
          setData(await fetch(`${API}/faqs`).then(r => r.json()));
          break;
        case "exams":
          setData(await fetch(`${API}/exam`).then(r => r.json()));
          break;
        case "questions":
          setData(await fetch(`${API}/question-bank/questions?limit=200`).then(r => r.json()));
          break;
        case "results":
          setData(await fetch(`${API}/exam/results/all`).then(r => r.json()).catch(() => []));
          break;
        case "users":
          setData(await fetch(`${API}/users/stats`).then(r => r.json()).catch(() => ({ total: 0 })));
          break;
        case "notifications":
          setData(await fetch(`${API}/notifications/events`).then(r => r.json()));
          break;
      }
    } catch (e) {
      console.error(e);
      setMessage("خطا در بارگذاری داده");
    }
    setLoading(false);
  };

  const tabs: { id: Tab; label: string; icon: string }[] = [
    { id: "dashboard", label: "داشبورد", icon: "📊" },
    { id: "universities", label: "پوهنتون‌ها", icon: "🏛️" },
    { id: "faculties", label: "پوهنځی‌ها", icon: "📚" },
    { id: "departments", label: "دیپارتمنت‌ها", icon: "🎓" },
    { id: "news", label: "اخبار", icon: "📰" },
    { id: "faqs", label: "FAQ", icon: "❓" },
    { id: "exams", label: "امتحانات", icon: "📝" },
    { id: "questions", label: "بانک سوالات", icon: "❓" },
    { id: "results", label: "نتایج", icon: "🏆" },
    { id: "notifications", label: "رویدادها", icon: "📅" },
  ];

  return (
    <>
      <Header />
      <main className="flex-1 py-6">
        <div className="max-w-7xl mx-auto px-4">
          <div className="flex items-center justify-between mb-6">
            <h1 className="text-2xl font-bold">پنل مدیریت</h1>
            <a href="http://localhost:9000/docs" target="_blank" className="text-primary-600 hover:underline text-sm">
              📄 Swagger API
            </a>
          </div>

          <div className="flex flex-wrap gap-2 mb-6">
            {tabs.map((t) => (
              <button
                key={t.id}
                onClick={() => setTab(t.id)}
                className={`px-3 py-2 rounded-lg text-sm font-medium transition-all ${
                  tab === t.id
                    ? "bg-primary-600 text-white shadow-md"
                    : "bg-white border border-border text-muted hover:bg-primary-50"
                }`}
              >
                {t.icon} {t.label}
              </button>
            ))}
          </div>

          {message && (
            <div className="bg-danger/10 border border-danger/20 rounded-lg p-3 mb-4 text-danger text-sm">
              {message}
            </div>
          )}

          {loading ? (
            <div className="text-center py-12 text-muted">در حال بارگذاری...</div>
          ) : (
            <>
              {/* Dashboard */}
              {tab === "dashboard" && data && (
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                  <Card><div className="text-center"><div className="text-3xl font-bold text-primary-600">{data.universities?.length || 0}</div><div className="text-muted text-sm">پوهنتون‌ها</div></div></Card>
                  <Card><div className="text-center"><div className="text-3xl font-bold text-primary-600">{data.faculties?.length || 0}</div><div className="text-muted text-sm">پوهنځی‌ها</div></div></Card>
                  <Card><div className="text-center"><div className="text-3xl font-bold text-primary-600">{data.departments?.length || 0}</div><div className="text-muted text-sm">دیپارتمنت‌ها</div></div></Card>
                  <Card><div className="text-center"><div className="text-3xl font-bold text-primary-600">{data.exams?.length || 0}</div><div className="text-muted text-sm">امتحانات</div></div></Card>
                  <Card><div className="text-center"><div className="text-3xl font-bold text-primary-600">{data.news?.length || 0}</div><div className="text-muted text-sm">اخبار</div></div></Card>
                  <Card><div className="text-center"><div className="text-3xl font-bold text-primary-600">{data.faqs?.length || 0}</div><div className="text-muted text-sm">FAQ</div></div></Card>
                  <Card><div className="text-center"><div className="text-3xl font-bold text-primary-600">{data.notifications?.length || 0}</div><div className="text-muted text-sm">رویدادها</div></div></Card>
                  <Card><div className="text-center"><div className="text-3xl font-bold text-accent-500">{data.questionBank?.total || 0}</div><div className="text-muted text-sm">سوالات</div></div></Card>
                </div>
              )}

              {/* Universities */}
              {tab === "universities" && data && (
                <Card>
                  <h3 className="font-bold mb-3">پوهنتون‌ها ({data.length})</h3>
                  <table className="w-full text-sm">
                    <thead><tr className="border-b"><th className="text-right p-2">نام</th><th className="text-right p-2">Slug</th><th className="text-right p-2">سال تأسیس</th></tr></thead>
                    <tbody>{data.map((u: any) => <tr key={u.id} className="border-b hover:bg-gray-50"><td className="p-2 font-medium">{u.name_fa}</td><td className="p-2 text-muted">{u.slug}</td><td className="p-2">{u.established_year}</td></tr>)}</tbody>
                  </table>
                </Card>
              )}

              {/* Faculties */}
              {tab === "faculties" && data && (
                <Card>
                  <h3 className="font-bold mb-3">پوهنځی‌ها ({data.length})</h3>
                  <table className="w-full text-sm">
                    <thead><tr className="border-b"><th className="text-right p-2">نام</th><th className="text-right p-2">Slug</th></tr></thead>
                    <tbody>{data.map((f: any) => <tr key={f.id} className="border-b hover:bg-gray-50"><td className="p-2 font-medium">{f.name_fa}</td><td className="p-2 text-muted">{f.slug}</td></tr>)}</tbody>
                  </table>
                </Card>
              )}

              {/* Departments */}
              {tab === "departments" && data && (
                <Card>
                  <h3 className="font-bold mb-3">دیپارتمنت‌ها ({data.length})</h3>
                  <div className="overflow-x-auto">
                    <table className="w-full text-sm">
                      <thead><tr className="border-b"><th className="text-right p-2">نام</th><th className="text-right p-2">Slug</th><th className="text-right p-2">نوع</th><th className="text-right p-2">مدت</th></tr></thead>
                      <tbody>{data.map((d: any) => <tr key={d.id} className="border-b hover:bg-gray-50"><td className="p-2 font-medium">{d.name_fa}</td><td className="p-2 text-muted">{d.slug}</td><td className="p-2"><Badge variant={d.department_type === "degree" ? "success" : "neutral"}>{d.department_type}</Badge></td><td className="p-2">{d.duration_years} سال</td></tr>)}</tbody>
                    </table>
                  </div>
                </Card>
              )}

              {/* News */}
              {tab === "news" && data && (
                <Card>
                  <h3 className="font-bold mb-3">اخبار ({data.length})</h3>
                  {data.length === 0 ? <p className="text-muted">خبری موجود نیست</p> : (
                    <table className="w-full text-sm">
                      <thead><tr className="border-b"><th className="text-right p-2">عنوان</th><th className="text-right p-2">وضعیت</th></tr></thead>
                      <tbody>{data.map((n: any) => <tr key={n.id} className="border-b hover:bg-gray-50"><td className="p-2">{n.title_fa}</td><td className="p-2"><Badge variant={n.is_published ? "success" : "warning"}>{n.is_published ? "منتشر شده" : "پیش‌نویس"}</Badge></td></tr>)}</tbody>
                    </table>
                  )}
                </Card>
              )}

              {/* FAQs */}
              {tab === "faqs" && data && (
                <Card>
                  <h3 className="font-bold mb-3">سوالات متداول ({data.length})</h3>
                  {data.length === 0 ? <p className="text-muted">سوالی موجود نیست</p> : (
                    <table className="w-full text-sm">
                      <thead><tr className="border-b"><th className="text-right p-2">سوال</th><th className="text-right p-2">دسته</th></tr></thead>
                      <tbody>{data.map((f: any) => <tr key={f.id} className="border-b hover:bg-gray-50"><td className="p-2">{f.question_fa}</td><td className="p-2"><Badge variant="neutral">{f.category || "-"}</Badge></td></tr>)}</tbody>
                    </table>
                  )}
                </Card>
              )}

              {/* Exams */}
              {tab === "exams" && data && (
                <Card>
                  <h3 className="font-bold mb-3">امتحانات ({data.length})</h3>
                  <table className="w-full text-sm">
                    <thead><tr className="border-b"><th className="text-right p-2">عنوان</th><th className="text-right p-2">سوالات</th><th className="text-right p-2">مدت</th><th className="text-right p-2">قبولی</th></tr></thead>
                    <tbody>{data.map((e: any) => <tr key={e.id} className="border-b hover:bg-gray-50"><td className="p-2 font-medium">{e.title_fa}</td><td className="p-2">{e.total_questions}</td><td className="p-2">{e.duration_minutes} دقیقه</td><td className="p-2">{e.passing_score}%</td></tr>)}</tbody>
                  </table>
                </Card>
              )}

              {/* Questions */}
              {tab === "questions" && data && (
                <Card>
                  <h3 className="font-bold mb-3">بانک سوالات ({data.length} سوال)</h3>
                  <div className="overflow-x-auto">
                    <table className="w-full text-sm">
                      <thead><tr className="border-b"><th className="text-right p-2">موضوع</th><th className="text-right p-2">سطح</th><th className="text-right p-2">سوال</th></tr></thead>
                      <tbody>{data.map((q: any) => <tr key={q.id} className="border-b hover:bg-gray-50"><td className="p-2"><Badge variant="neutral">{q.subject}</Badge></td><td className="p-2"><Badge variant={q.difficulty === "easy" ? "success" : q.difficulty === "hard" ? "danger" : "warning"}>{q.difficulty}</Badge></td><td className="p-2 max-w-md truncate">{q.question_fa}</td></tr>)}</tbody>
                    </table>
                  </div>
                </Card>
              )}

              {/* Results */}
              {tab === "results" && (
                <Card>
                  <h3 className="font-bold mb-3">نتایج امتحانات</h3>
                  {!data || data.length === 0 ? <p className="text-muted">هنوز نتیجه‌ای ثبت نشده</p> : (
                    <table className="w-full text-sm">
                      <thead><tr className="border-b"><th className="text-right p-2">نمره</th><th className="text-right p-2">درست</th><th className="text-right p-2">نادرست</th><th className="text-right p-2">وضعیت</th></tr></thead>
                      <tbody>{data.map((r: any) => <tr key={r.id} className="border-b hover:bg-gray-50"><td className="p-2 font-bold">{r.score}%</td><td className="p-2 text-success">{r.correct_answers}</td><td className="p-2 text-danger">{r.wrong_answers}</td><td className="p-2"><Badge variant={r.passed ? "success" : "danger"}>{r.passed ? "قبول" : "مردود"}</Badge></td></tr>)}</tbody>
                    </table>
                  )}
                </Card>
              )}

              {/* Notifications */}
              {tab === "notifications" && data && (
                <Card>
                  <h3 className="font-bold mb-3">رویدادها ({data.length})</h3>
                  {data.length === 0 ? <p className="text-muted">رویدادی موجود نیست</p> : (
                    <table className="w-full text-sm">
                      <thead><tr className="border-b"><th className="text-right p-2">عنوان</th><th className="text-right p-2">تاریخ</th><th className="text-right p-2">نوع</th></tr></thead>
                      <tbody>{data.map((e: any) => <tr key={e.id} className="border-b hover:bg-gray-50"><td className="p-2">{e.title_fa}</td><td className="p-2">{new Date(e.event_date).toLocaleDateString("fa-AF")}</td><td className="p-2"><Badge variant="neutral">{e.event_type}</Badge></td></tr>)}</tbody>
                    </table>
                  )}
                </Card>
              )}
            </>
          )}
        </div>
      </main>
      <Footer />
    </>
  );
}
