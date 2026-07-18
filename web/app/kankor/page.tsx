"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { Header } from "../components/layout/Header";
import { Footer } from "../components/layout/Footer";
import { Card, SectionTitle, Badge } from "../components/ui";
import { API_BASE } from "../lib/config";

interface Guide {
  id: string;
  title_fa: string;
  category: string | null;
  sort_order: number;
}

interface Event {
  id: string;
  title_fa: string;
  event_date: string;
  event_type: string;
  description_fa: string | null;
}

export default function KankorPage() {
  const [guides, setGuides] = useState<Guide[]>([]);
  const [events, setEvents] = useState<Event[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      fetch(`${API_BASE}/kankor/guides`).then(r => r.json()).catch(() => []),
      fetch(`${API_BASE}/notifications/events`).then(r => r.json()).catch(() => []),
    ]).then(([g, e]) => {
      setGuides(Array.isArray(g) ? g : []);
      setEvents(Array.isArray(e) ? e : []);
      setLoading(false);
    });
  }, []);

  const getDaysLeft = (dateStr: string) => {
    const target = new Date(dateStr);
    const now = new Date();
    const diff = Math.ceil((target.getTime() - now.getTime()) / (1000 * 60 * 60 * 24));
    return diff;
  };

  return (
    <>
      <Header />
      <main className="flex-1 py-12">
        <div className="max-w-7xl mx-auto px-4">
          <SectionTitle title="راهنمای کانکور" subtitle="اطلاعات کامل درباره امتحان کانکور" />

          {/* Quick links */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
            <Link href="/mock-kankor">
              <Card clickable className="h-full">
                <div className="text-3xl mb-3">📝</div>
                <h3 className="font-bold text-lg mb-2">کانکور آزمایشی</h3>
                <p className="text-muted text-sm">با سوالات واقعی سال‌های گذشته تمرین کنید</p>
                <Badge variant="warning" className="mt-3">⭐ جدید</Badge>
              </Card>
            </Link>
            <Link href="/kankor/chance">
              <Card clickable className="h-full">
                <div className="text-3xl mb-3">📊</div>
                <h3 className="font-bold text-lg mb-2">ماشین حساب چانس</h3>
                <p className="text-muted text-sm">نمره تخمینی خود را وارد کنید و چانس قبولی را ببینید</p>
              </Card>
            </Link>
            <Link href="/quiz">
              <Card clickable className="h-full">
                <div className="text-3xl mb-3">🎯</div>
                <h3 className="font-bold text-lg mb-2">آزمون انتخاب رشته</h3>
                <p className="text-muted text-sm">با پاسخ به سوالات، رشته مناسب خود را پیدا کنید</p>
              </Card>
            </Link>
          </div>

          {/* Events Calendar */}
          {events.length > 0 && (
            <section className="mb-12">
              <SectionTitle title="تقویم رویدادهای کانکور" />
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {events.map((ev) => {
                  const daysLeft = getDaysLeft(ev.event_date);
                  return (
                    <Card key={ev.id}>
                      <div className="flex items-center justify-between">
                        <div>
                          <h3 className="font-bold text-foreground">{ev.title_fa}</h3>
                          {ev.description_fa && <p className="text-muted text-sm mt-1">{ev.description_fa}</p>}
                        </div>
                        <div className="text-center shrink-0 ml-4">
                          {daysLeft > 0 ? (
                            <>
                              <div className="text-2xl font-bold text-primary-600">{daysLeft}</div>
                              <div className="text-xs text-muted">روز دیگر</div>
                            </>
                          ) : (
                            <Badge variant="danger">گذشته</Badge>
                          )}
                        </div>
                      </div>
                    </Card>
                  );
                })}
              </div>
            </section>
          )}

          {/* Guides */}
          {guides.length > 0 && (
            <section>
              <SectionTitle title="مقالات راهنمای کانکور" />
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {guides.map((guide) => (
                  <Card key={guide.id}>
                    <div className="flex items-center gap-3">
                      {guide.category && <Badge variant="neutral">{guide.category}</Badge>}
                      <h3 className="font-bold text-foreground">{guide.title_fa}</h3>
                    </div>
                  </Card>
                ))}
              </div>
            </section>
          )}

          {loading && <p className="text-muted text-center py-8">در حال بارگذاری...</p>}
        </div>
      </main>
      <Footer />
    </>
  );
}
