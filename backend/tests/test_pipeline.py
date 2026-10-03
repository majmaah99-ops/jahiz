"""
JAHIZ - Unit & Integration Tests

يختبر:
- توليد البيانات
- استخراج الميزات
- التنبؤ بالسيولة
- حساب السكور
- توليد التقرير
"""
from __future__ import annotations

import pytest

from app.bank_report import generate_report
from app.data_generator import (
    generate_bank_transactions,
    generate_invoices,
    generate_pos_transactions,
)
from app.feature_engineer import extract_all
from app.liquidity_forecast import build_daily_net, forecast_liquidity
from app.score_engine import predict_score, train_model


# ============================================================
#  Fixtures
# ============================================================

@pytest.fixture(scope="module")
def sample_data():
    """يُولَّد مرة واحدة لكل الوحدة"""
    invoices = generate_invoices()
    bank = generate_bank_transactions()
    return invoices, bank


@pytest.fixture(scope="module")
def trained_model():
    """يدرّب النموذج مرة واحدة"""
    return train_model()


# ============================================================
#  Data Generator Tests
# ============================================================

def test_invoice_count():
    """يجب توليد 1,200 فاتورة"""
    invoices = generate_invoices()
    assert len(invoices) == 1200


def test_invoice_columns():
    """التأكد من الأعمدة المطلوبة"""
    invoices = generate_invoices()
    required = {
        "invoice_uuid", "invoice_number", "issue_date",
        "seller_name", "buyer_id", "total", "payment_method",
    }
    assert required.issubset(invoices.columns)


def test_pos_transactions(sample_data):
    """معاملات POS أقل من الفواتير (فقط مدى)"""
    invoices, _ = sample_data
    pos = generate_pos_transactions(invoices)
    assert len(pos) <= len(invoices)
    assert "transaction_id" in pos.columns


def test_bank_transactions(sample_data):
    """معاملات بنكية غير فارغة"""
    _, bank = sample_data
    assert len(bank) > 0
    assert {"date", "type", "category", "amount"}.issubset(bank.columns)


# ============================================================
#  Feature Engineering Tests
# ============================================================

def test_features_extraction(sample_data):
    """كل الميزات تُستخرج في النطاق الصحيح"""
    invoices, bank = sample_data
    features = extract_all(invoices, bank)

    assert 0 <= features["customer_hhi"] <= 1
    assert features["monthly_revenue_avg"] > 0
    assert features["dso_days"] >= 0
    assert features["fixed_cost_ratio"] >= 0
    assert features["fixed_cost_ratio"] <= 1
    assert len(features) == 8  # عدد الميزات المتوقعة


# ============================================================
#  Liquidity Forecast Tests
# ============================================================

def test_forecast_runs(sample_data):
    """Prophet يعمل ويعيد النتائج المتوقعة"""
    invoices, bank = sample_data
    net = build_daily_net(bank, invoices)
    result = forecast_liquidity(net)

    assert "first_gap_date" in result
    assert "max_gap_amount" in result
    assert result["forecast_total_inflow"] > 0
    assert result["forecast_total_outflow"] > 0
    assert len(result["forecast_df"]) == 45


def test_forecast_df_columns(sample_data):
    """أعمدة forecast_df صحيحة للرسم"""
    invoices, bank = sample_data
    net = build_daily_net(bank, invoices)
    result = forecast_liquidity(net)
    expected = {"ds", "yhat", "yhat_lower", "yhat_upper", "cumulative"}
    assert expected.issubset(result["forecast_df"].columns)


# ============================================================
#  Score Engine Tests
# ============================================================

def test_score_range(sample_data, trained_model):
    """السكور بين 0 و 1000"""
    invoices, bank = sample_data
    features = extract_all(invoices, bank)
    model, explainer = trained_model
    result = predict_score(features, model, explainer)

    assert 0 <= result["jahiz_ready_score"] <= 1000
    assert result["verdict"]
    assert result["tier"]
    assert result["suggested_amount"] > 0
    assert len(result["top_factors"]) == 5


def test_score_missing_features(trained_model):
    """رسالة خطأ واضحة عند نقص الميزات"""
    model, explainer = trained_model
    with pytest.raises(ValueError, match="ميزات ناقصة"):
        predict_score({"customer_hhi": 0.5}, model, explainer)


# ============================================================
#  Bank Report Tests
# ============================================================

def test_report_generation(sample_data, trained_model):
    """التقرير يُولَّد بنجاح"""
    invoices, bank = sample_data
    features = extract_all(invoices, bank)
    model, explainer = trained_model
    score = predict_score(features, model, explainer)

    net = build_daily_net(bank, invoices)
    forecast = forecast_liquidity(net)
    forecast_public = {
        k: v for k, v in forecast.items()
        if k not in ("model", "full_forecast", "forecast_df")
    }

    report = generate_report("Test Café", score, features, forecast_public)
    assert "JAHIZ" in report
    assert "Test Café" in report
    assert str(score["jahiz_ready_score"]) in report
