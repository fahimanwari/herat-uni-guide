"use client";

import { useState, useEffect, useRef } from "react";
import { Header } from "../components/layout/Header";
import { Footer } from "../components/layout/Footer";
import { Button, Card, Badge } from "../components/ui";
import { API_BASE } from "../lib/config";

interface Message {
  role: "user" | "assistant";
  content: string;
  cached?: boolean;
}

const SUGGESTIONS = [
  "کدام رشته مناسب من است؟",
  "شرایط کانکور چیست؟",
  "رشته کمپیوتر ساینس چطور است؟",
];

function getSessionId(): string {
  if (typeof window === "undefined") return "";
  let id = localStorage.getItem("chat_session_id");
  if (!id) {
    id = crypto.randomUUID();
    localStorage.setItem("chat_session_id", id);
  }
  return id;
}

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState("");
  const [booksMode, setBooksMode] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    setSessionId(getSessionId());
  }, []);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const handleSend = async (text?: string) => {
    const msg = text || input;
    if (!msg.trim() || loading) return;

    const userMsg: Message = { role: "user", content: msg };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch(`${API_BASE}/ai/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: msg,
          language: "fa",
          session_id: sessionId,
          mode: booksMode ? "book" : "general",
        }),
      });

      if (res.ok) {
        const data = await res.json();
        setMessages((prev) => [
          ...prev,
          { role: "assistant", content: data.response, cached: data.cached },
        ]);
      } else {
        throw new Error("API error");
      }
    } catch {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            "متأسفانه در حال حاضر قادر به پاسخگویی نیستم. لطفاً بعداً تلاش کنید یا با دانشگاه تماس بگیرید.",
        },
      ]);
    }
    setLoading(false);
  };

  return (
    <>
      <Header />
      <main className="flex-1 py-12">
        <div className="max-w-2xl mx-auto px-4">
          <h1 className="text-2xl md:text-3xl font-bold text-foreground mb-2 text-center">
            🤖 مشاور هوش مصنوعی
          </h1>
          <p className="text-muted text-center mb-6 text-sm">
            سوالات خود درباره پوهنتون هرات را بپرسید
          </p>

          {/* Books Mode Toggle */}
          <label className="flex items-center justify-center gap-2 text-sm text-muted cursor-pointer mb-4 p-3 rounded-lg border border-border bg-surface hover:bg-primary-50 transition-colors">
            <input
              type="checkbox"
              checked={booksMode}
              onChange={(e) => setBooksMode(e.target.checked)}
              className="w-4 h-4 text-primary-600 rounded"
            />
            فقط از کتاب‌های درسی جواب بده (با ذکر کتاب و صفحه)
          </label>

          {/* Chat Area */}
          <Card className="mb-4 min-h-[400px] max-h-[500px] overflow-y-auto flex flex-col">
            <div className="flex-1 space-y-4">
              {messages.length === 0 && (
                <div className="text-center py-8">
                  <p className="text-muted mb-6">از من بپرسید...</p>
                  <div className="flex flex-wrap gap-2 justify-center">
                    {SUGGESTIONS.map((s) => (
                      <button
                        key={s}
                        onClick={() => handleSend(s)}
                        className="px-4 py-2 rounded-full border border-primary-200 text-primary-600 text-sm hover:bg-primary-50 transition-colors"
                      >
                        {s}
                      </button>
                    ))}
                  </div>
                </div>
              )}

              {messages.map((m, i) => (
                <div
                  key={i}
                  className={`flex ${m.role === "user" ? "justify-start" : "justify-end"}`}
                >
                  <div
                    className={`max-w-[85%] px-4 py-3 rounded-2xl ${
                      m.role === "user"
                        ? "bg-primary-100 text-foreground rounded-br-sm"
                        : "bg-accent-500 text-white rounded-bl-sm"
                    }`}
                  >
                    <p className="whitespace-pre-wrap">{m.content}</p>
                    {m.cached && (
                      <span className="text-xs opacity-70 block mt-1">
                        ⚡ پاسخ از حافظه
                      </span>
                    )}
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

          {/* Input */}
          <div className="flex gap-2">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSend()}
              placeholder="سوال خود را بنویسید..."
              disabled={loading}
              className="flex-1 px-4 py-3 rounded-[10px] border border-border bg-surface text-foreground focus:outline-none focus:ring-2 focus:ring-primary-500 disabled:opacity-50"
            />
            <Button onClick={() => handleSend()} loading={loading} disabled={!input.trim()}>
              ارسال
            </Button>
          </div>
        </div>
      </main>
      <Footer />
    </>
  );
}
