"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { Header } from "../components/layout/Header";
import { Footer } from "../components/layout/Footer";
import { Card, SectionTitle, Badge } from "../components/ui";
import { API_BASE } from "../lib/config";

interface Faculty {
  id: string;
  slug: string;
  name_fa: string;
  name_en: string | null;
}

// Approximate positions on campus SVG (percentages)
const FACULTY_POSITIONS: Record<string, { x: number; y: number }> = {
  "medicine": { x: 20, y: 30 },
  "dentistry": { x: 35, y: 25 },
  "engineering": { x: 50, y: 20 },
  "computer-science": { x: 65, y: 30 },
  "economics": { x: 80, y: 35 },
  "law": { x: 15, y: 55 },
  "education": { x: 30, y: 60 },
  "science": { x: 50, y: 55 },
  "agriculture": { x: 70, y: 60 },
  "veterinary": { x: 85, y: 50 },
  "literature": { x: 25, y: 75 },
  "journalism": { x: 45, y: 75 },
  "sharia": { x: 60, y: 80 },
  "arts": { x: 75, y: 75 },
  "social-sciences": { x: 40, y: 40 },
  "public-admin": { x: 55, y: 45 },
};

export default function CampusPage() {
  const [faculties, setFaculties] = useState<Faculty[]>([]);
  const [selected, setSelected] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${API_BASE}/faculties`)
      .then((r) => r.json())
      .then((data) => {
        setFaculties(Array.isArray(data) ? data : []);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  return (
    <>
      <Header />
      <main className="flex-1 py-12">
        <div className="max-w-7xl mx-auto px-4">
          <SectionTitle title="نقشه کمپس" subtitle="پوهنځی‌ها را روی نقشه پیدا کنید" />

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Map */}
            <div className="lg:col-span-2">
              <Card className="relative overflow-hidden">
                <svg viewBox="0 0 100 100" className="w-full h-auto" style={{ minHeight: 400 }}>
                  {/* Background */}
                  <rect x="0" y="0" width="100" height="100" fill="#E8F4E8" rx="2" />

                  {/* Paths */}
                  <path d="M10,50 Q50,45 90,50" stroke="#A0A0A0" strokeWidth="0.5" fill="none" />
                  <path d="M50,10 Q45,50 50,90" stroke="#A0A0A0" strokeWidth="0.5" fill="none" />

                  {/* Buildings */}
                  {faculties.map((f) => {
                    const pos = FACULTY_POSITIONS[f.slug] || { x: 50, y: 50 };
                    const isSelected = selected === f.id;
                    return (
                      <g key={f.id} onClick={() => setSelected(isSelected ? null : f.id)} className="cursor-pointer">
                        <circle cx={pos.x} cy={pos.y} r={isSelected ? 3 : 2} fill={isSelected ? "#E0A22E" : "#1E5AA8"} stroke="white" strokeWidth="0.3" />
                        <text x={pos.x} y={pos.y + 4} textAnchor="middle" fill="#1E293B" fontSize="2" fontWeight="bold">
                          {f.name_fa.length > 8 ? f.name_fa.slice(0, 8) + "..." : f.name_fa}
                        </text>
                      </g>
                    );
                  })}

                  {/* Legend */}
                  <circle cx="5" cy="95" r="1" fill="#1E5AA8" />
                  <text x="7" y="95.5" fill="#1E293B" fontSize="2">پوهنځی</text>
                  <circle cx="25" cy="95" r="1" fill="#E0A22E" />
                  <text x="27" y="95.5" fill="#1E293B" fontSize="2">انتخاب شده</text>
                </svg>
              </Card>
            </div>

            {/* Sidebar */}
            <div>
              <Card>
                <h3 className="font-bold text-foreground mb-3">فهرست پوهنځی‌ها</h3>
                {loading ? (
                  <p className="text-muted text-sm">در حال بارگذاری...</p>
                ) : (
                  <div className="space-y-2 max-h-[400px] overflow-y-auto">
                    {faculties.map((f) => (
                      <Link key={f.id} href={`/faculties/${f.slug}`}>
                        <div className={`p-2 rounded-lg cursor-pointer transition-colors ${selected === f.id ? "bg-primary-100" : "hover:bg-surface"}`}>
                          <p className="font-medium text-foreground text-sm">{f.name_fa}</p>
                          {f.name_en && <p className="text-muted text-xs">{f.name_en}</p>}
                        </div>
                      </Link>
                    ))}
                  </div>
                )}
              </Card>

              {selected && (
                <Card className="mt-4">
                  <p className="text-muted text-sm">روی نقطه کلیک کنید تا صفحه پوهنځی باز شود</p>
                </Card>
              )}
            </div>
          </div>
        </div>
      </main>
      <Footer />
    </>
  );
}
