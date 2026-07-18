"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Header } from "../components/layout/Header";
import { Footer } from "../components/layout/Footer";
import { Button, Card } from "../components/ui";
import { API_BASE } from "../lib/config";

export default function RegisterPage() {
  const router = useRouter();
  const [form, setForm] = useState({ email: "", password: "", full_name: "", phone: "" });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleRegister = async () => {
    setLoading(true);
    setError("");
    try {
      const res = await fetch(`${API_BASE}/users/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });
      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.detail || "خطا در ثبت‌نام");
      }
      const data = await res.json();
      localStorage.setItem("user_access", data.access_token);
      localStorage.setItem("user_refresh", data.refresh_token);
      localStorage.setItem("user_id", data.user?.id || "");
      router.push("/mock-kankor/history");
    } catch (e: any) {
      setError(e.message || "خطا در ثبت‌نام");
    }
    setLoading(false);
  };

  return (
    <>
      <Header />
      <main className="flex-1 flex items-center justify-center py-12 bg-surface min-h-screen">
        <div className="w-full max-w-md px-4">
          <Card>
            <h1 className="text-2xl font-bold text-center mb-6 text-foreground">ثبت‌نام</h1>
            <p className="text-muted text-center text-sm mb-6">حساب بسازید تا تاریخچه آزمون‌ها ذخیره شود</p>
            {error && <div className="bg-danger/10 text-danger p-3 rounded-lg mb-4 text-sm">{error}</div>}
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-muted mb-1">نام کامل</label>
                <input type="text" value={form.full_name} onChange={(e) => setForm({ ...form, full_name: e.target.value })} className="w-full px-4 py-3 border border-border rounded-[10px] bg-surface text-foreground focus:ring-2 focus:ring-primary-500" placeholder="نام کامل" />
              </div>
              <div>
                <label className="block text-sm font-medium text-muted mb-1">ایمیل</label>
                <input type="email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} className="w-full px-4 py-3 border border-border rounded-[10px] bg-surface text-foreground focus:ring-2 focus:ring-primary-500" placeholder="email@example.com" />
              </div>
              <div>
                <label className="block text-sm font-medium text-muted mb-1">شماره تلفن (اختیاری)</label>
                <input type="tel" value={form.phone} onChange={(e) => setForm({ ...form, phone: e.target.value })} className="w-full px-4 py-3 border border-border rounded-[10px] bg-surface text-foreground focus:ring-2 focus:ring-primary-500" placeholder="07XXXXXXXX" />
              </div>
              <div>
                <label className="block text-sm font-medium text-muted mb-1">رمز عبور</label>
                <input type="password" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} className="w-full px-4 py-3 border border-border rounded-[10px] bg-surface text-foreground focus:ring-2 focus:ring-primary-500" placeholder="حداقل ۶ کاراکتر" />
              </div>
              <Button onClick={handleRegister} loading={loading} className="w-full">ثبت‌نام</Button>
            </div>
            <p className="text-center mt-4 text-sm text-muted">
              حساب دارید؟ <Link href="/login" className="text-primary-600 hover:text-primary-700">ورود کنید</Link>
            </p>
          </Card>
        </div>
      </main>
      <Footer />
    </>
  );
}
