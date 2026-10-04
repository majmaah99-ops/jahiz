"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Navbar from "@/components/Navbar";
import ConnectCard from "@/components/ConnectCard";
import { ArrowLeft, Sparkles, Shield, Zap } from "lucide-react";

type Status = "idle" | "connecting" | "connected";

export default function HomePage() {
  const router = useRouter();
  const [zatca, setZatca] = useState<Status>("idle");
  const [mada, setMada] = useState<Status>("idle");
  const [bank, setBank] = useState<Status>("idle");

  const allConnected = zatca === "connected" && mada === "connected" && bank === "connected";

  const connect = (
    setter: React.Dispatch<React.SetStateAction<Status>>
  ) => {
    setter("connecting");
    setTimeout(() => setter("connected"), 1200);
  };

  return (
    <main className="min-h-screen">
      <Navbar />

      <div className="mx-auto max-w-6xl px-6 py-16">
        {/* Hero */}
        <div className="text-center mb-16 animate-fade-in">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-brand-500/10 border border-brand-500/30 text-brand-500 text-sm mb-6">
            <Sparkles className="w-4 h-4" />
            هاكاثون منشآت × البنك السعودي للاستثمار
          </div>

          <h1 className="text-5xl md:text-6xl font-bold text-white leading-tight">
            جاهز <span className="text-brand-500">|</span> JAHIZ
          </h1>
          <p className="text-xl text-slate-300 mt-6 max-w-2xl mx-auto leading-relaxed">
            محرك الجاهزية التمويلية الفوري — نربط 3 مصادر بيانات في 60 ثانية
            لنمنحك سكور جاهزية + تنبؤ بفجوات السيولة
          </p>

          {/* Stats */}
          <div className="grid grid-cols-3 gap-4 max-w-3xl mx-auto mt-10">
            {[
              { value: "60s", label: "وقت الربط" },
              { value: "1000", label: "سكور الجاهزية" },
              { value: "45 يوم", label: "إنذار مبكر" },
            ].map((stat) => (
              <div key={stat.label} className="glass rounded-xl p-4 border border-dark-700">
                <div className="text-2xl font-bold text-brand-500">{stat.value}</div>
                <div className="text-xs text-slate-400 mt-1">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>

        {/* Connect Cards */}
        <div className="mb-10">
          <h2 className="text-2xl font-bold text-white mb-2">اربط مصادر البيانات</h2>
          <p className="text-slate-400 mb-6">
            بأمان تام عبر OAuth 2.0 — لا نخزن بياناتك بعد التحليل
          </p>

          <div className="grid md:grid-cols-3 gap-4">
            <ConnectCard
              title="الفاتورة الإلكترونية"
              subtitle="ZATCA e-Invoicing"
              icon="zatca"
              status={zatca}
              onClick={() => connect(setZatca)}
            />
            <ConnectCard
              title="مدى / نقاط البيع"
              subtitle="Mada POS Transactions"
              icon="mada"
              status={mada}
              onClick={() => connect(setMada)}
            />
            <ConnectCard
              title="الحساب البنكي"
              subtitle="Open Banking via Lean"
              icon="bank"
              status={bank}
              onClick={() => connect(setBank)}
            />
          </div>
        </div>

        {/* CTA */}
        <button
          onClick={() => router.push("/dashboard")}
          disabled={!allConnected}
          className="w-full py-5 rounded-2xl bg-gradient-to-l from-brand-500 to-teal-500 text-white font-bold text-lg flex items-center justify-center gap-3 transition disabled:opacity-40 disabled:cursor-not-allowed hover:shadow-lg hover:shadow-brand-500/30"
        >
          {allConnected ? (
            <>
              <Zap className="w-5 h-5" />
              ابدأ التحليل الفوري
              <ArrowLeft className="w-5 h-5" />
            </>
          ) : (
            <>
              <Shield className="w-5 h-5" />
              اربط المصادر الثلاثة للمتابعة
            </>
          )}
        </button>

        {/* Trust footer */}
        <div className="mt-8 text-center text-xs text-slate-500">
          🔒 تشفير E2E • Zero-Retention • متوافق مع معايير ساما و ZATCA
        </div>
      </div>
    </main>
  );
}
