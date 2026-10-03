"""
JAHIZ - Feature Engineering Engine

استخراج ميزات الائتمان والجاهزية التمويلية من 3 مصادر:
- HHI لتركيز العملاء (خطر الاعتماد على عميل واحد)
- DSO لمتوسط أيام التحصيل
- Volatility لتذبذب التدفق النقدي
- Seasonality Strength لقوة الموسمية
- Fixed Cost Ratio لنسبة المصاريف الثابتة
- Supplier Delay لمتوسط أيام سداد الموردين

هذه الميزات تُستخدم لاحقاً في:
1. حساب JAHIZ-Ready Score (XGBoost + SHAP)
2. توليد تقرير البنك الذكي
"""
from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd


# ============================================================
#  Individual Feature Extractors
# ============================================================

def customer_concentration_hhi(invoices: pd.DataFrame) -> float:
    """
    مؤشر Herfindahl-Hirschman لتركيز العملاء.
    - النطاق: 0 (موزع تماماً) إلى 1 (عميل واحد يحتكر)
    - > 0.25 = خطر عالي
    - > 0.50 = خطر حرج
    """
    revenue = invoices.groupby("buyer_id")["total"].sum()
    if revenue.empty or revenue.sum() == 0:
        return 0.0
    shares = revenue / revenue.sum()
    return float((shares ** 2).sum())


def days_sales_outstanding(invoices: pd.DataFrame) -> float:
    """
    DSO: متوسط أيام التحصيل (تقديري).
    كلما ارتفع، كلما زاد الضغط على السيولة.
    - < 30 = ممتاز
    - 30-60 = متوسط
    - > 60 = خطر
    """
    daily = invoices.set_index("issue_date").resample("D")["total"].sum()
    if daily.empty or daily.mean() == 0:
        return 0.0
    return float((daily.rolling(30).mean().iloc[-1] / daily.mean()) * 30)


def cashflow_volatility(bank: pd.DataFrame) -> float:
    """
    معامل الاختلاف (CV) للتدفق النقدي اليومي.
    - < 0.5 = مستقر
    - 0.5-1.5 = متوسط
    - > 1.5 = متذبذب
    """
    if bank.empty:
        return 0.0

    df = bank.copy()
    df["signed"] = df.apply(
        lambda r: r["amount"] if r["type"] == "in" else -r["amount"],
        axis=1,
    )
    net = df.groupby(df["date"].dt.date)["signed"].sum()

    if net.empty or net.mean() == 0:
        return 0.0
    return float(net.std() / abs(net.mean()))


def avg_invoice_trend(invoices: pd.DataFrame) -> float:
    """
    نسبة تغير متوسط قيمة الفاتورة:
    آخر 30 يوم مقابل أول 30 يوم.
    - > 0 = نمو
    - < 0 = تراجع في الطلب أو تخفيض اضطراري
    """
    daily = (
        invoices.set_index("issue_date")
        .resample("D")["total"]
        .mean()
        .dropna()
    )
    if len(daily) < 60:
        return 0.0

    recent = daily.iloc[-30:].mean()
    older = daily.iloc[:30].mean()
    if older == 0:
        return 0.0
    return float((recent - older) / older)


def seasonality_strength(invoices: pd.DataFrame) -> float:
    """
    قوة الموسمية الأسبوعية:
    (متوسط نهاية الأسبوع) ÷ (متوسط أيام الأسبوع)
    - 1.0 = لا موسمية
    - > 1.3 = موسمية قوية
    - < 0.8 = اعتماد على أيام الأسبوع
    """
    daily = invoices.set_index("issue_date").resample("D")["total"].sum()
    if daily.empty:
        return 1.0

    weekend_mask = daily.index.weekday.isin([4, 5])
    weekend = daily[weekend_mask].mean()
    weekday = daily[~weekend_mask].mean()

    if pd.isna(weekday) or weekday == 0:
        return 1.0
    return float(weekend / weekday)


def fixed_cost_ratio(bank: pd.DataFrame) -> float:
    """
    نسبة المصاريف الثابتة (رواتب + إيجار) من إجمالي المصاريف.
    - < 0.40 = مرونة عالية
    - 0.40-0.65 = متوسط
    - > 0.65 = هشاشة (خطر عند انخفاض الإيراد)
    """
    out = bank[bank["type"] == "out"]
    if out.empty:
        return 0.0

    fixed = out[out["category"].isin(["Rent", "Salaries"])]["amount"].sum()
    total = out["amount"].sum()
    return float(fixed / total) if total else 0.0


def supplier_payment_delay(bank: pd.DataFrame) -> float:
    """
    متوسط أيام سداد الموردين (تقديري).
    ارتفاعه = مؤشر ضغط سيولة مبكر.
    """
    suppliers = bank[
        (bank["type"] == "out") & (bank["category"] == "Suppliers")
    ]
    if len(suppliers) < 2:
        return 0.0

    gaps = suppliers["date"].diff().dt.days.dropna()
    if gaps.empty:
        return 0.0
    return float(gaps.mean())


def monthly_revenue_avg(invoices: pd.DataFrame) -> float:
    """متوسط الإيراد الشهري (يُستخدم في حساب مبلغ التمويل المقترح)"""
    if invoices.empty:
        return 0.0
    monthly = (
        invoices.set_index("issue_date")
        .resample("ME")["total"]
        .sum()
    )
    return float(monthly.mean()) if not monthly.empty else 0.0


# ============================================================
#  Orchestrator
# ============================================================

def extract_all(
    invoices: pd.DataFrame,
    bank: pd.DataFrame,
) -> dict[str, Any]:
    """
    يستخرج كل الميزات في قاموس واحد موحّد.

    Args:
        invoices: DataFrame من data_generator.generate_invoices()
        bank: DataFrame من data_generator.generate_bank_transactions()

    Returns:
        dict بمفاتيح موحّدة تُستخدم في score_engine و bank_report
    """
    features = {
        "customer_hhi":          round(customer_concentration_hhi(invoices), 3),
        "dso_days":              round(days_sales_outstanding(invoices), 1),
        "cashflow_volatility":   round(cashflow_volatility(bank), 3),
        "invoice_value_trend":   round(avg_invoice_trend(invoices), 3),
        "seasonality_strength":  round(seasonality_strength(invoices), 3),
        "fixed_cost_ratio":      round(fixed_cost_ratio(bank), 3),
        "supplier_delay_days":   round(supplier_payment_delay(bank), 1),
        "monthly_revenue_avg":   round(monthly_revenue_avg(invoices), 2),
    }
    return features


def features_summary(features: dict[str, Any]) -> str:
    """نص ملخص للعرض في السجلات أو تقرير البنك"""
    lines = ["=" * 50, "  JAHIZ - Feature Summary", "=" * 50]
    for k, v in features.items():
        if isinstance(v, float) and v > 1000:
            lines.append(f"  {k:25s}: {v:>15,.0f}")
        else:
            lines.append(f"  {k:25s}: {v:>15}")
    lines.append("=" * 50)
    return "\n".join(lines)


# ============================================================
#  CLI entry point (اختبار سريع)
# ============================================================

if __name__ == "__main__":
    from app.config import DATA_DIR

    inv = pd.read_csv(
        DATA_DIR / "invoices.csv",
        parse_dates=["issue_date"],
    )
    bank = pd.read_csv(
        DATA_DIR / "bank.csv",
        parse_dates=["date"],
    )

    features = extract_all(inv, bank)
    print(features_summary(features))
