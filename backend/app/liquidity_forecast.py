"""
JAHIZ - Liquidity Forecasting Engine

يتنبأ بالتدفق النقدي اليومي للـ 45 يوماً القادمة باستخدام Prophet،
ويكتشف فجوات السيولة قبل حدوثها.

المخرجات:
- first_gap_date: أول يوم يُتوقع فيه عجز
- max_gap_amount: أقصى مبلغ عجز متوقع
- forecast_total_inflow / outflow: إجمالي التدفق الداخل/الخارج
- forecast_df: DataFrame بنقاط التنبؤ للرسم البياني

يُستخدم لاحقاً في:
1. تنبيه المنشأة قبل 45 يوماً
2. تقرير البنك الذكي
3. خطة السداد الموسمية
"""
from __future__ import annotations

import logging
from typing import Any

import numpy as np
import pandas as pd
from prophet import Prophet

from app.config import FORECAST_DAYS

# إخفاء تحذيرات Prophet و cmdstanpy
logging.getLogger("prophet").setLevel(logging.WARNING)
logging.getLogger("cmdstanpy").setLevel(logging.WARNING)


# ============================================================
#  Data Preparation
# ============================================================

def build_daily_net(
    bank: pd.DataFrame,
    invoices: pd.DataFrame,
) -> pd.DataFrame:
    """
    يجمع التدفق النقدي اليومي من كل المصادر:
    - إيرادات الفواتير الإلكترونية (inflow)
    - تحصيلات بنكية عشوائية (inflow)
    - مصاريف بنكية: إيجار، رواتب، موردين، ضريبة (outflow)

    Returns:
        DataFrame بأعمدة: ds (تاريخ), net (صافي التدفق اليومي)
    """
    if invoices.empty and bank.empty:
        raise ValueError("لا يمكن بناء التدفق من بيانات فارغة")

    # --- إيرادات الفواتير ---
    if not invoices.empty:
        inv_daily = (
            invoices.set_index("issue_date")
            .resample("D")["total"]
            .sum()
            .rename("inflow")
        )
    else:
        inv_daily = pd.Series(dtype=float, name="inflow")

    # --- مصاريف وتحصيلات بنكية ---
    if not bank.empty:
        out_daily = (
            bank[bank["type"] == "out"]
            .groupby("date")["amount"]
            .sum()
            .rename("outflow")
        )
        bank_in_daily = (
            bank[bank["type"] == "in"]
            .groupby("date")["amount"]
            .sum()
            .rename("bank_in")
        )
    else:
        out_daily = pd.Series(dtype=float, name="outflow")
        bank_in_daily = pd.Series(dtype=float, name="bank_in")

    # --- الدمج ---
    df = pd.concat([inv_daily, out_daily, bank_in_daily], axis=1).fillna(0)
    df["inflow"] = df["inflow"] + df["bank_in"]
    df["net"] = df["inflow"] - df["outflow"]

    df = df.reset_index().rename(columns={"issue_date": "ds", "index": "ds"})
    df["ds"] = pd.to_datetime(df["ds"]).dt.tz_localize(None)

    # ترتيب حسب التاريخ وملء الأيام الناقصة بصفر
    df = df.sort_values("ds").reset_index(drop=True)

    return df[["ds", "net"]]


def add_saudi_events() -> pd.DataFrame:
    """
    مناسبات سعودية تؤثر على السيولة (تُمرَّر لـ Prophet):
    - يوم الراتب (27 من كل شهر)
    - يوم الإيجار (1 من كل شهر)
    - رمضان (تقريبي)
    """
    rows = []
    for m in range(1, 13):
        rows.append({
            "holiday": "Salary Day",
            "ds": f"2025-{m:02d}-27",
            "lower_window": 0,
            "upper_window": 2,
        })
        rows.append({
            "holiday": "Rent Day",
            "ds": f"2025-{m:02d}-01",
            "lower_window": 0,
            "upper_window": 1,
        })

    # رمضان 2025 (تقريبي)
    rows.append({
        "holiday": "Ramadan",
        "ds": "2025-03-01",
        "lower_window": -30,
        "upper_window": 30,
    })

    return pd.DataFrame(rows)


# ============================================================
#  Forecasting
# ============================================================

