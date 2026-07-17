import Link from "next/link";
import { Header } from "../components/layout/Header";
import { Footer } from "../components/layout/Footer";
import { Card, SectionTitle } from "../components/ui";

export const metadata = {
  title: "راهنمای کانکور | پوهنتون هرات",
};

export default function KankorPage() {
  return (
    <>
      <Header />
      <main className="flex-1 py-12">
        <div className="max-w-7xl mx-auto px-4">
          <SectionTitle title="راهنمای کانکور" subtitle="اطلاعات کامل درباره امتحان کانکور" />

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Link href="/kankor/chance">
              <Card clickable className="h-full">
                <div className="text-3xl mb-3">📊</div>
                <h3 className="font-bold text-lg mb-2">ماشین حساب چانس</h3>
                <p className="text-muted text-sm">
                  نمره تخمینی خود را وارد کنید و چانس قبولی در هر رشته را ببینید
                </p>
              </Card>
            </Link>
            <Link href="/quiz">
              <Card clickable className="h-full">
                <div className="text-3xl mb-3">🎯</div>
                <h3 className="font-bold text-lg mb-2">آزمون انتخاب رشته</h3>
                <p className="text-muted text-sm">
                  با پاسخ به سوالات، رشته مناسب خود را پیدا کنید
                </p>
              </Card>
            </Link>
          </div>
        </div>
      </main>
      <Footer />
    </>
  );
}
