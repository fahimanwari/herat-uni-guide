import Link from "next/link";
import { Header } from "./components/layout/Header";
import { Footer } from "./components/layout/Footer";
import { Card, SectionTitle, Badge } from "./components/ui";

export default function HomePage() {
  return (
    <>
      <Header />
      <main className="flex-1">
        {/* Hero */}
        <section className="bg-gradient-to-bl from-primary-700 via-primary-600 to-primary-800 text-white py-16 md:py-24">
          <div className="max-w-7xl mx-auto px-4 text-center">
            <h1 className="text-3xl md:text-5xl font-bold mb-6 leading-tight">
              رشته مناسب خودت را پیدا کن
            </h1>
            <p className="text-primary-100 text-lg md:text-xl mb-8 max-w-2xl mx-auto">
              راهنمای هوشمند پوهنتون هرات — از انتخاب رشته تا مشاوره هوش مصنوعی
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                href="/kankor/chance"
                className="inline-flex items-center justify-center px-8 py-4 bg-gold-500 text-white rounded-[10px] font-bold text-lg hover:bg-gold-600 transition-colors shadow-lg"
              >
                ⭐ چانست را حساب کن
              </Link>
              <Link
                href="/faculties"
                className="inline-flex items-center justify-center px-8 py-4 border-2 border-white/30 text-white rounded-[10px] font-medium text-lg hover:bg-white/10 transition-colors"
              >
                پوهنځی‌ها را ببین
              </Link>
            </div>
          </div>
        </section>

        {/* Stats */}
        <section className="py-12 bg-surface">
          <div className="max-w-7xl mx-auto px-4">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
              {[
                { number: "۱۶", label: "پوهنځی" },
                { number: "۷۰+", label: "رشته" },
                { number: "۲۵,۰۰۰+", label: "محصل" },
                { number: "۴۰۰+", label: "استاد" },
              ].map((stat) => (
                <div key={stat.label} className="text-center">
                  <div className="text-3xl md:text-4xl font-bold text-primary-600">{stat.number}</div>
                  <div className="text-muted mt-1">{stat.label}</div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Quick Actions */}
        <section className="py-16">
          <div className="max-w-7xl mx-auto px-4">
            <SectionTitle title="سریع شروع کنید" />
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <Link href="/kankor/chance">
                <Card clickable>
                  <div className="text-3xl mb-3">📊</div>
                  <h3 className="font-bold text-lg mb-2">ماشین حساب چانس</h3>
                  <p className="text-muted text-sm">
                    نمره تخمینی خود را وارد کنید و چانس قبولی در هر رشته را ببینید
                  </p>
                  <Badge variant="success" className="mt-3">پرکشش‌ترین قابلیت</Badge>
                </Card>
              </Link>
              <Link href="/quiz">
                <Card clickable>
                  <div className="text-3xl mb-3">🎯</div>
                  <h3 className="font-bold text-lg mb-2">آزمون انتخاب رشته</h3>
                  <p className="text-muted text-sm">
                    با پاسخ به ۳۰ سوال، رشته‌های مناسب علاقه‌مندی‌های خود را کشف کنید
                  </p>
                </Card>
              </Link>
              <Link href="/chat">
                <Card clickable>
                  <div className="text-3xl mb-3">🤖</div>
                  <h3 className="font-bold text-lg mb-2">مشاور هوش مصنوعی</h3>
                  <p className="text-muted text-sm">
                    سوالات خود درباره پوهنتون هرات و رشته‌ها را از AI بپرسید
                  </p>
                  <Badge variant="neutral" className="mt-3">سه‌زبانه</Badge>
                </Card>
              </Link>
            </div>
          </div>
        </section>

        {/* Faculties Preview */}
        <section className="py-16 bg-surface">
          <div className="max-w-7xl mx-auto px-4">
            <SectionTitle title="پوهنځی‌ها" subtitle="همه ۱۶ پوهنځی پوهنتون هرات" />
            <div className="text-center">
              <Link
                href="/faculties"
                className="inline-flex items-center gap-2 text-primary-600 font-medium hover:text-primary-700 transition-colors"
              >
                مشاهده همه پوهنځی‌ها
                <span>←</span>
              </Link>
            </div>
          </div>
        </section>
      </main>
      <Footer />
    </>
  );
}