def forecast_liquidity(
    net_df: pd.DataFrame,
    forecast_days: int = FORECAST_DAYS,
) -> dict[str, Any]:
    """
    يشغّل Prophet على التدفق اليومي ويعيد:
    - forecast_df: DataFrame للرسم البياني (ds, yhat, yhat_lower, yhat_upper, cumulative)
    - first_gap_date: أول يوم عجز متوقع (أو None)
    - max_gap_amount: أقصى عجز متوقع بالريال
    - forecast_total_inflow / outflow: إجماليات متوقعة
    - model / full_forecast: للاستخدام الداخلي (لا تُرسل للواجهة)

    Args:
        net_df: DataFrame بأعمدة ds, net من build_daily_net()
        forecast_days: عدد أيام التنبؤ (افتراضي 45)

    Returns:
        dict بكل النتائج
    """
    if net_df.empty or len(net_df) < 30:
        raise ValueError(
            f"تحتاج 30 يوماً على الأقل من البيانات، لديك {len(net_df)}"
        )

    # --- تهيئة Prophet ---
    model = Prophet(
        daily_seasonality=False,
        weekly_seasonality=True,
        yearly_seasonality=False,
        changepoint_prior_scale=0.05,
        interval_width=0.80,
    )
    model.add_country_holidays(country_name="SA")
    model.fit(net_df)

    # --- التنبؤ ---
    future = model.make_future_dataframe(periods=forecast_days)
    fc = model.predict(future)

    # --- الرصيد التراكمي ---
    fc["cumulative"] = fc["yhat"].cumsum()
    future_only = fc.tail(forecast_days).copy()

    # --- كشف أول فجوة ---
    deficit = future_only[future_only["cumulative"] < 0]
    first_gap = (
        deficit.iloc[0]["ds"].strftime("%Y-%m-%d")
        if not deficit.empty
        else None
    )
    max_gap = (
        float(future_only["cumulative"].min())
        if not deficit.empty
        else 0.0
    )

    # --- الإجماليات ---
    total_inflow = round(
        float(future_only["yhat"].clip(lower=0).sum()), 2
    )
    total_outflow = round(
        float(abs(future_only["yhat"].clip(upper=0).sum())), 2
    )

    return {
        "forecast_df": future_only[
            ["ds", "yhat", "yhat_lower", "yhat_upper", "cumulative"]
        ].reset_index(drop=True),
        "first_gap_date": first_gap,
        "max_gap_amount": round(abs(max_gap), 2),
        "forecast_total_inflow": total_inflow,
        "forecast_total_outflow": total_outflow,
        "forecast_days": forecast_days,
        "model": model,
        "full_forecast": fc,
    }


def gap_summary(result: dict[str, Any]) -> str:
    """ملخص نصي للفجوة (يُستخدم في تقرير البنك والـ logs)"""
    if result["first_gap_date"]:
        return (
            f"⚠️ فجوة سيولة متوقعة بتاريخ {result['first_gap_date']} "
            f"بمقدار {result['max_gap_amount']:,.0f} ريال"
        )
    return "✅ لا توجد فجوات سيولة متوقعة خلال الفترة"


def adaptive_repayment_plan(
    result: dict[str, Any],
    loan_amount: float,
    months: int = 12,
) -> list[dict[str, Any]]:
    """
    خطة سداد تتكيف مع موسمية المنشأة.
    الأشهر ذات التدفق الأعلى تتحمل أقساطاً أكبر.

    Returns:
        قائمة بجدول السداد المقترح
    """
    fc = result["forecast_df"]
    if fc.empty:
        return []

    # نحسب متوسط التدفق لكل شهر من فترة التنبؤ
    fc = fc.copy()
    fc["month"] = fc["ds"].dt.month
    monthly_avg = fc.groupby("month")["yhat"].mean()

    if monthly_avg.sum() <= 0:
        return []

    weights = monthly_avg / monthly_avg.sum()

    plan = []
    for m, w in weights.items():
        plan.append({
            "month": int(m),
            "weight": round(float(w), 3),
            "installment": round(loan_amount / months * (w * months), 2),
        })
    return plan


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

    net = build_daily_net(bank, inv)
    print(f"📊 أيام التدفق: {len(net)}")
    print(f"📊 متوسط التدفق اليومي: {net['net'].mean():,.0f} ريال")

    result = forecast_liquidity(net)
    print(f"\n📅 أول فجوة سيولة: {result['first_gap_date']}")
    print(f"💰 أقصى عجز متوقع: {result['max_gap_amount']:,.0f} ريال")
    print(f"📥 إجمالي التدفق المتوقع: {result['forecast_total_inflow']:,.0f} ريال")
    print(f"📤 إجمالي المصاريف المتوقعة: {result['forecast_total_outflow']:,.0f} ريال")
    print(f"\n{gap_summary(result)}")

    # حفظ نقاط التنبؤ للرسم البياني
    result["forecast_df"].to_csv(
        DATA_DIR / "forecast.csv", index=False
    )
    print(f"\n✅ نقاط التنبؤ محفوظة في {DATA_DIR / 'forecast.csv'}")
