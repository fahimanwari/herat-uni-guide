"use client";

import { useState, useEffect, useRef } from "react";
import { Header } from "../components/layout/Header";
import { Footer } from "../components/layout/Footer";
import { Button, Card, SectionTitle, Badge } from "../components/ui";
import { API_BASE } from "../lib/config";

interface Message {
  role: "user" | "assistant";
  content: string;
}

const INTERVIEW_FIELDS = [
  "مهندسی نرم‌افزار",
  "کمپیوتر ساینس",
  "-network",
  "دیتابیس",
  "نجوم",
  "eneral",
];

export default function InterviewPage() {
  const [field, setField] = useState("");
  const [started, setStarted] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const startInterview = async () => {
    if (!field) return;
    setStarted(true);
    setLoading(true);

    const systemMsg: Message = {
      role: "assistant",
      content: `سلام! من مصاحبه‌گر شما برای موقعیت "${field}" هستم.\n\nمن ۵ سوال از شما می‌پرسم. لطفاً به هر سوال با جزئیات پاسخ دهید.\n\nسوال ۱: لطفاً خودتان را معرفی کنید و بگویید چرا این موقعیت برای شما مناسب است.`,
    };
    setMessages([systemMsg]);
    setLoading(false);
  };

  const handleSend = async () => {
    if (!input.trim() || loading) return;

    const userMsg: Message = { role: "user", content: input };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch(`${API_BASE}/ai/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: `من در حال تمرین مصاحبه شغلی برای موقعیت "${field}" هستم. مصاحبه‌گر باش و سوالات مصاحبه بپرس.\n\nسوالات قبلی و پاسخ‌های من:\n${messages.map(m => `${m.role === "user" ? "من" : "مصاحبه‌گر"}: ${m.content}`).join("\n")}\n\nپاسخ اخیر من: ${input}\n\nاگر هنوز ۵ سوال نپرسیده‌ام، سوال بعدی را بپرس. اگر ۵ سوال پرسیده‌ام، بازخورد کلی بده.`,
          language: "fa",
          session_id: "interview-" + Date.now(),
        }),
      });

      if (res.ok) {
        const data = await res.json();
        setMessages((prev) => [...prev, { role: "assistant", content: data.response }]);
      }
    } catch {
      setMessages((prev) => [...prev, { role: "assistant", content: "متأسفانه خطا رخ داد. لطفاً دوباره تلاش کنید." }]);
    }
    setLoading(false);
  };

  if (!started) {
    return (
      <>
        <Header />
        <main className="flex-1 py-12">
          <div className="max-w-3xl mx-auto px-4">
            <SectionTitle title="تمرین مصاحبه شغلی" subtitle="با هوش مصنوعی تمرین کنید" />
            <Card>
              <p className="text-muted mb-6">رشته یا موقعیت شغلی مورد نظر خود را انتخاب کنید:</p>
              <div className="space-y-3">
                {INTERVIEW_FIELDS.map((f) => (
                  <button key={f} onClick={() => setField(f)} className={`w-full text-right px-4 py-3 rounded-[10px] border-2 transition-all ${field === f ? "border-primary-500 bg-primary-50" : "border-border hover:border-primary-300"}`}>
                    {f}
                  </button>
                ))}
              </div>
              <div className="mt-4">
                <label className="block text-sm font-medium text-muted mb-1">یا موقعیت دلخواه:</label>
                <input value={field && !INTERVIEW_FIELDS.includes(field) ? field : ""} onChange={(e) => setField(e.target.value)} className="w-full px-4 py-3 border border-border rounded-[10px] bg-surface text-foreground" placeholder="مثال: مدیر پروژه" />
              </div>
              <Button onClick={startInterview} disabled={!field} className="w-full mt-6">شروع مصاحبه</Button>
            </Card>
          </div>
        </main>
        <Footer />
      </>
    );
  }

  return (
    <>
      <Header />
      <main className="flex-1 py-12">
        <div className="max-w-2xl mx-auto px-4">
          <div className="flex items-center gap-2 mb-4">
            <Badge variant="neutral">تمرین مصاحبه</Badge>
            <Badge variant="neutral">{field}</Badge>
          </div>

          <Card className="mb-4 min-h-[400px] max-h-[500px] overflow-y-auto flex flex-col">
            <div className="flex-1 space-y-4">
              {messages.map((m, i) => (
                <div key={i} className={`flex ${m.role === "user" ? "justify-start" : "justify-end"}`}>
                  <div className={`max-w-[85%] px-4 py-3 rounded-2xl ${m.role === "user" ? "bg-primary-100 text-foreground rounded-br-sm" : "bg-accent-500 text-white rounded-bl-sm"}`}>
                    <p className="whitespace-pre-wrap">{m.content}</p>
                  </div>
                </div>
              ))}
              {loading && (
                <div className="flex justify-end">
                  <div className="bg-accent-500 text-white px-4 py-3 rounded-2xl rounded-bl-sm">
                    <span className="animate-pulse">در حال فکر کردن...</span>
                  </div>
                </div>
              )}
              <div ref={bottomRef} />
            </div>
          </Card>

          <div className="flex gap-2">
            <input value={input} onChange={(e) => setInput(e.target.value)} onKeyDown={(e) => e.key === "Enter" && handleSend()} placeholder="پاسخ خود را بنویسید..." disabled={loading} className="flex-1 px-4 py-3 rounded-[10px] border border-border bg-surface text-foreground focus:ring-2 focus:ring-primary-500 disabled:opacity-50" />
            <Button onClick={handleSend} loading={loading} disabled={!input.trim()}>ارسال</Button>
          </div>
        </div>
      </main>
      <Footer />
    </>
  );
}
