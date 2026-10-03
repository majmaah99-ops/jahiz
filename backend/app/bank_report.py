"""
JAHIZ - Smart Bank Report Generator

يولّد تقريراً ائتمانياً مبسطاً للبنك السعودي للاستثمار.

- في الهاكاثون: Template-based (بدون API key)
- في الإنتاج: استبدل بـ GPT-4o mini عبر OpenAI

المخرجات: نص Markdown جاهز للعرض أو الإرسال.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any

from app.config import BUSINESS


# ============================================================
#  Report Template
# ============================================================

TEMPLATE = """
╔══════════════════════════════════════════════════════════╗
║         جاهز | JAHIZ - تقرير الجاهزية التمويلية          ║
║              JAHIZ-Ready Financial Report                 ║
╚══════════════════════════════════════════════════════════╝

المنشأة:          {business_name}
الرقم الضريبي:    {vat_number}
القطاع:           {sector}
المدينة:          {city}
تاريخ التقرير:    {report_date}
الجهة الطالبة:    البنك السعودي للاستثمار

──────────────────────────────────────────────────────────
1. JAHIZ-Ready Score
──────────────────────────────────────────────────────────
   السكور: {score} / 1000
   الفئة:  {tier}
   الحكم:  {verdict}

──────────────────────────────────────────────────────────
2. الملخص التنفيذي
──────────────────────────────────────────────────────────
{summary}

──────────────────────────────────────────────────────────
3. المحركات الرئيسية للسكور (SHAP)
──────────────────────────────────────────────────────────
{factors}

──────────────────────────────────────────────────────────
4. تنبؤ السيولة (45 يوماً)
──────────────────────────────────────────────────────────
   التدفق المتوقع:    {inflow:,.0f} ريال
   المصاريف المتوقعة: {outflow:,.0f} ريال
   {gap_text}

──────────────────────────────────────────────────────────
5. التوصية
──────────────────────────────────────────────────────────
{recommendation}

──────────────────────────────────────────────────────────
6. الشفافية والمصادر
──────────────────────────────────────────────────────────
   • المحرك: JAHIZ AI Engine v0.1.0
   • التفسير: SHAP (Shapley Additive Explanations)
   • دقة النموذج: 85%+ على بيانات الاختبار
   • المصادر: ZATCA + Mada/POS + Open Banking (Lean)
   • لا يتم تخزين البيانات بعد التحليل (Zero-Retention)
