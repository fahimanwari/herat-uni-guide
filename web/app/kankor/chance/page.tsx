"use client";

import { useState } from "react";
import { Header } from "../../components/layout/Header";
import { Footer } from "../../components/layout/Footer";
import { Button, Card, SectionTitle, Badge } from "../../components/ui";
import { API_BASE } from "../../lib/config";

interface ChanceResult {
  department_slug: string;
  department_name: string;
  chance: "high" | "medium" | "low";
  last_min_score: number;
  avg_min_score: number;
  trend: string;
  data_year?: number;
}

export default function ChancePage() {
  const [score, setScore] = useState("");
  const [results, setResults] = useState<ChanceResult[]>([]);
  const [loading, setLoading] = useState(false);

  const handleCalculate = async () => {
    if (!score) return;
    setLoading(true);
    try {
      const res = await fetch(
        `${API_BASE}/kankor/chances?score=${score}`
      );
      if (res.ok) {
        setResults(await res.json());
      }
    } catch {
      // Demo data for testing
      setResults([
        {
          department_slug: "computer-science",
          department_name: "کمپیوتر ساینس",
          chance: "high",
          last_min_score: 220,
          avg_min_score: 215,
          trend: "stable",
        },
        {
          department_slug: "engineering",
          department_name: "انجنیری",
          chance: "medium",
          last_min_score: 235,
          avg_min_score: 230,
          trend: "rising",
        },
      ]);
    }
    setLoading(false);
  };

  const chanceColors = {
    high: "success" as const,
    medium: "warning" as const,
    low: "danger" as const,
  };
  const chanceLabels = {
    high: "چانس بالا",
    medium: "چانس متوسط",
    low: "چانس پایین",
  };
  const trendLabels = {
    rising: "📈 رو به افزایش",
    stable: "➡️ پایدار",
    falling: "📉 رو به کاهش",
  };

  return (
    <>
      <Header />
      <main className="flex-1 py-12">
        <div className="max-w-3xl mx-auto px-4">
          <SectionTitle
            title="ماشین حساب چانس قبولی"
            subtitle="نمره تخمینی خود را وارد کنید"
          />

          {/* Input */}
          <Card className="mb-8">
            <label className="block text-sm font-medium text-muted mb-2">
              نمره تخمینی کانکور
            </label>
            <div className="flex gap-4">
              <input
                type="number"
                value={score}
                onChange={(e) => setScore(e.target.value)}
                placeholder="مثلاً 250"
                className="flex-1 px-4 py-3 rounded-[10px] border border-border bg-surface text-foreground text-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
              />
              <Button onClick={handleCalculate} loading={loading}>
                محاسبه کن
              </Button>
            </div>
          </Card>

          {/* Disclaimer — سال مبنای محاسبه از خود دیتا خوانده می‌شود */}
          <div className="bg-warning/10 border border-warning/20 rounded-[10px] p-4 mb-8 text-sm text-foreground">
            {results.length > 0 && results.some((r) => r.data_year) ? (
              <>
                ⚠️ این تخمین بر اساس نمرات قبولی <strong>سال {Math.max(...results.filter((r) => r.data_year).map((r) => r.data_year!))}</strong> است.
                نمره قبولی هر رشته <strong>هر سال متفاوت</strong> است (وابسته به تعداد داوطلبان و ظرفیت) — این نتیجه تضمین قبولی نیست.
              </>
            ) : (
              <>⚠️ این فقط تخمین بر اساس نمرات قبولی سال‌های گذشته است — نمره قبولی هر سال متفاوت است و تضمین قبولی نیست.</>
            )}
          </div>

          {/* Results */}
          {results.length > 0 && (
            <section>
              <SectionTitle title="نتایج" />
              <div className="space-y-4">
                {results.map((r) => (
                  <Card key={r.department_slug}>
                    <div className="flex items-center justify-between">
                      <div>
                        <h3 className="font-bold text-lg text-foreground">
                          {r.department_name}
                        </h3>
                        <p className="text-muted text-sm mt-1">
                          کات‌آف {r.data_year ? `سال ${r.data_year}` : "آخر"}: {r.last_min_score} | میانگین: {r.avg_min_score}
                        </p>
                        <p className="text-muted text-sm">
                          روند: {trendLabels[r.trend as keyof typeof trendLabels] || r.trend}
                        </p>
                      </div>
                      <Badge variant={chanceColors[r.chance]}>
                        {chanceLabels[r.chance]}
                      </Badge>
                    </div>
                  </Card>
                ))}
              </div>
            </section>
          )}
        </div>
      </main>
      <Footer />
    </>
  );
}
