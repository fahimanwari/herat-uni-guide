import Link from "next/link";

export function Footer() {
  return (
    <footer className="bg-primary-900 text-white mt-auto">
      <div className="max-w-7xl mx-auto px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* About */}
          <div>
            <h3 className="font-bold text-lg mb-4">پلتفرم راهنمای هوشمند</h3>
            <p className="text-primary-200 text-sm leading-relaxed">
              راهنمای جامع انتخاب رشته، ماشین حساب چانس کانکور، و مشاوره هوش مصنوعی برای شاگردان مکتب و محصلان پوهنتون هرات.
            </p>
          </div>

          {/* Links */}
          <div>
            <h3 className="font-bold text-lg mb-4">لینک‌ها</h3>
            <ul className="space-y-2 text-sm">
              <li><Link href="/faculties" className="text-primary-200 hover:text-white transition-colors">پوهنځی‌ها</Link></li>
              <li><Link href="/kankor" className="text-primary-200 hover:text-white transition-colors">راهنمای کانکور</Link></li>
              <li><Link href="/chat" className="text-primary-200 hover:text-white transition-colors">مشاور هوش مصنوعی</Link></li>
            </ul>
          </div>

          {/* Contact */}
          <div>
            <h3 className="font-bold text-lg mb-4">تماس</h3>
            <ul className="space-y-2 text-sm text-primary-200">
              <li>پوهنتون هرات</li>
              <li>شهر هرات، افغانستان</li>
            </ul>
          </div>
        </div>

        <div className="mt-8 pt-8 border-t border-primary-700 text-center text-sm text-primary-300">
          © {new Date().getFullYear()} پلتفرم راهنمای هوشمند پوهنتون هرات
        </div>
      </div>
    </footer>
  );
}
