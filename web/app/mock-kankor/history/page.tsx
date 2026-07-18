"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { Header } from "../../components/layout/Header";
import { Footer } from "../../components/layout/Footer";
import { Card, SectionTitle, Badge } from "../../components/ui";
import { API_BASE } from "../../lib/config";

interface HistoryItem {
  id: string;
  session_id: string;
  score: number | null;
  subject_scores: Record<string, any>;
  started_at: string;
  completed_at: string | null;
  time_taken_seconds: number | null;
}

export default function MockHistoryPage() {
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Get session ID from localStorage
    const mockExam = localStorage.getItem("mock_exam");
    const mockResult = localStorage.getItem("mock_exam_result");

    let sessionId = "";
    if (mockResult) {
      const r = JSON.parse(mockResult);
      sessionId = r.session_id;
    } else if (mockExam) {
      const e = JSON.parse(mockExam);
      sessionId = e.sessionId;
    }

    if (!sessionId) {
      setLoading(false);
      return;
    }

    fetch(`${API_BASE}/mock-kankor/history?session_id=${sessionId}`)
      .then((r) => r.json())
      .then((data) => {
        setHistory(Array.isArray(data) ? data : []);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  return (
    <>
      <Header />
      <main className="flex-1 py-12">
        <div className="max-w-3xl mx-auto px-4">
          <SectionTitle title="تاریخچه آزمون‌ها" />

          {loading ? (
            <p className="text-muted text-center py-8">در حال بارگذاری...</p>
          ) : history.length === 0 ? (
            <Card className="text-center py-8">
              <p className="text-muted mb-4">هنوز آزمونی نداده‌اید</p>
              <Link href="/mock-kankor" className="text-primary-600 hover:text-primary-700">
                اولین آزمون خود را شروع کنید
              </Link>
            </Card>
          ) : (
            <div className="space-y-4">
              {history.map((item) => (
                <Card key={item.id}>
                  <div className="flex items-center justify-between">
                    <div>
                      <div className="flex items-center gap-3 mb-1">
                        <span className="text-2xl font-bold text-primary-600">{item.score ?? "-"}%</span>
                        <Badge variant={item.score && item.score >= 50 ? "success" : "danger"}>
                          {item.score && item.score >= 50 ? "قبول" : "مردود"}
                        </Badge>
                      </div>
                      <p className="text-muted text-sm">
                        {new Date(item.started_at).toLocaleDateString("fa-AF")}
                        {item.time_taken_seconds && ` — ${Math.floor(item.time_taken_seconds / 60)} دقیقه`}
                      </p>
                    </div>
                    <Link
                      href={`/mock-kankor/review?session=${item.session_id}`}
                      className="text-primary-600 hover:text-primary-700 text-sm"
                    >
                      مرور →
                    </Link>
                  </div>
                </Card>
              ))}
            </div>
          )}
        </div>
      </main>
      <Footer />
    </>
  );
}
