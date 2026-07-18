"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { Header } from "../components/layout/Header";
import { Footer } from "../components/layout/Footer";
import { Card, Button, Badge, SectionTitle } from "../components/ui";

import { API_BASE } from "../lib/config";
const API = API_BASE;

interface Exam {
  id: string;
  title_fa: string;
  title_en: string | null;
  category: string;
  year: number | null;
  duration_minutes: number;
  total_questions: number;
  passing_score: number;
}

interface Question {
  id: string;
  question_fa: string;
  options: { id: string; text_fa: string }[];
  subject: string;
  sort_order: number;
}

interface ExamResult {
  score: number;
  correct_answers: number;
  wrong_answers: number;
  empty_answers: number;
  total_answers: number;
  passed: boolean;
  passing_score: number;
  subject_scores: Record<string, { correct: number; total: number; percentage: number }>;
  time_taken_seconds: number;
}

export default function ExamPage() {
  const [exams, setExams] = useState<Exam[]>([]);
  const [selectedExam, setSelectedExam] = useState<Exam | null>(null);
  const [questions, setQuestions] = useState<Question[]>([]);
  const [currentQ, setCurrentQ] = useState(0);
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [result, setResult] = useState<ExamResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [startTime, setStartTime] = useState<number>(0);

  useEffect(() => {
    fetch(`${API}/exam`)
      .then((r) => r.json())
      .then(setExams)
      .catch(() => {});
  }, []);

  const startExam = async (exam: Exam) => {
    setLoading(true);
    try {
      const res = await fetch(`${API}/exam/${exam.id}`);
      const data = await res.json();
      setSelectedExam(exam);
      setQuestions(data.questions);
      setCurrentQ(0);
      setAnswers({});
      setResult(null);
      setStartTime(Date.now());
    } catch (e) {
      console.error(e);
    }
    setLoading(false);
  };

  const selectAnswer = (questionId: string, optionId: string) => {
    setAnswers((prev) => ({ ...prev, [questionId]: optionId }));
  };

  const submitExam = async () => {
    if (!selectedExam) return;
    setLoading(true);
    try {
      const res = await fetch(`${API}/exam/${selectedExam.id}/submit`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          session_id: localStorage.getItem("session_id") || crypto.randomUUID(),
          answers,
          time_taken_seconds: Math.floor((Date.now() - startTime) / 1000),
        }),
      });
      setResult(await res.json());
    } catch (e) {
      console.error(e);
    }
    setLoading(false);
  };

  // Results view
  if (result) {
    return (
      <>
        <Header />
        <main className="flex-1 py-12">
          <div className="max-w-3xl mx-auto px-4">
            <SectionTitle title="نتیجه امتحان" />

            <Card className="mb-6">
              <div className="text-center mb-6">
                <div className={`text-6xl font-bold mb-2 ${result.passed ? "text-success" : "text-danger"}`}>
                  {result.score}%
                </div>
                <Badge variant={result.passed ? "success" : "danger"}>
                  {result.passed ? "✅ قبول شدید" : "❌ مردود"}
                </Badge>
                <p className="text-muted mt-2">
                  نمره قبولی: {result.passing_score}%
                </p>
              </div>

              <div className="grid grid-cols-3 gap-4 mb-6">
                <div className="text-center p-3 bg-success/10 rounded-lg">
                  <div className="text-2xl font-bold text-success">{result.correct_answers}</div>
                  <div className="text-sm text-muted">درست</div>
                </div>
                <div className="text-center p-3 bg-danger/10 rounded-lg">
                  <div className="text-2xl font-bold text-danger">{result.wrong_answers}</div>
                  <div className="text-sm text-muted">نادرست</div>
                </div>
                <div className="text-center p-3 bg-warning/10 rounded-lg">
                  <div className="text-2xl font-bold text-warning">{result.empty_answers}</div>
                  <div className="text-sm text-muted">خالی</div>
                </div>
              </div>

              {result.time_taken_seconds && (
                <p className="text-center text-muted">
                  زمان: {Math.floor(result.time_taken_seconds / 60)} دقیقه و {result.time_taken_seconds % 60} ثانیه
                </p>
              )}
            </Card>

            {/* Subject breakdown */}
            {Object.keys(result.subject_scores).length > 0 && (
              <Card className="mb-6">
                <h3 className="font-bold mb-3">نمره به تفکیک موضوع</h3>
                <div className="space-y-2">
                  {Object.entries(result.subject_scores).map(([subj, data]) => (
                    <div key={subj} className="flex items-center justify-between">
                      <span>{subj}</span>
                      <div className="flex items-center gap-2">
                        <div className="w-32 h-2 bg-border rounded-full overflow-hidden">
                          <div
                            className="h-full bg-primary-500 rounded-full"
                            style={{ width: `${data.percentage}%` }}
                          />
                        </div>
                        <span className="text-sm font-bold">{data.percentage}%</span>
                      </div>
                    </div>
                  ))}
                </div>
              </Card>
            )}

            <div className="flex gap-4 justify-center">
              <Button onClick={() => { setResult(null); setSelectedExam(null); setQuestions([]); }}>
                امتحان جدید
              </Button>
              <Link href="/exam">
                <Button variant="outline">بازگشت به لیست</Button>
              </Link>
            </div>
          </div>
        </main>
        <Footer />
      </>
    );
  }

  // Exam taking view
  if (selectedExam && questions.length > 0) {
    const q = questions[currentQ];
    const progress = ((currentQ + 1) / questions.length) * 100;

    return (
      <>
        <Header />
        <main className="flex-1 py-12">
          <div className="max-w-3xl mx-auto px-4">
            {/* Progress */}
            <div className="mb-6">
              <div className="flex justify-between text-sm text-muted mb-2">
                <span>سوال {currentQ + 1} از {questions.length}</span>
                <Badge variant="neutral">{q.subject}</Badge>
              </div>
              <div className="h-2 bg-border rounded-full overflow-hidden">
                <div className="h-full bg-primary-500 rounded-full transition-all" style={{ width: `${progress}%` }} />
              </div>
            </div>

            {/* Question */}
            <Card className="mb-6">
              <h2 className="text-xl font-bold text-foreground mb-6">{q.question_fa}</h2>
              <div className="space-y-3">
                {q.options.map((opt) => (
                  <button
                    key={opt.id}
                    onClick={() => selectAnswer(q.id, opt.id)}
                    className={`w-full text-right px-5 py-4 rounded-[10px] border-2 transition-all duration-200 text-foreground font-medium ${
                      answers[q.id] === opt.id
                        ? "border-primary-500 bg-primary-50"
                        : "border-border hover:border-primary-300"
                    }`}
                  >
                    {opt.text_fa}
                  </button>
                ))}
              </div>
            </Card>

            {/* Navigation */}
            <div className="flex justify-between">
              <Button
                variant="outline"
                onClick={() => setCurrentQ((p) => Math.max(0, p - 1))}
                disabled={currentQ === 0}
              >
                قبلی
              </Button>
              {currentQ < questions.length - 1 ? (
                <Button onClick={() => setCurrentQ((p) => p + 1)}>
                  بعدی
                </Button>
              ) : (
                <Button onClick={submitExam} loading={loading} variant="gold">
                  🎯 ارسال و دریافت نمره
                </Button>
              )}
            </div>

            {/* Answer summary */}
            <div className="mt-6 flex flex-wrap gap-2">
              {questions.map((q, i) => (
                <div
                  key={q.id}
                  onClick={() => setCurrentQ(i)}
                  className={`w-8 h-8 rounded-full flex items-center justify-center text-sm cursor-pointer transition-all ${
                    answers[q.id]
                      ? i === currentQ
                        ? "bg-primary-600 text-white"
                        : "bg-primary-200 text-primary-700"
                      : i === currentQ
                      ? "bg-gray-400 text-white"
                      : "bg-gray-200 text-gray-600"
                  }`}
                >
                  {i + 1}
                </div>
              ))}
            </div>
          </div>
        </main>
        <Footer />
      </>
    );
  }

  // Exam list view
  return (
    <>
      <Header />
      <main className="flex-1 py-12">
        <div className="max-w-7xl mx-auto px-4">
          <SectionTitle title="امتحانات" subtitle="تست بدهید و نمره بگیرید" />

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {exams.map((exam) => (
              <Card key={exam.id} clickable>
                <div className="flex items-start justify-between mb-3">
                  <h3 className="font-bold text-lg">{exam.title_fa}</h3>
                  <Badge variant="neutral">{exam.category}</Badge>
                </div>
                {exam.title_en && <p className="text-muted text-sm mb-3">{exam.title_en}</p>}
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-muted">سوالات:</span>
                    <span>{exam.total_questions}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted">مدت:</span>
                    <span>{exam.duration_minutes} دقیقه</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted">نمره قبولی:</span>
                    <span>{exam.passing_score}%</span>
                  </div>
                  {exam.year && (
                    <div className="flex justify-between">
                      <span className="text-muted">سال:</span>
                      <span>{exam.year}</span>
                    </div>
                  )}
                </div>
                <Button
                  className="w-full mt-4"
                  onClick={() => startExam(exam)}
                  loading={loading}
                >
                  شروع امتحان
                </Button>
              </Card>
            ))}
          </div>
        </div>
      </main>
      <Footer />
    </>
  );
}
