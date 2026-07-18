"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Header } from "../../components/layout/Header";
import { Footer } from "../../components/layout/Footer";
import { Button, Card, SectionTitle, Badge } from "../../components/ui";
import { API_BASE } from "../../lib/config";

interface SubjectScore {
  correct: number;
  total: number;
  percentage: number;
}

interface ExamResult {
  session_id: string;
  score: number;
  score_360?: number;
  correct_answers: number;
  wrong_answers: number;
  empty_answers: number;
  total_answers: number;
  subject_scores: Record<string, SubjectScore>;
  passed: boolean;
  time_taken_seconds: number | null;
  new_badges: string[];
}

export default function MockResultPage() {
  const router = useRouter();
  const [result, setResult] = useState<ExamResult | null>(null);
  const [studyPlan, setStudyPlan] = useState<string | null>(null);
  const [loadingPlan, setLoadingPlan] = useState(false);

  useEffect(() => {
    const saved = localStorage.getItem("mock_exam_result");
    if (!saved) {
      router.push("/mock-kankor");
      return;
    }
    setResult(JSON.parse(saved));
  }, [router]);

  const generateStudyPlan = async () => {
    if (!result) return;
    setLoadingPlan(true);
    try {
      const res = await fetch(`${API_BASE}/ai/study-plan`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ session_id: result.session_id }),
      });
      if (res.ok) {
        const data = await res.json();
        setStudyPlan(data.plan);
      }
    } catch {}
    setLoadingPlan(false);
  };

  if (!result) {
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

  const scoreColor = result.score >= 70 ? "text-success" : result.score >= 50 ? "text-warning" : "text-danger";
  const scoreBadge = result.score >= 70 ? "success" : result.score >= 50 ? "warning" : "danger";
  const formatTime = (s: number) => {
    const m = Math.floor(s / 60);
    const sec = s % 60;
    return `${m} دقیقه و ${sec} ثانیه`;
  };

  // Calculate stats
  const totalCorrect = result.correct_answers;
  const totalWrong = result.wrong_answers;
  const totalEmpty = result.empty_answers;
  const accuracy = result.total_answers > 0 ? Math.round((totalCorrect / result.total_answers) * 100) : 0;

  return (
    <>
      <Header />
      <main className="flex-1 py-12">
        <div className="max-w-3xl mx-auto px-4">
          <SectionTitle title="نتیجه کانکور آزمایشی" />

          {/* Score card */}
          <Card className="mb-8 text-center relative overflow-hidden">
            <div className="absolute top-0 left-0 right-0 h-2 bg-gradient-to-r from-primary-500 via-accent-500 to-gold-500" />
            <div className="pt-4">
              <div className={`text-7xl font-bold ${scoreColor} mb-2`}>{result.score}%</div>
              {result.score_360 !== undefined && (
                <p className="text-foreground text-xl font-bold mb-2">
                  نمره تخمینی کانکور: <span className={scoreColor}>{result.score_360}</span> از ۳۶۰
                </p>
              )}
              <Badge variant={scoreBadge} className="text-lg px-4 py-1">
                {result.passed ? "قبول" : "نیاز به تلاش بیشتر"}
              </Badge>
            </div>
          </Card>

          {/* Stats grid */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
            <Card className="text-center">
              <div className="text-3xl font-bold text-success">{totalCorrect}</div>
              <p className="text-muted text-sm mt-1">درست</p>
            </Card>
            <Card className="text-center">
              <div className="text-3xl font-bold text-danger">{totalWrong}</div>
              <p className="text-muted text-sm mt-1">نادرست</p>
            </Card>
            <Card className="text-center">
              <div className="text-3xl font-bold text-muted">{totalEmpty}</div>
              <p className="text-muted text-sm mt-1">بی‌پاسخ</p>
            </Card>
            <Card className="text-center">
              <div className="text-3xl font-bold text-primary-600">{accuracy}%</div>
              <p className="text-muted text-sm mt-1">دقت</p>
            </Card>
          </div>

          {result.time_taken_seconds && (
            <Card className="mb-8 text-center">
              <p className="text-muted">زمان: <span className="font-bold text-foreground">{formatTime(result.time_taken_seconds)}</span></p>
            </Card>
          )}

          {/* New badges */}
          {result.new_badges && result.new_badges.length > 0 && (
            <Card className="mb-8 bg-gold-500/10 border-gold-500/30">
              <h3 className="font-bold text-lg text-foreground mb-3">🏅 نشان جدید گرفتی!</h3>
              <div className="flex flex-wrap gap-3">
                {result.new_badges.map((badge: string) => (
                  <span key={badge} className="px-4 py-2 bg-gold-500/20 text-gold-600 rounded-full text-sm font-medium">
                    {badge.replace(/_/g, " ")}
                  </span>
                ))}
              </div>
            </Card>
          )}

          {/* Subject breakdown */}
          {Object.keys(result.subject_scores).length > 0 && (
            <Card className="mb-8">
              <h3 className="font-bold text-lg text-foreground mb-4">تفکیک مضامین</h3>
              <div className="space-y-4">
                {Object.entries(result.subject_scores)
                  .sort(([, a], [, b]) => b.percentage - a.percentage)
                  .map(([subj, data]) => (
                  <div key={subj}>
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-foreground font-medium">{subj}</span>
                      <span className="text-muted text-sm">{data.correct}/{data.total} ({data.percentage}%)</span>
                    </div>
                    <div className="h-4 bg-border rounded-full overflow-hidden">
                      <div
                        className={`h-full rounded-full transition-all duration-700 ${
                          data.percentage >= 70 ? "bg-success" : data.percentage >= 50 ? "bg-warning" : "bg-danger"
                        }`}
                        style={{ width: `${data.percentage}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </Card>
          )}

          {/* Actions */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-8">
            <Link href={`/mock-kankor/review?session=${result.session_id}`}>
              <Button variant="outline" size="lg" className="w-full">
                مرور پاسخ‌ها
              </Button>
            </Link>
            <Link href="/kankor/chance">
              <Button size="lg" className="w-full">
                ⭐ چانس قبولی با این نمره
              </Button>
            </Link>
          </div>

          {/* Study Plan */}
          <Card className="mb-8">
            <h3 className="font-bold text-lg text-foreground mb-3">📅 برنامه مطالعه شخصی</h3>
            {studyPlan ? (
              <div className="text-foreground whitespace-pre-line leading-relaxed">{studyPlan}</div>
            ) : (
              <div className="text-center">
                <p className="text-muted mb-4">برنامه مطالعه شخصی بر اساس نقاط ضعف شما بسازید</p>
                <Button onClick={generateStudyPlan} loading={loadingPlan} variant="outline">
                  ساخت برنامه مطالعه
                </Button>
              </div>
            )}
          </Card>

          {/* Disclaimer */}
          <div className="bg-warning/10 border border-warning/20 rounded-[10px] p-4 text-sm text-foreground text-center">
            ⚠️ محاسبه چانس قبولی بر اساس نمرات قبولی <strong>آخرین سال موجود در سیستم</strong> انجام می‌شود. نمره قبولی هر رشته <strong>هر سال متفاوت</strong> است و این نتیجه فقط یک تخمین است.
          </div>

          <div className="text-center mt-6">
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
