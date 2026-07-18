"use client";

import { useState, useEffect, Suspense } from "react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { Header } from "../../components/layout/Header";
import { Footer } from "../../components/layout/Footer";
import { Card, SectionTitle, Badge } from "../../components/ui";
import { API_BASE } from "../../lib/config";

interface ReviewQuestion {
  question_fa: string;
  subject: string;
  user_answer: string | null;
  correct_answer: string;
  is_correct: boolean;
  explanation: string | null;
  options: { text: string; is_correct?: boolean }[];
}

function MockReviewContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const sessionId = searchParams.get("session");
  const [questions, setQuestions] = useState<ReviewQuestion[]>([]);
  const [score, setScore] = useState(0);
  const [loading, setLoading] = useState(true);
  const [current, setCurrent] = useState(0);

  useEffect(() => {
    if (!sessionId) {
      router.push("/mock-kankor");
      return;
    }

    fetch(`${API_BASE}/mock-kankor/${sessionId}/review`)
      .then((r) => r.json())
      .then((data) => {
        setQuestions(data.questions || []);
        setScore(data.score || 0);
        setLoading(false);
      })
      .catch(() => {
        // Fallback: try to use result from localStorage
        const saved = localStorage.getItem("mock_exam_result");
        if (saved) {
          const result = JSON.parse(saved);
          setScore(result.score);
        }
        setLoading(false);
      });
  }, [sessionId, router]);

  if (loading) {
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

  if (questions.length === 0) {
    return (
      <>
        <Header />
        <main className="flex-1 py-12">
          <div className="max-w-3xl mx-auto px-4 text-center">
            <p className="text-muted mb-4">داده‌ای برای مرور موجود نیست</p>
            <Link href="/mock-kankor" className="text-primary-600 hover:text-primary-700">بازگشت</Link>
          </div>
        </main>
        <Footer />
      </>
    );
  }

  const q = questions[current];
  const correctCount = questions.filter((q) => q.is_correct).length;

  return (
    <>
      <Header />
      <main className="flex-1 py-12">
        <div className="max-w-3xl mx-auto px-4">
          <SectionTitle title="مرور پاسخ‌ها" subtitle={`${correctCount}/${questions.length} درست — نمره: ${score}%`} />

          {/* Navigation */}
          <div className="flex items-center justify-between mb-4">
            <span className="text-sm text-muted">سوال {current + 1} از {questions.length}</span>
            <div className="flex gap-2">
              <button onClick={() => setCurrent(Math.max(0, current - 1))} disabled={current === 0} className="px-3 py-1 rounded border border-border text-sm disabled:opacity-40">قبلی</button>
              <button onClick={() => setCurrent(Math.min(questions.length - 1, current + 1))} disabled={current === questions.length - 1} className="px-3 py-1 rounded border border-border text-sm disabled:opacity-40">بعدی</button>
            </div>
          </div>

          {/* Question */}
          <Card className="mb-6">
            <div className="flex items-center gap-2 mb-3">
              <Badge variant="neutral">{q.subject}</Badge>
              <Badge variant={q.is_correct ? "success" : "danger"}>
                {q.is_correct ? "✓ درست" : "✗ نادرست"}
              </Badge>
            </div>
            <h2 className="text-lg font-bold text-foreground mb-4">{q.question_fa}</h2>

            <div className="space-y-2">
              {q.options.map((opt, i) => {
                const isUserAnswer = opt.text === q.user_answer;
                const isCorrect = opt.is_correct;
                let bgClass = "bg-surface border-border";
                if (isCorrect) bgClass = "bg-success/10 border-success/30";
                if (isUserAnswer && !isCorrect) bgClass = "bg-danger/10 border-danger/30";

                return (
                  <div key={i} className={`px-4 py-3 rounded-[10px] border text-sm ${bgClass}`}>
                    <span className="font-medium ml-2">{String.fromCharCode(65 + i)}.</span>
                    {opt.text}
                    {isCorrect && <span className="text-success mr-2">✓</span>}
                    {isUserAnswer && !isCorrect && <span className="text-danger mr-2">✗ پاسخ شما</span>}
                  </div>
                );
              })}
            </div>

            {q.explanation && (
              <div className="mt-4 p-3 bg-primary-50 rounded-lg border border-primary-200">
                <p className="text-sm text-foreground"><strong>توضیح:</strong> {q.explanation}</p>
              </div>
            )}
          </Card>

          {/* Progress dots */}
          <div className="flex flex-wrap gap-1 justify-center mb-8">
            {questions.map((eq, i) => (
              <button
                key={i}
                onClick={() => setCurrent(i)}
                className={`w-8 h-8 rounded text-xs font-medium transition-all ${
                  i === current ? "ring-2 ring-primary-400 bg-primary-600 text-white" :
                  eq.is_correct ? "bg-success/10 text-success border border-success/30" :
                  "bg-danger/10 text-danger border border-danger/30"
                }`}
              >
                {i + 1}
              </button>
            ))}
          </div>

          <div className="text-center">
            <Link href="/mock-kankor" className="text-primary-600 hover:text-primary-700 text-sm">
              آزمون جدید بدهید
            </Link>
          </div>
        </div>
      </main>
      <Footer />
    </>
  );
}

export default function MockReviewPage() {
  return (
    <Suspense fallback={<div className="flex items-center justify-center py-12"><p className="text-muted">در حال بارگذاری...</p></div>}>
      <MockReviewContent />
    </Suspense>
  );
}
