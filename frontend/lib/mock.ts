import type { AnalyzeResponse, ForecastPoint } from "./types";

export const MOCK_ANALYZE: AnalyzeResponse = {
  jahiz_ready_score: 820,
  tier: "بلاتيني - جاهز فوري",
  verdict: "مؤهل بامتياز - خطر منخفض",
  suggested_amount: 164000,
  top_factors: [
    { feature: "invoice_value_trend", value: 0.12, impact: 0.245 },
    { feature: "customer_hhi", value: 0.42, impact: -0.187 },
    { feature: "monthly_revenue_avg", value: 95000, impact: 0.152 },
    { feature: "fixed_cost_ratio", value: 0.55, impact: -0.098 },
    { feature: "dso_days", value: 35, impact: -0.076 },
  ],
  liquidity_forecast: {
    first_gap_date: "2025-11-15",
    max_gap_amount: 32000,
    forecast_total_inflow: 142830,
    forecast_total_outflow: 108204,
  },
  bank_report: `
============================================================
         JAHIZ - تقرير الجاهزية التمويلية
         JAHIZ-Ready Financial Report
============================================================

المنشأة:          Cairo Café
الرقم الضريبي:    310123456700003
القطاع:           Food & Beverage
المدينة:          Riyadh
الجهة الطالبة:    البنك السعودي للاستثمار

------------------------------------------------------------
1. JAHIZ-Ready Score
------------------------------------------------------------
   السكور: 820 / 1000
   الفئة:  بلاتيني - جاهز فوري
   الحكم:  مؤهل بامتياز - خطر منخفض

------------------------------------------------------------
2. الملخص التنفيذي
------------------------------------------------------------
المنشأة تُظهر استقراراً مالياً قوياً مع إيرادات شهرية متوسطة
تبلغ 95,000 ريال. مؤشرات النمو إيجابية وتذبذب التدفق النقدي
ضمن النطاق الآمن. المنشأة جاهزة للتمويل الفوري.

------------------------------------------------------------
3. المحركات الرئيسية للسكور (SHAP)
------------------------------------------------------------
   [+] invoice_value_trend  =     0.12   (الأثر: +0.245)
   [-] customer_hhi         =     0.42   (الأثر: -0.187)
   [+] monthly_revenue_avg  = 95000.00   (الأثر: +0.152)
   [-] fixed_cost_ratio     =     0.55   (الأثر: -0.098)
   [-] dso_days             =    35.00   (الأثر: -0.076)

------------------------------------------------------------
4. تنبؤ السيولة (45 يوماً)
------------------------------------------------------------
   التدفق المتوقع:    142,830 ريال
   المصاريف المتوقعة: 108,204 ريال
   [!] فجوة سيولة متوقعة بتاريخ 2025-11-15 بمقدار 32,000 ريال

------------------------------------------------------------
5. التوصية
------------------------------------------------------------
[OK] نوصي بالموافقة على التمويل بمبلغ يصل إلى 2.0x الإيراد الشهري.

------------------------------------------------------------
6. الشفافية والمصادر
------------------------------------------------------------
   * المحرك: JAHIZ AI Engine v0.1.0
   * التفسير: SHAP (Shapley Additive Explanations)
   * دقة النموذج: 85%+ على بيانات الاختبار
   * المصادر: ZATCA + Mada/POS + Open Banking (Lean)
------------------------------------------------------------
`,
  features: {
    customer_hhi: 0.42,
    dso_days: 35,
    cashflow_volatility: 0.6,
    invoice_value_trend: 0.12,
    seasonality_strength: 1.25,
    fixed_cost_ratio: 0.55,
    supplier_delay_days: 28,
    monthly_revenue_avg: 95000,
  },
};

export function generateMockForecast(): ForecastPoint[] {
  const points: ForecastPoint[] = [];
  const start = new Date();
  let cumulative = 50000;  // رصيد افتتاحي 50,000 ر.س

  for (let i = 0; i < 45; i++) {
    const date = new Date(start);
    date.setDate(date.getDate() + i);
    const dow = date.getDay();
    const weekendBoost = dow === 5 || dow === 6 ? 1.35 : 1.0;
    const yhat = (2500 + Math.sin(i / 5) * 800 + Math.random() * 400) * weekendBoost;

    // فجوة سيولة في الأسبوع 5-6 (يوم 30-40)
    const isGapWeek = i >= 30 && i <= 40;
    const expense = isGapWeek ? 3400 : 2200;

    cumulative += yhat - expense;
    points.push({
      ds: date.toISOString().split("T")[0],
      yhat: Math.round(yhat),
      yhat_lower: Math.round(yhat * 0.75),
      yhat_upper: Math.round(yhat * 1.25),
      cumulative: Math.round(cumulative),
    });
  }
  return points;
}
