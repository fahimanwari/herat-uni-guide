import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "پلتفرم راهنمای هوشمند پوهنتون هرات",
  description: "راهنمای جامع انتخاب رشته، ماشین حساب چانس کانکور، و مشاوره هوش مصنوعی برای پوهنتون هرات",
  metadataBase: new URL("https://guide.hu.edu.af"),
  openGraph: {
    title: "پلتفرم راهنمای هوشمند پوهنتون هرات",
    description: "راهنمای جامع انتخاب رشته، ماشین حساب چانس کانکور، و مشاوره هوش مصنوعی",
    url: "https://guide.hu.edu.af",
    siteName: "پوهنتون هرات",
    locale: "fa_AF",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "پلتفرم راهنمای هوشمند پوهنتون هرات",
    description: "راهنمای جامع انتخاب رشته، ماشین حساب چانس کانکور، و مشاوره هوش مصنوعی",
  },
  alternates: {
    canonical: "https://guide.hu.edu.af",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="fa" dir="rtl" className="h-full antialiased">
      <head>
        <link rel="preload" href="/fonts/Vazirmatn-Regular.woff2" as="font" type="font/woff2" crossOrigin="anonymous" />
        <link rel="preload" href="/fonts/Vazirmatn-Bold.woff2" as="font" type="font/woff2" crossOrigin="anonymous" />
      </head>
      <body className="min-h-full flex flex-col font-vazir">
        {children}
      </body>
    </html>
  );
}
