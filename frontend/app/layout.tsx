import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "جاهز | JAHIZ — محرك الجاهزية التمويلية الفوري",
  description:
    "منصة ذكاء اصطناعي تربط ZATCA + مدى + Open Banking لتمنح المنشآت سكور جاهزية تمويلية وتنبؤ بفجوات السيولة",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ar" dir="rtl">
      <body className="font-arabic antialiased">{children}</body>
    </html>
  );
}
