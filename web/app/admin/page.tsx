"use client";

import { useState, useEffect } from "react";
import { Header } from "../components/layout/Header";
import { Footer } from "../components/layout/Footer";
import { Card, Button, SectionTitle, Badge } from "../components/ui";

const API = "http://localhost:9000/api/v1";

export default function AdminPage() {
  const [tab, setTab] = useState<"stats" | "questions" | "results" | "users">("stats");
  const [stats, setStats] = useState<any>(null);
  const [questions, setQuestions] = useState<any[]>([]);
  const [results, setResults] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    setLoading(true);
    try {
      const [uniRes, facRes, deptRes, examRes, qbRes] = await Promise.all([
        fetch(`${API}/universities`).then(r => r.json()),
        fetch(`${API}/faculties`).then(r => r.json()),
        fetch(`${API}/departments`).then(r => r.json()),
        fetch(`${API}/exam`).then(r => r.json()),
        fetch(`${API}/question-bank/stats`).then(r => r.json()),
      ]);
      setStats({
        universities: uniRes.length,
        faculties: facRes.length,
        departments: deptRes.length,
        exams: examRes.length,
        questionBank: qbRes,
      });
    } catch (e) {
      console.error(e);
    }
    setLoading(false);
  };

  const loadQuestions = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API}/question-bank/questions?limit=100`);
      setQuestions(await res.json());
    } catch (e) {
      console.error(e);
    }
    setLoading(false);
  };

  const loadResults = async () => {
    setLoading(true);
    try {
      // Get results for all sessions
      const res = await fetch(`${API}/exam/results/admin`);
      setResults(await res.json());
    } catch (e) {
      console.error(e);
    }
    setLoading(false);
  };

  return (
    <>
      <Header />
      <main className="flex-1 py-8">
        <div className="max-w-7xl mx-auto px-4">
          <div className="flex items-center justify-between mb-8">
            <h1 className="text-2xl font-bold">پنل مدیریت</h1>
            <a
              href="http://localhost:9000/admin"
              target="_blank"
              className="text-primary-600 hover:underline"
            >
              مدیریت محتوا (SQLAdmin) →
            </a>
          </div>

          {/* Tabs */}
          <div className="flex gap-2 mb-6 border-b pb-2">
            {[
              { id: "stats", label: "آمار کلی" },
              { id: "questions", label: "بانک سوالات" },
              { id: "results", label: "نتایج امتحانات" },
            ].map((t) => (
              <button
                key={t.id}
                onClick={() => {
                  setTab(t.id as any);
                  if (t.id === "questions") loadQuestions();
                  if (t.id === "results") loadResults();
                }}
                className={`px-4 py-2 rounded-t-lg font-medium ${
                  tab === t.id
                    ? "bg-primary-600 text-white"
                    : "bg-gray-100 text-gray-600 hover:bg-gray-200"
                }`}
              >
                {t.label}
              </button>
            ))}
          </div>

          {/* Stats Tab */}
          {tab === "stats" && (
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <Card>
                <div className="text-center">
                  <div className="text-3xl font-bold text-primary-600">
                    {stats?.universities || 0}
                  </div>
                  <div className="text-muted">پوهنتون‌ها</div>
                </div>
              </Card>
              <Card>
                <div className="text-center">
                  <div className="text-3xl font-bold text-primary-600">
                    {stats?.faculties || 0}
                  </div>
                  <div className="text-muted">پوهنځی‌ها</div>
                </div>
              </Card>
              <Card>
                <div className="text-center">
                  <div className="text-3xl font-bold text-primary-600">
                    {stats?.departments || 0}
                  </div>
                  <div className="text-muted">دیپارتمنت‌ها</div>
                </div>
              </Card>
              <Card>
                <div className="text-center">
                  <div className="text-3xl font-bold text-primary-600">
                    {stats?.exams || 0}
                  </div>
                  <div className="text-muted">امتحانات</div>
                </div>
              </Card>

              {/* Question Bank Stats */}
              {stats?.questionBank && (
                <div className="col-span-2 md:col-span-4">
                  <Card>
                    <h3 className="font-bold mb-3">بانک سوالات</h3>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
                      {Object.entries(stats.questionBank).map(([subject, count]) => (
                        <div key={subject} className="text-center p-2 bg-gray-50 rounded">
                          <div className="font-bold">{count as number}</div>
                          <div className="text-sm text-muted">{subject}</div>
                        </div>
                      ))}
                    </div>
                  </Card>
                </div>
              )}
            </div>
          )}

          {/* Questions Tab */}
          {tab === "questions" && (
            <Card>
              <div className="flex justify-between items-center mb-4">
                <h3 className="font-bold">سوالات بانک ({questions.length} سوال)</h3>
              </div>
              {loading ? (
                <p className="text-muted">در حال بارگذاری...</p>
              ) : (
                <div className="overflow-x-auto">
                  <table className="w-full text-sm">
                    <thead>
                      <tr className="border-b">
                        <th className="text-right p-2">موضوع</th>
                        <th className="text-right p-2">سطح</th>
                        <th className="text-right p-2">سوال</th>
                        <th className="text-right p-2">منبع</th>
                      </tr>
                    </thead>
                    <tbody>
                      {questions.map((q) => (
                        <tr key={q.id} className="border-b hover:bg-gray-50">
                          <td className="p-2">
                            <Badge variant="neutral">{q.subject}</Badge>
                          </td>
                          <td className="p-2">
                            <Badge
                              variant={
                                q.difficulty === "easy"
                                  ? "success"
                                  : q.difficulty === "hard"
                                  ? "danger"
                                  : "warning"
                              }
                            >
                              {q.difficulty}
                            </Badge>
                          </td>
                          <td className="p-2 max-w-md truncate">{q.question_fa}</td>
                          <td className="p-2 text-muted">{q.source || "-"}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </Card>
          )}

          {/* Results Tab */}
          {tab === "results" && (
            <Card>
              <h3 className="font-bold mb-4">نتایج امتحانات</h3>
              {loading ? (
                <p className="text-muted">در حال بارگذاری...</p>
              ) : results.length === 0 ? (
                <p className="text-muted">هنوز نتیجه‌ای ثبت نشده</p>
              ) : (
                <div className="overflow-x-auto">
                  <table className="w-full text-sm">
                    <thead>
                      <tr className="border-b">
                        <th className="text-right p-2">نمره</th>
                        <th className="text-right p-2">درست</th>
                        <th className="text-right p-2">نادرست</th>
                        <th className="text-right p-2">وضعیت</th>
                        <th className="text-right p-2">زمان</th>
                      </tr>
                    </thead>
                    <tbody>
                      {results.map((r) => (
                        <tr key={r.id} className="border-b hover:bg-gray-50">
                          <td className="p-2 font-bold">{r.score}%</td>
                          <td className="p-2 text-success">{r.correct_answers}</td>
                          <td className="p-2 text-danger">{r.wrong_answers}</td>
                          <td className="p-2">
                            <Badge variant={r.passed ? "success" : "danger"}>
                              {r.passed ? "قبول" : "مردود"}
                            </Badge>
                          </td>
                          <td className="p-2 text-muted">
                            {r.time_taken_seconds
                              ? `${Math.floor(r.time_taken_seconds / 60)} دقیقه`
                              : "-"}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </Card>
          )}
        </div>
      </main>
      <Footer />
    </>
  );
}
