"""
JAHIZ - Full Pipeline Orchestrator

يشغّل كل شيء من البداية للنهاية:
1. توليد/تحميل البيانات
2. استخراج الميزات
3. التنبؤ بالسيولة
4. حساب JAHIZ-Ready Score
5. توليد تقرير البنك
"""
from __future__ import annotations

from typing import Any

import pandas as pd

from app.bank_report import generate_report, save_report
from app.config import BUSINESS, DATA_DIR
from app.data_generator import save_all
from app.feature_engineer import extract_all, features_summary
from app.liquidity_forecast import build_daily_net, forecast_liquidity, gap_summary
from app.score_engine import predict_score, score_summary, train_model


def run_full_pipeline(regenerate_data: bool = False) -> dict[str, Any]:
    """
    يشغّل خط الأنابيب الكامل.

    Args:
        regenerate_data: إذا True، يولّد بيانات جديدة أولاً.

    Returns:
        dict يحتوي على: features, score, forecast, report
    """
    print("=" * 60)
    print("🚀  JAHIZ - Full Pipeline")
    print("=" * 60)

    # ---------------------------------------------------------
    # 1. البيانات
    # ---------------------------------------------------------
    if regenerate_data:
        print("\n📦 [1/5] توليد البيانات...")
        inv, _pos, bank = save_all()
    else:
        print("\n📦 [1/5] تحميل البيانات...")
        inv = pd.read_csv(
            DATA_DIR / "invoices.csv",
            parse_dates=["issue_date"],
        )
        bank = pd.read_csv(
            DATA_DIR / "bank.csv",
            parse_dates=["date"],
        )

    # ---------------------------------------------------------
    # 2. الميزات
    # ---------------------------------------------------------
    print("\n🔧 [2/5] استخراج الميزات...")
    features = extract_all(inv, bank)
    print(features_summary(features))

    # ---------------------------------------------------------
    # 3. التنبؤ بالسيولة
    # ---------------------------------------------------------
    print("\n📈 [3/5] التنبؤ بالسيولة (Prophet)...")
    net = build_daily_net(bank, inv)
    forecast = forecast_liquidity(net)
    print(f"     {gap_summary(forecast)}")

    # ---------------------------------------------------------
    # 4. السكور
    # ---------------------------------------------------------
    print("\n🧠 [4/5] تدريب النموذج وحساب السكور...")
    model, explainer = train_model()
    score_data = predict_score(features, model, explainer)
    print(score_summary(score_data))

    # ---------------------------------------------------------
    # 5. تقرير البنك
    # ---------------------------------------------------------
    print("\n📄 [5/5] توليد تقرير البنك...")
    report = generate_report(
        business_name=BUSINESS["name"],
        score_data=score_data,
        features=features,
        forecast=forecast,
    )
    report_path = DATA_DIR / "bank_report.txt"
    save_report(report, report_path)
    print(f"     ✅ التقرير محفوظ في {report_path}")

    print("\n" + "=" * 60)
    print("✨ اكتمل التشغيل بنجاح!")
    print("=" * 60)

    # فلترة النتائج (بدون model/full_forecast)
    forecast_public = {
        k: v for k, v in forecast.items()
        if k not in ("model", "full_forecast")
    }

    return {
        "features": features,
        "score": score_data,
        "forecast": forecast_public,
        "report": report,
    }


# ============================================================
#  CLI entry point
# ============================================================

if __name__ == "__main__":
    run_full_pipeline(regenerate_data=True)
