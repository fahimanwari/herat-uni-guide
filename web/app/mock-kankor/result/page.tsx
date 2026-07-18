"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Header } from "../../components/layout/Header";
import { Footer } from "../../components/layout/Footer";
import { Button, Card, SectionTitle, Badge } from "../../components/ui";

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

  useEffect(() => {
    const saved = localStorage.getItem("mock_exam_result");
    if (!saved) {
      router.push("/mock-kankor");
      return;
    }
    setResult(JSON.parse(saved));
  }, [router]);

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

  return (
    <>
      <Header />
      <main className="flex-1 py-12">
        <div className="max-w-3xl mx-auto px-4">
          <SectionTitle title="نتیجه کانکور آزمایشی" />

          {/* Score card */}
          <Card className="mb-8 text-center">
            <div className={`text-6xl font-bold ${scoreColor} mb-2`}>{result.score}%</div>
            {result.score_360 !== undefined && (
              <p className="text-foreground text-xl font-bold mb-2">
                نمره تخمینی کانکور: <span className={scoreColor}>{result.score_360}</span> از ۳۶۰
              </p>
            )}
            <Badge variant={scoreBadge} className="text-lg px-4 py-1">
              {result.passed ? "قبول" : "نیاز به تلاش بیشتر"}
            </Badge>
            <p className="text-muted mt-4">
              {result.correct_answers} درست | {result.wrong_answers} نادرست | {result.empty_answers} بی‌پاسخ
            </p>
            {result.time_taken_seconds && (
              <p className="text-muted text-sm mt-1">زمان: {formatTime(result.time_taken_seconds)}</p>
            )}
          </Card>

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
              <div className="space-y-3">
                {Object.entries(result.subject_scores).map(([subj, data]) => (
                  <div key={subj}>
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-foreground font-medium">{subj}</span>
                      <span className="text-muted text-sm">{data.correct}/{data.total} ({data.percentage}%)</span>
                    </div>
                    <div className="h-3 bg-border rounded-full overflow-hidden">
                      <div
                        className={`h-full rounded-full transition-all ${
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
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href={`/mock-kankor/review?session=${result.session_id}`}>
              <Button variant="outline" size="lg" className="w-full sm:w-auto">
                مرور پاسخ‌ها
              </Button>
            </Link>
            <Link href="/kankor/chance">
              <Button size="lg" className="w-full sm:w-auto">
                ⭐ چانس قبولی با این نمره
              </Button>
            </Link>
          </div>

          <div className="bg-warning/10 border border-warning/20 rounded-[10px] p-4 mt-6 text-sm text-foreground text-center">
            ⚠️ محاسبه چانس قبولی بر اساس نمرات قبولی <strong>آخرین سال موجود در سیستم</strong> انجام می‌شود
            (سال دقیق در صفحه چانس نمایش داده می‌شود). نمره قبولی هر رشته <strong>هر سال متفاوت</strong> است
            و این نتیجه فقط یک تخمین است، نه تضمین قبولی.
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
