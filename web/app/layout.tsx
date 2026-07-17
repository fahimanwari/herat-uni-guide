import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "پلتفرم راهنمای هوشمند پوهنتون هرات",
  description: "راهنمای جامع انتخاب رشته، ماشین حساب چانس کانکور، و مشاوره هوش مصنوعی برای پوهنتون هرات",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="fa" dir="rtl" className="h-full antialiased">
      <head>
        <link
          rel="stylesheet"
          href="https://cdn.jsdelivr.net/gh/rastikerdar/vazirmatn@v33.003/Vazirmatn-font-face.css"
        />
      </head>
      <body className="min-h-full flex flex-col font-vazir">
        {children}
      </body>
    </html>
  );
}
