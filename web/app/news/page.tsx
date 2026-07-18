import Link from "next/link";
import { Header } from "../components/layout/Header";
import { Footer } from "../components/layout/Footer";
import { Card, SectionTitle, Badge } from "../components/ui";
import { api } from "../lib/api";

export const metadata = {
  title: "اخبار | پوهنتون هرات",
};

export default async function NewsPage() {
  let news: any[] = [];
  try {
    news = await api.news.list();
  } catch {
    news = [];
  }

  return (
    <>
      <Header />
      <main className="flex-1 py-12">
        <div className="max-w-7xl mx-auto px-4">
          <SectionTitle title="اخبار پوهنتون هرات" />

          {news.length === 0 ? (
            <Card className="text-center py-12">
              <p className="text-muted text-lg">هنوز خبری منتشر نشده است</p>
            </Card>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {news.map((item: any) => (
                <Link key={item.id} href={`/news/${item.id}`}>
                  <Card clickable className="h-full">
                    {item.cover_image_url && (
                      <div className="mb-3 rounded-lg overflow-hidden bg-surface h-40 flex items-center justify-center">
                        <img src={item.cover_image_url} alt={item.title_fa} className="w-full h-full object-cover" />
                      </div>
                    )}
                    <h3 className="font-bold text-lg text-foreground mb-2 line-clamp-2">{item.title_fa}</h3>
                    {item.published_at && (
                      <p className="text-muted text-sm">
                        {new Date(item.published_at).toLocaleDateString("fa-AF", { dateStyle: "long" })}
                      </p>
                    )}
                  </Card>
                </Link>
              ))}
            </div>
          )}
        </div>
      </main>
      <Footer />
    </>
  );
}
