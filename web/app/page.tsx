"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { Header } from "./components/layout/Header";
import { Footer } from "./components/layout/Footer";
import { Card, SectionTitle, Badge } from "./components/ui";
import { API_BASE } from "./lib/config";

export default function HomePage() {
  const [news, setNews] = useState<any[]>([]);
  const [stats, setStats] = useState<any>({});
  const [events, setEvents] = useState<any[]>([]);
  const [faculties, setFaculties] = useState<any[]>([]);
  const [animate, setAnimate] = useState(false);

  useEffect(() => {
    setAnimate(true);
    Promise.allSettled([
      fetch(`${API_BASE}/news`).then(r => r.json()),
      fetch(`${API_BASE}/faculties`).then(r => r.json()),
      fetch(`${API_BASE}/notifications/events`).then(r => r.json()),
    ]).then(([newsRes, facRes, evRes]) => {
      if (newsRes.status === "fulfilled") setNews((newsRes.value || []).slice(0, 3));
      if (facRes.status === "fulfilled") {
        const f = facRes.value || [];
        setFaculties(f);
        setStats({ faculties: f.length });
      }
      if (evRes.status === "fulfilled") {
        const ev = (evRes.value || []).filter((e: any) => new Date(e.event_date) > new Date()).slice(0, 2);
        setEvents(ev);
      }
    });
  }, []);

  return (
    <>
      <Header />
      <main className="flex-1">
        {/* Hero */}
        <section className="relative bg-gradient-to-bl from-primary-700 via-primary-600 to-primary-800 text-white py-20 md:py-28 overflow-hidden">
          {/* Decorative elements */}
          <div className="absolute inset-0 opacity-10">
            <div className="absolute top-20 right-20 w-64 h-64 rounded-full bg-gold-500 blur-3xl" />
            <div className="absolute bottom-10 left-10 w-48 h-48 rounded-full bg-accent-500 blur-3xl" />
          </div>

          <div className="relative max-w-7xl mx-auto px-4 text-center">
            <div className={`transition-all duration-1000 ${animate ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"}`}>
              <Badge variant="warning" className="mb-6 text-sm px-4 py-1.5">
                ⭐ پلتفرم رسمی راهنمای کانکور
              </Badge>
              <h1 className="text-4xl md:text-6xl font-bold mb-6 leading-tight">
                رشته مناسب <span className="text-gold-400">خودت</span> را پیدا کن
              </h1>
              <p className="text-primary-100 text-lg md:text-xl mb-10 max-w-2xl mx-auto leading-relaxed">
                راهنمای هوشمند پوهنتون هرات — از انتخاب رشته تا مشاوره هوش مصنوعی، همه چیز در یک پلتفرم
              </p>
            </div>

            <div className={`flex flex-col sm:flex-row gap-4 justify-center transition-all duration-1000 delay-300 ${animate ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"}`}>
              <Link href="/mock-kankor" className="inline-flex items-center justify-center px-8 py-4 bg-gold-500 text-white rounded-[10px] font-bold text-lg hover:bg-gold-600 transition-all shadow-lg hover:shadow-xl hover:-translate-y-0.5">
                📝 کانکور آزمایشی
              </Link>
              <Link href="/kankor/chance" className="inline-flex items-center justify-center px-8 py-4 bg-white/10 border-2 border-white/30 text-white rounded-[10px] font-medium text-lg hover:bg-white/20 transition-all">
                📊 چانست را حساب کن
              </Link>
              <Link href="/faculties" className="inline-flex items-center justify-center px-8 py-4 border-2 border-white/30 text-white rounded-[10px] font-medium text-lg hover:bg-white/10 transition-all">
                🎓 پوهنځی‌ها را ببین
              </Link>
            </div>
          </div>
        </section>

        {/* Stats */}
        <section className="py-16 bg-surface">
          <div className="max-w-7xl mx-auto px-4">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
              {[
                { number: `${stats.faculties || "۱۶"}`, label: "پوهنځی", icon: "🏛️" },
                { number: "۷۰+", label: "رشته", icon: "📚" },
                { number: "۲۵,۰۰۰+", label: "محصل", icon: "👨‍🎓" },
                { number: "۴۰۰+", label: "استاد", icon: "👨‍🏫" },
              ].map((stat, i) => (
                <div key={stat.label} className={`text-center transition-all duration-700 ${animate ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"}`} style={{ transitionDelay: `${i * 100 + 400}ms` }}>
                  <div className="text-3xl mb-2">{stat.icon}</div>
                  <div className="text-3xl md:text-4xl font-bold text-primary-600">{stat.number}</div>
                  <div className="text-muted mt-1">{stat.label}</div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Upcoming Events */}
        {events.length > 0 && (
          <section className="py-12">
            <div className="max-w-7xl mx-auto px-4">
              <SectionTitle title="رویدادهای نزدیک" />
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {events.map((ev: any) => {
                  const daysLeft = Math.ceil((new Date(ev.event_date).getTime() - Date.now()) / (1000 * 60 * 60 * 24));
                  return (
                    <Card key={ev.id} className="relative overflow-hidden">
                      <div className="absolute top-0 left-0 w-1 h-full bg-gold-500" />
                      <div className="flex items-center justify-between pl-4">
                        <div>
                          <h3 className="font-bold text-foreground">{ev.title_fa}</h3>
                          {ev.description_fa && <p className="text-muted text-sm mt-1">{ev.description_fa}</p>}
                        </div>
                        <div className="text-center shrink-0 ml-4">
                          <div className="text-3xl font-bold text-gold-500">{daysLeft}</div>
                          <div className="text-xs text-muted">روز دیگر</div>
                        </div>
                      </div>
                    </Card>
                  );
                })}
              </div>
            </div>
          </section>
        )}

        {/* Quick Actions */}
        <section className="py-16 bg-surface">
          <div className="max-w-7xl mx-auto px-4">
            <SectionTitle title="سریع شروع کنید" />
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              {[
                { href: "/mock-kankor", icon: "📝", title: "کانکور آزمایشی", desc: "با سوالات واقعی سال‌های گذشته تمرین کنید", badge: "⭐ جدید", badgeVariant: "warning" as const },
                { href: "/kankor/chance", icon: "📊", title: "ماشین حساب چانس", desc: "نمره تخمینی خود را وارد کنید و چانس قبولی را ببینید" },
                { href: "/quiz", icon: "🎯", title: "آزمون انتخاب رشته", desc: "با پاسخ به ۳۰ سوال، رشته مناسب خود را کشف کنید" },
                { href: "/chat", icon: "🤖", title: "مشاور هوش مصنوعی", desc: "سوالات خود را از AI بپرسید", badge: "سه‌زبانه", badgeVariant: "neutral" as const },
              ].map((item, i) => (
                <Link key={item.href} href={item.href}>
                  <div className="transition-all duration-500 hover:shadow-lg" style={{ transitionDelay: `${i * 100}ms` }}>
                    <Card clickable className="h-full">
                      <div className="text-4xl mb-4">{item.icon}</div>
                      <h3 className="font-bold text-lg mb-2 text-foreground">{item.title}</h3>
                      <p className="text-muted text-sm mb-3">{item.desc}</p>
                      {item.badge && <Badge variant={item.badgeVariant}>{item.badge}</Badge>}
                    </Card>
                  </div>
                </Link>
              ))}
            </div>
          </div>
        </section>

        {/* Latest News */}
        {news.length > 0 && (
          <section className="py-16">
            <div className="max-w-7xl mx-auto px-4">
              <SectionTitle title="آخرین اخبار" />
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {news.map((item: any) => (
                  <Link key={item.id} href={`/news/${item.id}`}>
                    <Card clickable className="h-full group">
                      <h3 className="font-bold text-lg text-foreground mb-2 group-hover:text-primary-600 transition-colors line-clamp-2">{item.title_fa}</h3>
                      {item.published_at && (
                        <p className="text-muted text-sm">
                          {new Date(item.published_at).toLocaleDateString("fa-AF", { dateStyle: "long" })}
                        </p>
                      )}
                    </Card>
                  </Link>
                ))}
              </div>
              <div className="text-center mt-6">
                <Link href="/news" className="inline-flex items-center gap-2 text-primary-600 hover:text-primary-700 font-medium transition-colors">
                  مشاهده همه اخبار
                  <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M15 19l-7-7 7-7" />
                  </svg>
                </Link>
              </div>
            </div>
          </section>
        )}

        {/* Testimonials */}
        <section className="py-16 bg-primary-900 text-white">
          <div className="max-w-7xl mx-auto px-4">
            <SectionTitle title="نظرات شاگردان" subtitle="آنچه شاگردان درباره ما می‌گویند" className="[&_h2]:text-white [&_div]:bg-white/20 [&_p]:text-primary-200" />
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {[
                { name: "احمد احمدی", role: "شاگرد صنف ۱۲", text: "ماشین حساب چانس خیلی کمکم کرد. فهمیدم چه رشته‌هایی شانس قبولی دارم." },
                { name: "فاطمه حسینی", role: "محصل پوهنځی انجنیری", text: "آزمون انتخاب رشته عالی بود. فهمیدم انجنیری بهترین انتخاب برای من است." },
                { name: "محمد رحیمی", role: "شاگرد صنف ۱۱", text: "مشاور AI خیلی مفید است. هر سوالی داشتم فوراً جواب گرفتم." },
              ].map((t, i) => (
                <Card key={i} className="bg-white/10 border-white/20">
                  <div className="flex items-center gap-3 mb-3">
                    <div className="w-10 h-10 rounded-full bg-gold-500 flex items-center justify-center text-white font-bold">
                      {t.name[0]}
                    </div>
                    <div>
                      <p className="font-medium text-white">{t.name}</p>
                      <p className="text-primary-300 text-xs">{t.role}</p>
                    </div>
                  </div>
                  <p className="text-primary-100 text-sm leading-relaxed">{t.text}</p>
                </Card>
              ))}
            </div>
          </div>
        </section>

        {/* Faculties Preview */}
        <section className="py-16 bg-surface">
          <div className="max-w-7xl mx-auto px-4">
            <SectionTitle title="پوهنځی‌ها" subtitle={`همه ${stats.faculties || "۱۶"} پوهنځی پوهنتون هرات`} />
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {faculties.slice(0, 8).map((f: any) => (
                <Link key={f.id} href={`/faculties/${f.slug}`}>
                  <Card clickable className="h-full text-center py-6">
                    <p className="font-medium text-foreground">{f.name_fa}</p>
                  </Card>
                </Link>
              ))}
            </div>
            <div className="text-center mt-6">
              <Link href="/faculties" className="inline-flex items-center gap-2 text-primary-600 hover:text-primary-700 font-medium transition-colors">
                مشاهده همه پوهنځی‌ها
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M15 19l-7-7 7-7" />
                </svg>
              </Link>
            </div>
          </div>
        </section>

        {/* CTA */}
        <section className="py-16 bg-gradient-to-bl from-gold-500 to-gold-600 text-white">
          <div className="max-w-3xl mx-auto px-4 text-center">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">آماده‌اید رشته خود را پیدا کنید؟</h2>
            <p className="text-gold-100 text-lg mb-8">
              همین حالا شروع کنید و آینده شغلی خود را بسازید
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="/mock-kankor" className="inline-flex items-center justify-center px-8 py-4 bg-white text-gold-600 rounded-[10px] font-bold text-lg hover:bg-gold-50 transition-all shadow-lg">
                📝 شروع آزمون
              </Link>
              <Link href="/chat" className="inline-flex items-center justify-center px-8 py-4 border-2 border-white/50 text-white rounded-[10px] font-medium text-lg hover:bg-white/10 transition-all">
                🤖 مشاوره AI
              </Link>
            </div>
          </div>
        </section>
      </main>
      <Footer />
    </>
  );
}
