"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Header } from "../components/layout/Header";
import { Footer } from "../components/layout/Footer";
import { Button, Card, SectionTitle, Badge } from "../components/ui";
import { API_BASE } from "../lib/config";

const EXAM_OPTIONS = [
  {
    id: "full",
    title: "کانکور آزمایشی کامل",
    desc: "تمام مضامین — ۱۶۰ سوال — ۱۶۰ دقیقه",
    icon: "📝",
    questions: 160,
    minutes: 160,
  },
  {
    id: "math",
    title: "آزمون ریاضی",
    desc: "فقط ریاضی — ۳۰ سوال — ۳۰ دقیقه",
    icon: "🔢",
    questions: 30,
    minutes: 30,
    subject: "ریاضی",
  },
  {
    id: "physics",
    title: "آزمون فیزیک",
    desc: "فقط فیزیک — ۲۵ سوال — ۲۵ دقیقه",
    icon: "⚛️",
    questions: 25,
    minutes: 25,
    subject: "فزیک",
  },
  {
    id: "biology",
    title: "آزمون بیولوژی",
    desc: "فقط بیولوژی — ۲۰ سوال — ۲۰ دقیقه",
    icon: "🧬",
    questions: 20,
    minutes: 20,
    subject: "بیولوژی",
  },
  {
    id: "chemistry",
    title: "آزمون کیمیا",
    desc: "فقط کیمیا — ۲۰ سوال — ۲۰ دقیقه",
    icon: "🧪",
    questions: 20,
    minutes: 20,
    subject: "کیمیا",
  },
];

type Blueprint = {
  id: string;
  name_fa: string;
  description_fa: string | null;
  total_minutes: number;
  sections: { subject: string; count: number }[];
};

export default function MockKankorPage() {
  const router = useRouter();
  const [selected, setSelected] = useState<string | null>(null);
  const [starting, setStarting] = useState(false);
  const [error, setError] = useState("");
  const [fullBlueprint, setFullBlueprint] = useState<Blueprint | null>(null);

  // If an admin has configured a real exam blueprint (per-subject section
  // counts), use it for the "full" exam instead of flat random sampling —
  // otherwise fall back to today's behavior so nothing breaks.
  useEffect(() => {
    fetch(`${API_BASE}/mock-kankor/blueprints`)
      .then((r) => (r.ok ? r.json() : []))
      .then((list: Blueprint[]) => setFullBlueprint(Array.isArray(list) && list.length > 0 ? list[0] : null))
      .catch(() => setFullBlueprint(null));
  }, []);

  const examOptions = fullBlueprint
    ? EXAM_OPTIONS.map((o) => o.id === "full"
        ? {
            ...o,
            title: fullBlueprint.name_fa,
            desc: `${fullBlueprint.description_fa || "تمام مضامین بر اساس ساختار رسمی"} — ${fullBlueprint.sections.reduce((s, x) => s + x.count, 0)} سوال — ${fullBlueprint.total_minutes} دقیقه`,
            questions: fullBlueprint.sections.reduce((s, x) => s + x.count, 0),
            minutes: fullBlueprint.total_minutes,
          }
        : o)
    : EXAM_OPTIONS;

  const handleStart = async () => {
    const opt = examOptions.find((o) => o.id === selected);
    if (!opt) return;

    setStarting(true);
    setError("");

    const sessionId = crypto.randomUUID();
    try {
      const res = await fetch(`${API_BASE}/mock-kankor/start`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          session_id: sessionId,
          subject: opt.subject || null,
          num_questions: opt.questions,
          blueprint_id: opt.id === "full" && fullBlueprint ? fullBlueprint.id : null,
        }),
      });

      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.detail || "خطا در شروع آزمون");
      }

      const data = await res.json();

      // Save to localStorage for the exam page
      localStorage.setItem("mock_exam", JSON.stringify({
        sessionId: data.session_id,
        questions: data.questions,
        totalMinutes: data.total_minutes || opt.minutes,
        startedAt: Date.now(),
        examType: opt.id,
      }));

      router.push("/mock-kankor/exam");
    } catch (e: any) {
      setError(e.message || "خطا در شروع آزمون");
    }
    setStarting(false);
  };

  return (
    <>
      <Header />
      <main className="flex-1 py-12">
        <div className="max-w-3xl mx-auto px-4">
          <SectionTitle
            title="⭐ کانکور آزمایشی"
            subtitle=".similar to the real Kankor exam — practice with real questions"
          />

          <div className="bg-warning/10 border border-warning/20 rounded-[10px] p-4 mb-8 text-sm text-foreground">
            ⚠️ این آزمون بر اساس سوالات واقعی کانکور سال‌های گذشته است. نمره شما تخمینی از عملکرد واقعی شما در کانکور است.
          </div>

          <div className="space-y-4">
            {examOptions.map((opt) => (
              <div
                key={opt.id}
                onClick={() => setSelected(opt.id)}
                className={`cursor-pointer transition-all ${selected === opt.id ? "ring-2 ring-primary-500 rounded-[16px]" : ""}`}
              >
                <Card clickable>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-4">
                      <span className="text-3xl">{opt.icon}</span>
                      <div>
                        <h3 className="font-bold text-lg text-foreground">{opt.title}</h3>
                        <p className="text-muted text-sm">{opt.desc}</p>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <Badge variant="neutral">{opt.questions} سوال</Badge>
                      <Badge variant="neutral">{opt.minutes} دقیقه</Badge>
                    </div>
                  </div>
                </Card>
              </div>
            ))}
          </div>

          {error && (
            <div className="bg-danger/10 border border-danger/20 rounded-[10px] p-4 mt-6 text-sm text-danger">
              {error}
            </div>
          )}

          <div className="mt-8 text-center">
            <Button
              size="lg"
              onClick={handleStart}
              loading={starting}
              disabled={!selected}
            >
              شروع آزمون
            </Button>
          </div>

          {/* History link */}
          <div className="mt-6 text-center">
            <a href="/mock-kankor/history" className="text-primary-600 hover:text-primary-700 text-sm">
              مشاهده تاریخچه آزمون‌ها
            </a>
          </div>
        </div>
      </main>
      <Footer />
    </>
  );
}
