"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { Header } from "../components/layout/Header";
import { Footer } from "../components/layout/Footer";
import { Button, Card, Badge, SectionTitle } from "../components/ui";
import { API_BASE } from "../lib/config";

interface QuizOption {
  id: string;
  text_fa: string;
}

interface QuizQuestion {
  id: string;
  question_fa: string;
  category: string | null;
  sort_order: number;
  options: QuizOption[];
}

interface QuizMatch {
  department_slug: string;
  department_name: string;
  percent: number;
}

export default function QuizPage() {
  const [questions, setQuestions] = useState<QuizQuestion[]>([]);
  const [current, setCurrent] = useState(0);
  const [answers, setAnswers] = useState<string[]>([]);
  const [results, setResults] = useState<QuizMatch[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetch(`${API_BASE}/quiz/questions`)
      .then((r) => r.json())
      .then(setQuestions)
      .catch(() => {
        // Demo questions
        setQuestions([
          {
            id: "1", question_fa: "كداميك از فعاليت‌ها براي شما جذاب‌تر است؟",
            category: "علایق", sort_order: 0,
            options: [
              { id: "1a", text_fa: "حل مسائل رياضي و منطقي" },
              { id: "1b", text_fa: "مطالعه متون ادبي و نوشتن" },
              { id: "1c", text_fa: "آزمايش در لابراتوار" },
              { id: "1d", text_fa: "کار با کامپیوتر و برنامه‌نویسي" },
            ],
          },
          {
            id: "2", question_fa: "كدام درس در مکتب براي شما آسان‌تر بود؟",
            category: "توانایی", sort_order: 1,
            options: [
              { id: "2a", text_fa: "رياضيات" },
              { id: "2b", text_fa: "ادبيات" },
              { id: "2c", text_fa: "علوم" },
              { id: "2d", text_fa: "زبان انگليسي" },
            ],
          },
        ]);
      });
  }, []);

  const handleAnswer = (optionId: string) => {
    const newAnswers = [...answers, optionId];
    setAnswers(newAnswers);

    if (current < questions.length - 1) {
      setCurrent(current + 1);
    } else {
      // Submit
      setLoading(true);
      fetch(`${API_BASE}/quiz/score`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ selected_option_ids: newAnswers }),
      })
        .then((r) => r.json())
        .then(setResults)
        .catch(() => {
          setResults([
            { department_slug: "software-engineering", department_name: "انجنیری نرم‌افزار", percent: 85 },
            { department_slug: "database-information-systems", department_name: "دیتابیس و سیستم‌های معلوماتی", percent: 72 },
            { department_slug: "network-information-technology", department_name: "نتورک و تکنالوژی معلوماتی", percent: 58 },
          ]);
        });
      setLoading(false);
    }
  };

  const progress = questions.length > 0 ? ((current + 1) / questions.length) * 100 : 0;

  // Results view
  if (results.length > 0) {
    return (
      <>
        <Header />
        <main className="flex-1 py-12">
          <div className="max-w-3xl mx-auto px-4">
            <SectionTitle title="نتایج آزمون" subtitle="۵ رشته برتر بر اساس علاقه‌مندی‌های شما" />

            <div className="space-y-4">
              {results.map((r, i) => (
                <Link key={r.department_slug} href={`/faculties/department/${r.department_slug}`}>
                  <Card clickable className="mb-4">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-4">
                        <span className="text-2xl font-bold text-primary-600">#{i + 1}</span>
                        <div>
                          <h3 className="font-bold text-lg text-foreground">{r.department_name}</h3>
                          <p className="text-muted text-sm">تطابق: {r.percent}%</p>
                        </div>
                      </div>
                      <div className="w-16 h-16 rounded-full bg-primary-100 flex items-center justify-center">
                        <span className="text-xl font-bold text-primary-600">{r.percent}%</span>
                      </div>
                    </div>
                    {/* Progress bar */}
                    <div className="mt-3 h-2 bg-border rounded-full overflow-hidden">
                      <div
                        className="h-full bg-primary-500 rounded-full transition-all"
                        style={{ width: `${r.percent}%` }}
                      />
                    </div>
                  </Card>
                </Link>
              ))}
            </div>

            <div className="mt-8 text-center">
              <Button variant="outline" onClick={() => { setResults([]); setCurrent(0); setAnswers([]); }}>
                دوباره آزمون بده
              </Button>
            </div>
          </div>
        </main>
        <Footer />
      </>
    );
  }

  // Quiz view
  if (questions.length === 0) {
    return (
      <>
        <Header />
        <main className="flex-1 py-12">
          <div className="max-w-3xl mx-auto px-4 text-center">
            <p className="text-muted">در حال بارگذاری سوالات...</p>
          </div>
        </main>
        <Footer />
      </>
    );
  }

  const q = questions[current];

  return (
    <>
      <Header />
      <main className="flex-1 py-12">
        <div className="max-w-3xl mx-auto px-4">
          {/* Progress */}
          <div className="mb-8">
            <div className="flex justify-between text-sm text-muted mb-2">
              <span>سوال {current + 1} از {questions.length}</span>
              {q.category && <Badge variant="neutral">{q.category}</Badge>}
            </div>
            <div className="h-2 bg-border rounded-full overflow-hidden">
              <div
                className="h-full bg-primary-500 rounded-full transition-all duration-300"
                style={{ width: `${progress}%` }}
              />
            </div>
          </div>

          {/* Question */}
          <Card className="mb-6">
            <h2 className="text-xl font-bold text-foreground mb-6">
              {q.question_fa}
            </h2>
            <div className="space-y-3">
              {q.options.map((opt) => (
                <button
                  key={opt.id}
                  onClick={() => handleAnswer(opt.id)}
                  className="w-full text-right px-5 py-4 rounded-[10px] border-2 border-border hover:border-primary-400 hover:bg-primary-50 transition-all duration-200 text-foreground font-medium"
                >
                  {opt.text_fa}
                </button>
              ))}
            </div>
          </Card>
        </div>
      </main>
      <Footer />
    </>
  );
}
