import Link from "next/link";
import { notFound } from "next/navigation";
import { Header } from "../../components/layout/Header";
import { Footer } from "../../components/layout/Footer";
import { Card } from "../../components/ui";
import { api } from "../../lib/api";

export async function generateMetadata({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  try {
    const news = await api.news.list();
    const item = news.find((n: any) => n.id === id);
    return { title: item ? `${item.title_fa} | اخبار` : "خبر | پوهنتون هرات" };
  } catch {
    return { title: "خبر | پوهنتون هرات" };
  }
}

export default async function NewsDetailPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;

  let item: any = null;
  try {
    const news = await api.news.list();
    item = news.find((n: any) => n.id === id);
  } catch {}

  if (!item) notFound();

  return (
    <>
      <Header />
      <main className="flex-1 py-12">
        <div className="max-w-3xl mx-auto px-4">
          {/* Breadcrumb */}
          <nav className="text-sm text-muted mb-6">
            <Link href="/" className="hover:text-primary-600">خانه</Link>
            <span className="mx-2">←</span>
            <Link href="/news" className="hover:text-primary-600">اخبار</Link>
            <span className="mx-2">←</span>
            <span className="text-foreground">{item.title_fa}</span>
          </nav>

          {item.cover_image_url && (
            <div className="mb-6 rounded-xl overflow-hidden bg-surface">
              <img src={item.cover_image_url} alt={item.title_fa} className="w-full h-64 object-cover" />
            </div>
          )}

          <h1 className="text-3xl font-bold text-foreground mb-4">{item.title_fa}</h1>

          {item.published_at && (
            <p className="text-muted text-sm mb-6">
              {new Date(item.published_at).toLocaleDateString("fa-AF", { dateStyle: "long" })}
            </p>
          )}

          <Card>
            <div className="prose prose-lg max-w-none text-foreground leading-relaxed whitespace-pre-wrap">
              {item.body_fa || item.body_en || ""}
            </div>
          </Card>

          <div className="mt-8">
            <Link href="/news" className="text-primary-600 hover:text-primary-700 text-sm">
              ← بازگشت به اخبار
            </Link>
          </div>
        </div>
      </main>
      <Footer />
    </>
  );
}
