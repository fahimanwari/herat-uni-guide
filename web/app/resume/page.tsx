"use client";

import { useState } from "react";
import { Header } from "../components/layout/Header";
import { Footer } from "../components/layout/Footer";
import { Button, Card, SectionTitle } from "../components/ui";

interface ResumeData {
  fullName: string;
  email: string;
  phone: string;
  education: { school: string; year: string; field: string }[];
  skills: string[];
  languages: string[];
  interests: string;
  goal: string;
}

const emptyResume: ResumeData = {
  fullName: "", email: "", phone: "",
  education: [{ school: "", year: "", field: "" }],
  skills: [""], languages: ["دری", "انگلیسی"], interests: "", goal: "",
};

export default function ResumePage() {
  const [data, setData] = useState<ResumeData>(emptyResume);
  const [showPreview, setShowPreview] = useState(false);

  const updateField = (field: keyof ResumeData, value: any) => {
    setData({ ...data, [field]: value });
  };

  const addEducation = () => {
    setData({ ...data, education: [...data.education, { school: "", year: "", field: "" }] });
  };

  const updateEducation = (index: number, field: string, value: string) => {
    const newEdu = [...data.education];
    (newEdu[index] as any)[field] = value;
    setData({ ...data, education: newEdu });
  };

  const removeEducation = (index: number) => {
    setData({ ...data, education: data.education.filter((_, i) => i !== index) });
  };

  return (
    <>
      <Header />
      <main className="flex-1 py-12">
        <div className="max-w-3xl mx-auto px-4">
          <SectionTitle title="ساخت رزومه" subtitle="رزومه خود را بسازید و چاپ کنید" />

          {showPreview ? (
            <Card className="mb-6">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-xl font-bold text-foreground">پیش‌نمایش رزومه</h2>
                <div className="flex gap-2">
                  <Button variant="outline" size="sm" onClick={() => setShowPreview(false)}>ویرایش</Button>
                  <Button size="sm" onClick={() => window.print()}>چاپ / ذخیره PDF</Button>
                </div>
              </div>
              <div className="border border-border p-6 rounded-lg">
                <h1 className="text-2xl font-bold text-foreground mb-1">{data.fullName || "نام شما"}</h1>
                <p className="text-muted text-sm mb-4">{data.email} {data.phone && `| ${data.phone}`}</p>
                {data.goal && <p className="text-foreground mb-4">{data.goal}</p>}
                {data.education.length > 0 && data.education[0].school && (
                  <div className="mb-4">
                    <h3 className="font-bold text-foreground mb-2">تحصیلات</h3>
                    {data.education.map((edu, i) => edu.school && (
                      <div key={i} className="mb-2">
                        <p className="font-medium text-foreground">{edu.field} — {edu.school}</p>
                        <p className="text-muted text-sm">{edu.year}</p>
                      </div>
                    ))}
                  </div>
                )}
                {data.skills.filter(Boolean).length > 0 && (
                  <div className="mb-4">
                    <h3 className="font-bold text-foreground mb-2">مهارت‌ها</h3>
                    <div className="flex flex-wrap gap-2">
                      {data.skills.filter(Boolean).map((s, i) => (
                        <span key={i} className="px-3 py-1 bg-primary-100 text-primary-700 rounded-full text-sm">{s}</span>
                      ))}
                    </div>
                  </div>
                )}
                {data.languages.length > 0 && (
                  <div className="mb-4">
                    <h3 className="font-bold text-foreground mb-2">زبان‌ها</h3>
                    <p className="text-foreground">{data.languages.join("، ")}</p>
                  </div>
                )}
                {data.interests && (
                  <div>
                    <h3 className="font-bold text-foreground mb-2">علایق</h3>
                    <p className="text-foreground">{data.interests}</p>
                  </div>
                )}
              </div>
            </Card>
          ) : (
            <Card className="mb-6">
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-muted mb-1">نام کامل</label>
                  <input value={data.fullName} onChange={(e) => updateField("fullName", e.target.value)} className="w-full px-4 py-3 border border-border rounded-[10px] bg-surface text-foreground" placeholder="نام کامل" />
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-muted mb-1">ایمیل</label>
                    <input value={data.email} onChange={(e) => updateField("email", e.target.value)} className="w-full px-4 py-3 border border-border rounded-[10px] bg-surface text-foreground" placeholder="email@example.com" />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-muted mb-1">تلفن</label>
                    <input value={data.phone} onChange={(e) => updateField("phone", e.target.value)} className="w-full px-4 py-3 border border-border rounded-[10px] bg-surface text-foreground" placeholder="07XXXXXXXX" />
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium text-muted mb-1">هدف شغلی</label>
                  <textarea value={data.goal} onChange={(e) => updateField("goal", e.target.value)} className="w-full px-4 py-3 border border-border rounded-[10px] bg-surface text-foreground" rows={2} placeholder="جستجوی موقعیت ..." />
                </div>
                <div>
                  <div className="flex items-center justify-between mb-1">
                    <label className="text-sm font-medium text-muted">تحصیلات</label>
                    <button onClick={addEducation} className="text-primary-600 text-sm hover:text-primary-700">+ افزودن</button>
                  </div>
                  {data.education.map((edu, i) => (
                    <div key={i} className="grid grid-cols-3 gap-2 mb-2">
                      <input value={edu.field} onChange={(e) => updateEducation(i, "field", e.target.value)} className="px-3 py-2 border border-border rounded-lg text-sm bg-surface" placeholder="رشته" />
                      <input value={edu.school} onChange={(e) => updateEducation(i, "school", e.target.value)} className="px-3 py-2 border border-border rounded-lg text-sm bg-surface" placeholder="مکتب/پوهنتون" />
                      <div className="flex gap-1">
                        <input value={edu.year} onChange={(e) => updateEducation(i, "year", e.target.value)} className="flex-1 px-3 py-2 border border-border rounded-lg text-sm bg-surface" placeholder="سال" />
                        {data.education.length > 1 && <button onClick={() => removeEducation(i)} className="text-danger text-sm px-2">✕</button>}
                      </div>
                    </div>
                  ))}
                </div>
                <div>
                  <label className="block text-sm font-medium text-muted mb-1">مهارت‌ها (هر خط یک مهارت)</label>
                  <textarea value={data.skills.join("\n")} onChange={(e) => updateField("skills", e.target.value.split("\n"))} className="w-full px-4 py-3 border border-border rounded-[10px] bg-surface text-foreground" rows={3} placeholder="برنامه‌نویسی&#10;حل مسئله" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-muted mb-1">علایق</label>
                  <textarea value={data.interests} onChange={(e) => updateField("interests", e.target.value)} className="w-full px-4 py-3 border border-border rounded-[10px] bg-surface text-foreground" rows={2} placeholder="کتابخوانی، ورزش، ..." />
                </div>
                <Button onClick={() => setShowPreview(true)} className="w-full">پیش‌نمایش و چاپ</Button>
              </div>
            </Card>
          )}
        </div>
      </main>
      <Footer />
    </>
  );
}
