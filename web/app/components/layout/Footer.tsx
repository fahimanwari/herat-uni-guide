import Link from "next/link";

export function Footer() {
  return (
    <footer className="bg-primary-900 text-white mt-auto">
      <div className="max-w-7xl mx-auto px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {/* About */}
          <div>
            <div className="flex items-center gap-3 mb-4">
              <div className="w-10 h-10 rounded-full bg-primary-600 flex items-center justify-center text-white font-bold text-lg">
                ه
              </div>
              <div>
                <h3 className="font-bold text-lg">پوهنتون هرات</h3>
                <p className="text-primary-300 text-xs">راهنمای هوشمند</p>
              </div>
            </div>
            <p className="text-primary-200 text-sm leading-relaxed">
              راهنمای جامع انتخاب رشته، ماشین حساب چانس کانکور، و مشاوره هوش مصنوعی برای شاگردان مکتب و محصلان پوهنتون هرات.
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="font-bold text-lg mb-4">لینک‌های سریع</h3>
            <ul className="space-y-2 text-sm">
              <li><Link href="/faculties" className="text-primary-200 hover:text-white transition-colors">پوهنځی‌ها</Link></li>
              <li><Link href="/mock-kankor" className="text-primary-200 hover:text-white transition-colors">کانکور آزمایشی</Link></li>
              <li><Link href="/kankor/chance" className="text-primary-200 hover:text-white transition-colors">ماشین حساب چانس</Link></li>
              <li><Link href="/quiz" className="text-primary-200 hover:text-white transition-colors">آزمون انتخاب رشته</Link></li>
              <li><Link href="/chat" className="text-primary-200 hover:text-white transition-colors">مشاور هوش مصنوعی</Link></li>
            </ul>
          </div>

          {/* Resources */}
          <div>
            <h3 className="font-bold text-lg mb-4">منابع</h3>
            <ul className="space-y-2 text-sm">
              <li><Link href="/news" className="text-primary-200 hover:text-white transition-colors">اخبار پوهنتون</Link></li>
              <li><Link href="/faq" className="text-primary-200 hover:text-white transition-colors">پرسش‌های متداول</Link></li>
              <li><Link href="/kankor" className="text-primary-200 hover:text-white transition-colors">راهنمای کانکور</Link></li>
              <li><Link href="/resume" className="text-primary-200 hover:text-white transition-colors">ساخت رزومه</Link></li>
              <li><Link href="/interview" className="text-primary-200 hover:text-white transition-colors">تمرین مصاحبه</Link></li>
            </ul>
          </div>

          {/* Contact */}
          <div>
            <h3 className="font-bold text-lg mb-4">تماس</h3>
            <ul className="space-y-3 text-sm text-primary-200">
              <li className="flex items-center gap-2">
                <svg className="w-4 h-4 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  <path strokeLinecap="round" strokeLinejoin="round" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                <span>شهر هرات، افغانستان</span>
              </li>
              <li className="flex items-center gap-2">
                <svg className="w-4 h-4 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
                <a href="mailto:info@hu.edu.af" className="hover:text-white transition-colors">info@hu.edu.af</a>
              </li>
              <li className="flex items-center gap-2">
                <svg className="w-4 h-4 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" />
                </svg>
                <a href="https://hu.edu.af" target="_blank" rel="noopener noreferrer" className="hover:text-white transition-colors">hu.edu.af</a>
              </li>
            </ul>

            {/* Social */}
            <div className="flex gap-3 mt-4">
              <a href="#" className="w-9 h-9 rounded-full bg-primary-800 flex items-center justify-center text-primary-200 hover:bg-primary-700 hover:text-white transition-colors" aria-label="فیسبوک">
                <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
              </a>
              <a href="#" className="w-9 h-9 rounded-full bg-primary-800 flex items-center justify-center text-primary-200 hover:bg-primary-700 hover:text-white transition-colors" aria-label="تویتر">
                <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z"/></svg>
              </a>
              <a href="#" className="w-9 h-9 rounded-full bg-primary-800 flex items-center justify-center text-primary-200 hover:bg-primary-700 hover:text-white transition-colors" aria-label="یوتیوب">
                <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
              </a>
              <a href="#" className="w-9 h-9 rounded-full bg-primary-800 flex items-center justify-center text-primary-200 hover:bg-primary-700 hover:text-white transition-colors" aria-label="تلگرام">
                <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M11.944 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0a12 12 0 0 0-.056 0zm4.962 7.224c.1-.002.321.023.465.14a.506.506 0 0 1 .171.325c.016.093.036.306.02.472-.18 1.898-.962 6.502-1.36 8.627-.168.9-.499 1.201-.82 1.23-.696.065-1.225-.46-1.9-.902-1.056-.693-1.653-1.124-2.678-1.8-1.185-.78-.417-1.21.258-1.91.177-.184 3.247-2.977 3.307-3.23.007-.032.014-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 1.14-5.061 3.345-.479.33-.913.49-1.302.48-.428-.008-1.252-.241-1.865-.44-.752-.245-1.349-.374-1.297-.789.027-.216.325-.437.893-.663 3.498-1.524 5.83-2.529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.635z"/></svg>
              </a>
            </div>
          </div>
        </div>

        {/* Bottom */}
        <div className="mt-8 pt-8 border-t border-primary-700">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4 text-sm text-primary-300">
            <p>© {new Date().getFullYear()} پلتفرم راهنمای هوشمند پوهنتون هرات. تمامی حقوق محفوظ است.</p>
            <div className="flex gap-4">
              <Link href="/faq" className="hover:text-white transition-colors">حریم خصوصی</Link>
              <Link href="/faq" className="hover:text-white transition-colors">شرایط استفاده</Link>
              <a href="https://hu.edu.af" target="_blank" rel="noopener noreferrer" className="hover:text-white transition-colors">وبسایت رسمی</a>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
}