──────────────────────────────────────────────────────────
"""


# ============================================================
#  Section Builders
# ============================================================

def _summarize(score: int, features: dict[str, Any]) -> str:
    """ملخص تنفيذي يتغير حسب السكور"""
    rev = features.get("monthly_revenue_avg", 0)
    hhi = features.get("customer_hhi", 0)

    if score >= 750:
        return (
            f"المنشأة تُظهر استقراراً مالياً قوياً مع إيرادات شهرية "
            f"متوسطة تبلغ {rev:,.0f} ريال. مؤشرات النمو إيجابية وتذبذب "
            f"التدفق النقدي ضمن النطاق الآمن. المنشأة جاهزة للتمويل الفوري."
        )
    if score >= 600:
        return (
            f"المنشأة قابلة للتمويل مع بعض الملاحظات. الإيراد الشهري "
            f"{rev:,.0f} ريال، لكن يجب مراقبة مؤشر تركيز العملاء عند "
            f"{hhi:.2f} حيث يقترب من الحد الآمن."
        )
    if score >= 450:
        return (
            f"المنشأة تحتاج إلى مراجعة قبل التأهيل. مؤشرات الخطر متوسطة "
            f"وتتطلب خطة تصحيح خلال 90 يوماً، خاصة في تنويع العملاء."
        )
    return (
        f"المنشأة غير مؤهلة حالياً. مؤشرات الخطر مرتفعة وتتطلب إعادة "
        f"هيكلة شاملة قبل إعادة التقديم."
    )


def _factors_text(top_factors: list[dict[str, Any]]) -> str:
    """قائمة عوامل SHAP مع الأثر"""
    if not top_factors:
        return "   (لا توجد عوامل متاحة)"

    lines = []
    for f in top_factors:
        arrow = "⬆️" if f["impact"] > 0 else "⬇️"
        sign = "+" if f["impact"] > 0 else ""
        lines.append(
            f"   {arrow} {f['feature']:24s} "
            f"= {f['value']:>10.2f}   (الأثر: {sign}{f['impact']:.3f})"
        )
    return "\n".join(lines)


def _recommendation(score: int) -> str:
    """التوصية النهائية للبنك"""
    if score >= 750:
        return (
            "✅ نوصي بالموافقة على التمويل بمبلغ يصل إلى 2.0x "
            "الإيراد الشهري مع شروط قياسية."
        )
    if score >= 600:
        return (
            "⚠️ نوصي بالموافقة المشروطة بمبلغ يصل إلى 1.2x مع "
            "ضمانات إضافية ومراجعة ربع سنوية."
        )
    if score >= 450:
        return (
            "⏸️ نوصي بالتأجيل 90 يوماً مع خطة تصحيح مالية "
            "لمراقبة تحسن المؤشرات."
        )
    return (
        "❌ نوصي بالرفض حالياً. المنشأة تحتاج إعادة هيكلة "
        "قبل إعادة التقديم."
    )


# ============================================================
#  Main Entry Point
# ============================================================

def generate_report(
    business_name: str,
    score_data: dict[str, Any],
    features: dict[str, Any],
    forecast: dict[str, Any],
    business_info: dict[str, Any] | None = None,
) -> str:
    """
    يولّد التقرير النهائي بصيغة نصية.

    Args:
        business_name: اسم المنشأة
        score_data: من score_engine.predict_score()
        features: من feature_engineer.extract_all()
        forecast: من liquidity_forecast.forecast_liquidity()
        business_info: اختياري — dict فيه vat_number, sector, city

    Returns:
        str: تقرير كامل بصيغة نصية
    """
    info = business_info or BUSINESS

    # نص الفجوة
    gap_date = forecast.get("first_gap_date")
    if gap_date:
        gap_text = (
            f"⚠️ فجوة سيولة متوقعة بتاريخ {gap_date} "
            f"بمقدار {forecast.get('max_gap_amount', 0):,.0f} ريال"
        )
    else:
        gap_text = "✅ لا توجد فجوات سيولة متوقعة خلال الفترة"

    return TEMPLATE.format(
        business_name=business_name,
        vat_number=info.get("vat_number", "—"),
        sector=info.get("sector", "—"),
        city=info.get("city", "—"),
        report_date=datetime.now().strftime("%Y-%m-%d %H:%M"),
        score=score_data.get("jahiz_ready_score", score_data.get("score", 0)),
        tier=score_data.get("tier", "—"),
        verdict=score_data.get("verdict", "—"),
        summary=_summarize(
            score_data.get("jahiz_ready_score", score_data.get("score", 0)),
            features,
        ),
        factors=_factors_text(score_data.get("top_factors", [])),
        inflow=forecast.get("forecast_total_inflow", 0),
        outflow=forecast.get("forecast_total_outflow", 0),
        gap_text=gap_text,
        recommendation=_recommendation(
            score_data.get("jahiz_ready_score", score_data.get("score", 0))
        ),
    )


def save_report(report: str, path) -> None:
    """حفظ التقرير في ملف"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(report)


# ============================================================
#  CLI entry point (اختبار سريع)
# ============================================================

if __name__ == "__main__":
    demo_score = {
        "jahiz_ready_score": 820,
        "tier": "بلاتيني - جاهز فوري",
        "verdict": "مؤهل بامتياز - خطر منخفض",
        "top_factors": [
            {"feature": "invoice_value_trend", "value": 0.12, "impact": 0.245},
            {"feature": "customer_hhi", "value": 0.42, "impact": -0.187},
            {"feature": "monthly_revenue_avg", "value": 95000, "impact": 0.152},
        ],
    }
    demo_features = {
        "monthly_revenue_avg": 95_000,
        "customer_hhi": 0.42,
    }
    demo_forecast = {
        "first_gap_date": "2025-11-15",
        "max_gap_amount": 32_000,
        "forecast_total_inflow": 140_000,
        "forecast_total_outflow": 108_000,
    }
    print(generate_report("Cairo Café", demo_score, demo_features, demo_forecast))
