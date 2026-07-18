"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { Header } from "../components/layout/Header";
import { Footer } from "../components/layout/Footer";
import { Card, SectionTitle } from "../components/ui";
import { FacultyListItem } from "../lib/types";

import { API_BASE } from "../lib/config";
const API = API_BASE;

export default function FacultiesPage() {
  const [faculties, setFaculties] = useState<FacultyListItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${API}/faculties`)
      .then(r => r.json())
      .then(setFaculties)
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  return (
    <>
      <Header />
      <main className="flex-1 py-12">
        <div className="max-w-7xl mx-auto px-4">
          <SectionTitle title="پوهنځی‌ها" subtitle="همه ۱۶ پوهنځی پوهنتون هرات" />

          {loading ? (
            <div className="text-center py-16 text-muted">در حال بارگذاری...</div>
          ) : faculties.length === 0 ? (
            <div className="text-center py-16">
              <span className="text-4xl mb-4 block">📚</span>
              <p className="text-muted text-lg">هنوز پوهنځی ثبت نشده است</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
              {faculties.map((fac) => (
                <Link key={fac.id} href={`/faculties/${fac.slug}`}>
                  <Card clickable className="h-full">
                    <h3 className="font-bold text-lg mb-2 text-foreground">{fac.name_fa}</h3>
                    {fac.name_en && <p className="text-muted text-sm">{fac.name_en}</p>}
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
