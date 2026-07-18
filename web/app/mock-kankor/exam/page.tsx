"use client";

import { useState, useEffect, useCallback } from "react";
import { useRouter } from "next/navigation";
import { Header } from "../../components/layout/Header";
import { Footer } from "../../components/layout/Footer";
import { Button, Card, Badge } from "../../components/ui";
import { API_BASE } from "../../lib/config";

interface ExamQuestion {
  id: string;
  question_fa: string;
  options: { id: string; text: string }[];
  subject: string;
  sort_order: number;
}

interface ExamData {
  sessionId: string;
  questions: ExamQuestion[];
  totalMinutes: number;
  startedAt: number;
  examType: string;
}

export default function MockExamPage() {
  const router = useRouter();
  const [exam, setExam] = useState<ExamData | null>(null);
  const [current, setCurrent] = useState(0);
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [marked, setMarked] = useState<Set<string>>(new Set());
  const [timeLeft, setTimeLeft] = useState(0);
  const [submitting, setSubmitting] = useState(false);

  // Load exam from localStorage
  useEffect(() => {
    const saved = localStorage.getItem("mock_exam");
    if (!saved) {
      router.push("/mock-kankor");
      return;
    }
    const data: ExamData = JSON.parse(saved);
    setExam(data);

    // Calculate remaining time
    const elapsed = Math.floor((Date.now() - data.startedAt) / 1000);
    const totalSeconds = data.totalMinutes * 60;
    const remaining = Math.max(0, totalSeconds - elapsed);
    setTimeLeft(remaining);

    // Load saved answers
    const savedAnswers = localStorage.getItem("mock_exam_answers");
    if (savedAnswers) {
      setAnswers(JSON.parse(savedAnswers));
    }
  }, [router]);

  // Timer
  useEffect(() => {
    if (timeLeft <= 0 && exam) {
      handleSubmit();
      return;
    }
    const timer = setInterval(() => {
      setTimeLeft((t) => {
        if (t <= 1) {
          clearInterval(timer);
          return 0;
        }
        return t - 1;
      });
    }, 1000);
    return () => clearInterval(timer);
  }, [timeLeft > 0, exam]);

  // Save answers to localStorage
  useEffect(() => {
    if (Object.keys(answers).length > 0) {
      localStorage.setItem("mock_exam_answers", JSON.stringify(answers));
    }
  }, [answers]);

  const handleAnswer = (questionId: string, optionId: string) => {
    setAnswers((prev) => ({ ...prev, [questionId]: optionId }));
  };

  const toggleMark = (questionId: string) => {
    setMarked((prev) => {
      const next = new Set(prev);
      if (next.has(questionId)) next.delete(questionId);
      else next.add(questionId);
      return next;
    });
  };

  const handleSubmit = async () => {
    if (submitting || !exam) return;
    setSubmitting(true);

    try {
      const res = await fetch(`${API_BASE}/mock-kankor/${exam.sessionId}/submit`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          answers,
          time_taken_seconds: Math.floor((Date.now() - exam.startedAt) / 1000),
        }),
      });

      if (!res.ok) throw new Error("خطا در ارسال");

      const result = await res.json();
      localStorage.setItem("mock_exam_result", JSON.stringify(result));
      localStorage.removeItem("mock_exam");
      localStorage.removeItem("mock_exam_answers");
      router.push("/mock-kankor/result");
    } catch {
      setSubmitting(false);
    }
  };

  if (!exam) {
    return (
      <>
        <Header />
        <main className="flex-1 flex items-center justify-center py-12">
          <p className="text-muted">در حال بارگذاری...</p>
        </main>
        <Footer />
      </>
    );
  }

  const q = exam.questions[current];
  const answered = Object.keys(answers).length;
  const total = exam.questions.length;
  const progress = ((current + 1) / total) * 100;

  const formatTime = (s: number) => {
    const h = Math.floor(s / 3600);
    const m = Math.floor((s % 3600) / 60);
    const sec = s % 60;
    return h > 0 ? `${h}:${String(m).padStart(2, "0")}:${String(sec).padStart(2, "0")}` : `${m}:${String(sec).padStart(2, "0")}`;
  };

  return (
    <>
      <Header />
      <main className="flex-1 py-4 md:py-8">
        <div className="max-w-4xl mx-auto px-4">
          {/* Top bar */}
          <div className="flex items-center justify-between mb-4 bg-surface-card rounded-xl border border-border p-3">
            <div className="flex items-center gap-4">
              <span className={`text-lg font-bold ${timeLeft < 300 ? "text-danger animate-pulse" : "text-foreground"}`}>
                ⏱ {formatTime(timeLeft)}
              </span>
              <span className="text-sm text-muted">{answered}/{total} پاسخ</span>
            </div>
            <Button size="sm" onClick={handleSubmit} loading={submitting} disabled={submitting}>
              پایان آزمون
            </Button>
          </div>

          {/* Progress */}
          <div className="h-2 bg-border rounded-full overflow-hidden mb-6">
            <div className="h-full bg-primary-500 rounded-full transition-all" style={{ width: `${progress}%` }} />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* Question */}
            <div className="md:col-span-2">
              <Card>
                <div className="flex items-center justify-between mb-4">
                  <Badge variant="neutral">{q.subject}</Badge>
                  <span className="text-sm text-muted">سوال {current + 1} از {total}</span>
                </div>
                <h2 className="text-lg font-bold text-foreground mb-6">{q.question_fa}</h2>
                <div className="space-y-3">
                  {q.options.map((opt, i) => (
                    <button
                      key={opt.id}
                      onClick={() => handleAnswer(q.id, opt.id)}
                      className={`w-full text-right px-5 py-4 rounded-[10px] border-2 transition-all duration-200 text-foreground font-medium ${
                        answers[q.id] === opt.id
                          ? "border-primary-500 bg-primary-50"
                          : "border-border hover:border-primary-300 hover:bg-surface"
                      }`}
                    >
                      <span className="text-muted ml-3">{String.fromCharCode(65 + i)}.</span>
                      {opt.text}
                    </button>
                  ))}
                </div>

                {/* Mark + Navigation */}
                <div className="flex items-center justify-between mt-6">
                  <button onClick={() => toggleMark(q.id)} className={`px-4 py-2 rounded-lg text-sm transition-colors ${marked.has(q.id) ? "bg-warning/10 text-warning border border-warning/30" : "text-muted hover:text-foreground border border-border"}`}>
                    {marked.has(q.id) ? "★ علامت‌گذاری شده" : "☆ علامت‌گذاری"}
                  </button>
                  <div className="flex gap-2">
                    <Button variant="outline" size="sm" onClick={() => setCurrent(Math.max(0, current - 1))} disabled={current === 0}>قبلی</Button>
                    <Button size="sm" onClick={() => setCurrent(Math.min(total - 1, current + 1))} disabled={current === total - 1}>بعدی</Button>
                  </div>
                </div>
              </Card>
            </div>

            {/* Question grid */}
            <div>
              <Card>
                <h3 className="font-bold text-foreground mb-3">شبکه سوالات</h3>
                <div className="grid grid-cols-5 gap-2">
                  {exam.questions.map((eq, i) => {
                    const isAnswered = !!answers[eq.id];
                    const isMarked = marked.has(eq.id);
                    const isCurrent = i === current;
                    return (
                      <button
                        key={eq.id}
                        onClick={() => setCurrent(i)}
                        className={`w-10 h-10 rounded-lg text-sm font-medium transition-all ${
                          isCurrent ? "bg-primary-600 text-white ring-2 ring-primary-400" :
                          isAnswered ? "bg-success/10 text-success border border-success/30" :
                          isMarked ? "bg-warning/10 text-warning border border-warning/30" :
                          "bg-surface border border-border text-muted hover:border-primary-400"
                        }`}
                      >
                        {i + 1}
                      </button>
                    );
                  })}
                </div>
                <div className="flex gap-4 mt-3 text-xs text-muted">
                  <span className="flex items-center gap-1"><span className="w-3 h-3 rounded bg-success/20 border border-success/40" /> پاسخ‌داده</span>
                  <span className="flex items-center gap-1"><span className="w-3 h-3 rounded bg-warning/20 border border-warning/40" /> علامت‌گذاری</span>
                </div>
              </Card>
            </div>
          </div>
        </div>
      </main>
      <Footer />
    </>
  );
}
