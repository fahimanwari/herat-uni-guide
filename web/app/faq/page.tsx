"use client";

import { useState, useEffect } from "react";
import { Header } from "../components/layout/Header";
import { Footer } from "../components/layout/Footer";
import { Card, SectionTitle, Badge } from "../components/ui";
import { API_BASE } from "../lib/config";

interface FAQ {
  id: string;
  question_fa: string;
  answer_fa: string;
  category: string | null;
  sort_order: number;
}

export default function FaqPage() {
  const [faqs, setFaqs] = useState<FAQ[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [openId, setOpenId] = useState<string | null>(null);
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);

  useEffect(() => {
    fetch(`${API_BASE}/faqs`)
      .then((r) => r.json())
      .then((data) => {
        setFaqs(Array.isArray(data) ? data : []);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  // Get unique categories
  const categories = [...new Set(faqs.map((f) => f.category).filter(Boolean))] as string[];

  // Filter
  const filtered = faqs.filter((f) => {
    const matchSearch = !search || f.question_fa.includes(search) || f.answer_fa.includes(search);
    const matchCategory = !selectedCategory || f.category === selectedCategory;
    return matchSearch && matchCategory;
  });

  return (
    <>
      <Header />
      <main className="flex-1 py-12">
        <div className="max-w-3xl mx-auto px-4">
          <SectionTitle title="سوالات متداول" subtitle="پاسخ سوالات رایج درباره پوهنتون هرات" />

          {/* Search */}
          <div className="mb-6">
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="جستجو در سوالات..."
              className="w-full px-4 py-3 rounded-[10px] border border-border bg-surface text-foreground focus:ring-2 focus:ring-primary-500"
            />
          </div>

          {/* Category filters */}
          {categories.length > 0 && (
            <div className="flex flex-wrap gap-2 mb-6">
              <button
                onClick={() => setSelectedCategory(null)}
                className={`px-3 py-1 rounded-full text-sm transition-colors ${!selectedCategory ? "bg-primary-600 text-white" : "bg-surface border border-border text-muted hover:border-primary-400"}`}
              >
                همه
              </button>
              {categories.map((cat) => (
                <button
                  key={cat}
                  onClick={() => setSelectedCategory(selectedCategory === cat ? null : cat)}
                  className={`px-3 py-1 rounded-full text-sm transition-colors ${selectedCategory === cat ? "bg-primary-600 text-white" : "bg-surface border border-border text-muted hover:border-primary-400"}`}
                >
                  {cat}
                </button>
              ))}
            </div>
          )}

          {/* FAQ list */}
          {loading ? (
            <p className="text-muted text-center py-8">در حال بارگذاری...</p>
          ) : filtered.length === 0 ? (
            <Card className="text-center py-8">
              <p className="text-muted">سوالی یافت نشد</p>
            </Card>
          ) : (
            <div className="space-y-3">
              {filtered.map((faq) => (
                <div key={faq.id} className="border border-border rounded-[10px] overflow-hidden">
                  <button
                    onClick={() => setOpenId(openId === faq.id ? null : faq.id)}
                    className="w-full text-right px-5 py-4 flex items-center justify-between hover:bg-surface transition-colors"
                  >
                    <div className="flex items-center gap-3">
                      {faq.category && <Badge variant="neutral">{faq.category}</Badge>}
                      <span className="font-medium text-foreground">{faq.question_fa}</span>
                    </div>
                    <span className={`text-muted transition-transform ${openId === faq.id ? "rotate-180" : ""}`}>▼</span>
                  </button>
                  {openId === faq.id && (
                    <div className="px-5 pb-4 text-foreground leading-relaxed border-t border-border pt-4">
                      {faq.answer_fa}
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      </main>
      <Footer />
    </>
  );
}
