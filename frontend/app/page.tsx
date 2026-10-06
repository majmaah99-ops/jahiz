"use client";

import { useRouter } from "next/navigation";
import Navbar from "@/components/Navbar";
import { MOCK_ANALYZE } from "@/lib/mock";
import { FEATURE_LABELS } from "@/lib/types";
import {
  ArrowLeft,
  Sparkles,
  Shield,
  Zap,
  AlertTriangle,
  TrendingUp,
  Award,
  FileText,
  Bell,
  Building2,
  BarChart3,
  CheckCircle2,
  Coffee,
  XCircle,
  Store,
} from "lucide-react";
import clsx from "clsx";

export default function HomePage() {
  const router = useRouter();
  const data = MOCK_ANALYZE;

  return (
    <main className="min-h-screen">
      <Navbar />

      {/* ============================================================
          SECTION 1: HERO
      ============================================================ */}
      <section className="mx-auto max-w-6xl px-6 pt-16 pb-12">
        <div className="text-center mb-10 animate-fade-in">
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

          {/* Primary CTA */}
          <button
            onClick={() => router.push("/dashboard")}
            className="mt-10 inline-flex items-center gap-3 px-10 py-5 rounded-2xl bg-gradient-to-l from-brand-500 to-teal-500 text-white font-bold text-lg hover:shadow-lg hover:shadow-brand-500/30 transition group"
          >
            <Zap className="w-5 h-5" />
            جرّب الآن مع بيانات تجريبية
            <ArrowLeft className="w-5 h-5 group-hover:-translate-x-1 transition" />
          </button>

          <div className="mt-6 text-sm text-slate-500">
            🔒 OAuth 2.0 • تشفير E2E • Zero-Retention • متوافق مع ساما و ZATCA
          </div>
        </div>
      </section>

      {/* ============================================================
          SECTION 2: قصة منيرة
      ============================================================ */}
      <section className="mx-auto max-w-6xl px-6 py-16 border-t border-dark-700">
        <div className="text-center mb-12">
          <div className="inline-flex items-center gap-2 text-brand-500 text-sm mb-3">
            <Coffee className="w-4 h-4" />
            قصة حقيقية
          </div>
          <h2 className="text-3xl md:text-4xl font-bold text-white">
            قصة منيرة، وليست حالة فردية
          </h2>
          <p className="text-slate-400 mt-3 max-w-2xl mx-auto">
            1.1 مليون منشأة في السعودية تواجه نفس التحدي: بياناتها موجودة،
            لكن البنك لا يراها.
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-6">
          {[
            {
              num: "01",
              icon: Store,
              color: "brand",
              title: "منيرة، 3 فروع كافيه",
              desc: "في الرياض • مبيعاتها 90 ألف ريال شهرياً",
            },
            {
              num: "02",
              icon: XCircle,
              color: "red",
              title: "طلبت تمويل 100 ألف ريال",
              desc: "رُفض لعدم وجود ميزانية مدققة — رغم أن مبيعاتها حقيقية",
            },
            {
              num: "03",
              icon: AlertTriangle,
              color: "red",
              title: "أغلقت فرعاً بعد شهرين",
              desc: "بسبب فجوة سيولة لم تكن تتوقعها",
            },
          ].map((item) => {
            const Icon = item.icon;
            const isRed = item.color === "red";
            return (
              <div
                key={item.num}
                className={clsx(
                  "glass rounded-2xl p-6 border transition hover:scale-[1.02]",
                  isRed
                    ? "border-red-500/30 hover:border-red-500/50"
                    : "border-brand-500/30 hover:border-brand-500/50"
                )}
              >
                <div className="flex items-start justify-between mb-4">
                  <div className="text-5xl font-bold text-white/20">
                    {item.num}
                  </div>
                  <div
                    className={clsx(
                      "w-10 h-10 rounded-xl flex items-center justify-center",
                      isRed ? "bg-red-500/10" : "bg-brand-500/10"
                    )}
                  >
                    <Icon
                      className={clsx(
                        "w-5 h-5",
                        isRed ? "text-red-400" : "text-brand-500"
                      )}
                    />
                  </div>
                </div>
                <div className="font-bold text-white text-lg mb-2">
                  {item.title}
                </div>
                <div className="text-sm text-slate-400 leading-relaxed">
                  {item.desc}
                </div>
              </div>
            );
          })}
        </div>

        <div className="mt-10 text-center">
          <p className="text-brand-500 font-semibold text-lg">
            المشكلة ليست في البيع — بل في غياب اللغة المشتركة مع البنك
          </p>
        </div>
      </section>

      {/* ============================================================
          SECTION 3: الديمو الحي
      ============================================================ */}
      <section className="mx-auto max-w-6xl px-6 py-16 border-t border-dark-700">
        <div className="text-center mb-12">
          <div className="inline-flex items-center gap-2 text-brand-500 text-sm mb-3">
            <BarChart3 className="w-4 h-4" />
            العرض الحي
          </div>
          <h2 className="text-3xl md:text-4xl font-bold text-white">
            هكذا تبدو منيرة بعد 60 ثانية
          </h2>
          <p className="text-slate-400 mt-3 max-w-2xl mx-auto">
            هذه نتائج فعلية من محرك JAHIZ على بيانات محاكاة — جاهزة للعرض الفوري
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-6">
          {/* Score Card */}
          <div className="glass rounded-2xl p-6 border border-brand-500/30 md:col-span-1">
            <div className="flex items-center gap-2 text-brand-500 text-sm mb-4">
              <Award className="w-4 h-4" />
              سكور الجاهزية
            </div>
            <div className="text-center">
              <div className="text-6xl font-bold text-white">
                {data.jahiz_ready_score}
              </div>
              <div className="text-sm text-slate-400 mt-1">/ 1000</div>
              <div className="mt-4 inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-brand-500/10 border border-brand-500/30 text-brand-500 text-xs">
                <Award className="w-3 h-3" />
                {data.tier}
              </div>
            </div>
            <div className="mt-6 pt-6 border-t border-dark-700">
              <div className="text-xs text-slate-400 mb-2">الحكم</div>
              <div className="text-white font-semibold">{data.verdict}</div>
            </div>
          </div>

          {/* Liquidity Gap Alert */}
          <div className="glass rounded-2xl p-6 border border-red-500/30 md:col-span-1">
            <div className="flex items-center gap-2 text-red-400 text-sm mb-4">
              <AlertTriangle className="w-4 h-4" />
              إنذار مبكر
            </div>
            <div className="text-white font-bold text-lg mb-4">
              فجوة سيولة متوقعة
            </div>
            <div className="text-sm text-slate-300 leading-relaxed mb-4">
              بناءً على نمط فواتيرك الحالي، من المتوقع عجز بمقدار{" "}
              <span className="font-bold text-red-400">
                {data.liquidity_forecast.max_gap_amount.toLocaleString("ar-SA")} ريال
              </span>{" "}
              بتاريخ{" "}
              <span className="font-bold text-white">
                {data.liquidity_forecast.first_gap_date}
              </span>
            </div>
            <div className="space-y-2 text-xs">
              <div className="flex justify-between">
                <span className="text-slate-400">التدفق المتوقع</span>
                <span className="text-brand-500 font-semibold">
                  {data.liquidity_forecast.forecast_total_inflow.toLocaleString("ar-SA")} ر.س
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">المصاريف المتوقعة</span>
                <span className="text-red-400 font-semibold">
                  {data.liquidity_forecast.forecast_total_outflow.toLocaleString("ar-SA")} ر.س
                </span>
              </div>
            </div>
          </div>

          {/* Suggested Amount */}
          <div className="glass rounded-2xl p-6 border border-brand-500/30 md:col-span-1">
            <div className="flex items-center gap-2 text-brand-500 text-sm mb-4">
              <TrendingUp className="w-4 h-4" />
              مبلغ التمويل المقترح
            </div>
            <div className="text-center mt-6">
              <div className="text-4xl font-bold text-brand-500 mb-1">
                {data.suggested_amount.toLocaleString("ar-SA")}
              </div>
              <div className="text-sm text-slate-400">ريال سعودي</div>
            </div>
            <div className="mt-6 pt-6 border-t border-dark-700 text-xs text-slate-400 leading-relaxed">
              محسوب بناءً على موسمية المبيعات، الدورة النقدية،
              ومؤشرات النمو المستقبلية.
            </div>
          </div>
        </div>

        <div className="mt-10 text-center">
          <button
            onClick={() => router.push("/dashboard")}
            className="inline-flex items-center gap-3 px-8 py-4 rounded-xl bg-brand-500 text-white font-bold hover:bg-brand-600 transition group"
          >
            <BarChart3 className="w-5 h-5" />
            افتح لوحة التحكم الكاملة
            <ArrowLeft className="w-5 h-5 group-hover:-translate-x-1 transition" />
          </button>
        </div>
      </section>

      {/* ============================================================
          SECTION 4: تقرير البنك
      ============================================================ */}
      <section className="mx-auto max-w-6xl px-6 py-16 border-t border-dark-700">
        <div className="text-center mb-12">
          <div className="inline-flex items-center gap-2 text-brand-500 text-sm mb-3">
            <FileText className="w-4 h-4" />
            الشفافية الكاملة
          </div>
          <h2 className="text-3xl md:text-4xl font-bold text-white">
            لماذا السكور 820؟
          </h2>
          <p className="text-slate-400 mt-3 max-w-2xl mx-auto">
            لا يوجد صندوق أسود. البنك يرى كل عامل ووزنه — بتفسير SHAP
          </p>
        </div>

        <div className="glass rounded-2xl p-8 border border-dark-700">
          <div className="grid md:grid-cols-2 gap-8">
            {/* Factors */}
            <div>
              <h3 className="text-lg font-semibold text-white mb-6">
                المحركات الرئيسية للسكور
              </h3>
              <div className="space-y-4">
                {data.top_factors.slice(0, 5).map((factor) => {
                  const positive = factor.impact > 0;
                  const label = FEATURE_LABELS[factor.feature] || factor.feature;
                  const maxImpact = Math.max(
                    ...data.top_factors.map((f) => Math.abs(f.impact))
                  );
                  const width = (Math.abs(factor.impact) / maxImpact) * 100;
                  return (
                    <div key={factor.feature}>
                      <div className="flex items-center justify-between text-sm mb-2">
                        <span className="text-slate-200">{label}</span>
                        <span
                          className={clsx(
                            "font-mono text-xs px-2 py-0.5 rounded",
                            positive
                              ? "text-brand-500 bg-brand-500/10"
                              : "text-red-400 bg-red-500/10"
                          )}
                        >
                          {factor.impact > 0 ? "+" : ""}
                          {factor.impact.toFixed(3)}
                        </span>
                      </div>
                      <div className="h-2 rounded-full bg-dark-700 overflow-hidden">
                        <div
                          className={clsx(
                            "h-full rounded-full transition-all duration-1000",
                            positive
                              ? "bg-gradient-to-l from-brand-500 to-teal-400"
                              : "bg-gradient-to-l from-red-500 to-orange-400"
                          )}
                          style={{ width: `${width}%` }}
                        />
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Explanation */}
            <div className="flex flex-col justify-center">
              <div className="p-6 rounded-xl bg-dark-800 border border-dark-700">
                <div className="flex items-center gap-3 mb-4">
                  <div className="w-10 h-10 rounded-xl bg-brand-500/10 flex items-center justify-center">
                    <Shield className="w-5 h-5 text-brand-500" />
                  </div>
                  <div>
                    <div className="text-white font-semibold">
                      لماذا هذا السكور؟
                    </div>
                    <div className="text-xs text-slate-400">
                      تفسير SHAP لكل قرار
                    </div>
                  </div>
                </div>
                <ul className="space-y-3 text-sm text-slate-300">
                  <li className="flex items-start gap-2">
                    <CheckCircle2 className="w-4 h-4 text-brand-500 mt-0.5 flex-shrink-0" />
                    <span>نمو مستقر في قيمة الفاتورة (+18%)</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <CheckCircle2 className="w-4 h-4 text-brand-500 mt-0.5 flex-shrink-0" />
                    <span>إيراد شهري متزايد وموسمية صحية</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <AlertTriangle className="w-4 h-4 text-amber-500 mt-0.5 flex-shrink-0" />
                    <span>تركيز عملاء مرتفع نسبياً (42%)</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <CheckCircle2 className="w-4 h-4 text-brand-500 mt-0.5 flex-shrink-0" />
                    <span>المخاطر الإجمالية: منخفضة</span>
                  </li>
                </ul>
              </div>

              <button
                onClick={() => router.push("/report")}
                className="mt-4 inline-flex items-center justify-center gap-2 px-6 py-3 rounded-lg glass border border-dark-700 text-slate-300 hover:text-white hover:border-brand-500/50 transition text-sm"
              >
                <FileText className="w-4 h-4" />
                اعرض تقرير البنك الكامل
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* ============================================================
          SECTION 5: Trust + Final CTA
      ============================================================ */}
      <section className="mx-auto max-w-6xl px-6 py-16 border-t border-dark-700">
        <div className="grid md:grid-cols-3 gap-6 mb-12">
          {[
            {
              icon: Shield,
              title: "أمان وامتثال",
              desc: "OAuth 2.0 + PKCE • تشفير E2E • Zero-Retention",
            },
            {
              icon: Building2,
              title: "للبنك ومنشآت",
              desc: "B2B2B — البنك يدفع 199 ر.س/تقرير • المنشأة مجاناً",
            },
            {
              icon: Bell,
              title: "إنذار مبكر 45 يوماً",
              desc: "تنبؤ بفجوات السيولة قبل حدوثها — Prophet + موسمية سعودية",
            },
          ].map((item) => {
            const Icon = item.icon;
            return (
              <div
                key={item.title}
                className="glass rounded-2xl p-6 border border-dark-700 text-center"
              >
                <div className="w-12 h-12 rounded-xl bg-brand-500/10 flex items-center justify-center mx-auto mb-4">
                  <Icon className="w-6 h-6 text-brand-500" />
                </div>
                <div className="text-white font-semibold mb-2">
                  {item.title}
                </div>
                <div className="text-sm text-slate-400">{item.desc}</div>
              </div>
            );
          })}
        </div>

        <div className="text-center">
          <h3 className="text-2xl font-bold text-white mb-4">
            جاهز — الآن
          </h3>
          <p className="text-brand-500 font-bold text-xl mb-8">
            لا نمنح تمويلاً. نمنح جاهزية.
          </p>
          <button
            onClick={() => router.push("/dashboard")}
            className="inline-flex items-center gap-3 px-10 py-5 rounded-2xl bg-gradient-to-l from-brand-500 to-teal-500 text-white font-bold text-lg hover:shadow-lg hover:shadow-brand-500/30 transition group"
          >
            <Zap className="w-5 h-5" />
            ابدأ التجربة الآن
            <ArrowLeft className="w-5 h-5 group-hover:-translate-x-1 transition" />
          </button>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-dark-700 py-8 text-center text-xs text-slate-500">
        <div className="mx-auto max-w-6xl px-6">
          <div className="flex items-center justify-center gap-4 mb-2">
            <span>جاهز | JAHIZ</span>
            <span>•</span>
            <a
              href="https://github.com/majmaah99-ops/jahiz"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-brand-500 transition"
            >
              GitHub
            </a>
            <span>•</span>
            <span>هاكاثون منشآت × البنك السعودي للاستثمار</span>
          </div>
        </div>
      </footer>
    </main>
  );
}
