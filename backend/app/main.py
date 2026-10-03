"""
JAHIZ - FastAPI Application

يخدم لوحة التحكم في الهاكاثون عبر endpoint واحد رئيسي.

Endpoints:
- GET  /              : معلومات المشروع
- POST /analyze       : تحليل كامل لمنشأة (سكور + تنبؤ + تقرير)
- GET  /forecast      : نقاط التنبؤ للرسم البياني
- GET  /health        : فحص الصحة
"""
from __future__ import annotations

from typing import Any

import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.bank_report import generate_report
from app.config import (
    APP_NAME,
    APP_NAME_AR,
    BUSINESS,
    DATA_DIR,
    SCORE_NAME,
    TAGLINE,
)
from app.feature_engineer import extract_all
from app.liquidity_forecast import build_daily_net, forecast_liquidity
from app.score_engine import predict_score, train_model


# ============================================================
#  App Initialization
# ============================================================

app = FastAPI(
    title=f"{APP_NAME} | {APP_NAME_AR}",
    description=TAGLINE,
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# تدريب النموذج مرة واحدة عند الإقلاع
print("⏳ تدريب النموذج عند الإقلاع...")
MODEL, EXPLAINER = train_model()
print("✅ النموذج جاهز")


# ============================================================
#  Pydantic Response Models
# ============================================================

class ForecastInfo(BaseModel):
    first_gap_date: str | None
    max_gap_amount: float
    forecast_total_inflow: float
    forecast_total_outflow: float


class AnalyzeResponse(BaseModel):
    jahiz_ready_score: int
    tier: str
    verdict: str
    suggested_amount: float
    top_factors: list[dict[str, Any]]
    liquidity_forecast: ForecastInfo
    bank_report: str
    features: dict[str, Any]


# ============================================================
#  Endpoints
# ============================================================

@app.get("/")
def root() -> dict[str, Any]:
    """معلومات المشروع"""
    return {
        "app": APP_NAME,
        "name_ar": APP_NAME_AR,
        "tagline": TAGLINE,
        "score_name": SCORE_NAME,
        "business": BUSINESS["name"],
        "status": "ready",
    }


@app.get("/health")
def health() -> dict[str, str]:
    """فحص الصحة"""
    return {"status": "ok"}


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze() -> AnalyzeResponse:
    """
    المسار الرئيسي: يحلل المنشأة ويعيد:
    - JAHIZ-Ready Score
    - تنبؤ السيولة 45 يوم
    - تقرير البنك الذكي
    """
    try:
        inv = pd.read_csv(
            DATA_DIR / "invoices.csv",
            parse_dates=["issue_date"],
        )
        bank = pd.read_csv(
            DATA_DIR / "bank.csv",
            parse_dates=["date"],
        )
    except FileNotFoundError:
        raise HTTPException(
            400,
            "البيانات غير موجودة. شغّل `python -m app.data_generator` أولاً.",
        )

    # الميزات والسكور
    features = extract_all(inv, bank)
    score_data = predict_score(features, MODEL, EXPLAINER)

    # التنبؤ
    net = build_daily_net(bank, inv)
    forecast = forecast_liquidity(net)
    fc_public = {
        k: v for k, v in forecast.items()
        if k not in ("model", "full_forecast", "forecast_df")
    }

    # التقرير
    report = generate_report(
        business_name=BUSINESS["name"],
        score_data=score_data,
        features=features,
        forecast=fc_public,
    )

    return AnalyzeResponse(
        jahiz_ready_score=score_data["jahiz_ready_score"],
        tier=score_data["tier"],
        verdict=score_data["verdict"],
        suggested_amount=score_data["suggested_amount"],
        top_factors=score_data["top_factors"],
        liquidity_forecast=ForecastInfo(
            first_gap_date=fc_public["first_gap_date"],
            max_gap_amount=fc_public["max_gap_amount"],
            forecast_total_inflow=fc_public["forecast_total_inflow"],
            forecast_total_outflow=fc_public["forecast_total_outflow"],
        ),
        bank_report=report,
        features=features,
    )


@app.get("/forecast")
def get_forecast() -> list[dict[str, Any]]:
    """إرجاع نقاط التنبؤ للرسم البياني في الواجهة"""
    try:
        inv = pd.read_csv(
            DATA_DIR / "invoices.csv",
            parse_dates=["issue_date"],
        )
        bank = pd.read_csv(
            DATA_DIR / "bank.csv",
            parse_dates=["date"],
        )
    except FileNotFoundError:
        raise HTTPException(400, "البيانات غير موجودة.")

    net = build_daily_net(bank, inv)
    result = forecast_liquidity(net)
    fc = result["forecast_df"].copy()
    fc["ds"] = fc["ds"].dt.strftime("%Y-%m-%d")
    return fc.to_dict(orient="records")


# ============================================================
#  CLI entry point (تشغيل مباشر)
# ============================================================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
