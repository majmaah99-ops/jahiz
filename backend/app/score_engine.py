"""
JAHIZ - Scoring Engine

محرك حساب JAHIZ-Ready Score (0-1000) باستخدام XGBoost + SHAP.

المخرجات:
- jahiz_ready_score: السكور من 0 إلى 1000
- tier: تصنيف الفئة (بلاتيني/ذهبي/فضي/قيد التأهيل)
- verdict: الحكم النصي
- suggested_amount: مبلغ التمويل المقترح
- top_factors: أهم 5 عوامل مؤثرة مع تفسير SHAP

يُستخدم لاحقاً في:
1. لوحة تحكم المنشأة (عرض السكور)
2. تقرير البنك الذكي (تفسير القرار)
"""
from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd
import shap
import xgboost as xgb
from sklearn.model_selection import train_test_split

# ============================================================
#  Feature Configuration
# ============================================================

# أوزان الميزات (قابلة للمعايرة مع البنك لاحقاً)
# الإشارة: + يعني تحسين السكور، - يعني تخفيضه
FEATURE_WEIGHTS: dict[str, float] = {
    "customer_hhi":          -250,      # تركيز العملاء العالي = خطر
    "dso_days":              -3,        # كل يوم تأخير في التحصيل
    "cashflow_volatility":   -120,      # تذبذب التدفق = خطر
    "invoice_value_trend":   +200,      # نمو قيمة الفاتورة = إيجابي
    "seasonality_strength":  +30,       # موسمية معتدلة = إيجابي
    "fixed_cost_ratio":      -150,      # مصاريف ثابتة عالية = هشاشة
    "supplier_delay_days":   -2,        # تأخر السداد = ضغط سيولة
    "monthly_revenue_avg":   +0.001,    # حجم الإيراد
}

FEATURE_ORDER: list[str] = list(FEATURE_WEIGHTS.keys())


# ============================================================
#  Training Data (Synthetic)
# ============================================================

def synthetic_training(n_samples: int = 3000) -> pd.DataFrame:
    """
    بيانات محاكاة لتدريب النموذج.
    في الإنتاج: تُستبدل ببيانات SAIB الحقيقية (تاريخية مع Label التعثر).

    الهدف: التنبؤ باحتمالية "عدم التعثر" خلال 6 أشهر قادمة.
    """
    rng = np.random.default_rng(42)

    df = pd.DataFrame({
        "customer_hhi":          rng.uniform(0.05, 0.90, n_samples),
        "dso_days":              rng.uniform(5, 90, n_samples),
        "cashflow_volatility":   rng.uniform(0.10, 2.50, n_samples),
        "invoice_value_trend":   rng.uniform(-0.50, 0.60, n_samples),
        "seasonality_strength":  rng.uniform(0.80, 2.00, n_samples),
        "fixed_cost_ratio":      rng.uniform(0.20, 0.85, n_samples),
        "supplier_delay_days":   rng.uniform(0, 60, n_samples),
        "monthly_revenue_avg":   rng.uniform(30_000, 500_000, n_samples),
    })

    # حساب "سكور خام" خطي من الأوزان
    raw = sum(df[col] * w for col, w in FEATURE_WEIGHTS.items())
    raw = (raw - raw.mean()) / raw.std()      # normalize
    prob_default = 1 / (1 + np.exp(raw))      # sigmoid

    # Label: 1 = تعثر، 0 = لم يتعثر
    df["defaulted"] = (rng.random(n_samples) < prob_default).astype(int)

    return df


# ============================================================
#  Model Training
# ============================================================

def train_model() -> tuple[xgb.XGBClassifier, shap.TreeExplainer]:
    """
    يدرّب نموذج XGBoost على البيانات المحاكاة.

    Returns:
        (model, explainer): النموذج + SHAP TreeExplainer
    """
    df = synthetic_training()

    X = df[FEATURE_ORDER]
    y = 1 - df["defaulted"]     # 1 = جيد (لم يتعثر)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y,
    )

    model = xgb.XGBClassifier(
        n_estimators=300,
        max_depth=5,
        learning_rate=0.05,
        objective="binary:logistic",
        eval_metric="auc",
        random_state=42,
        tree_method="hist",       # أسرع على البيانات الكبيرة
    )
    model.fit(X_train, y_train)

    explainer = shap.TreeExplainer(model)
    return model, explainer


# ============================================================
#  Prediction
# ============================================================

def predict_score(
    features: dict[str, Any],
    model: xgb.XGBClassifier,
    explainer: shap.TreeExplainer,
) -> dict[str, Any]:
    """
    يحسب JAHIZ-Ready Score + التفسير.

    Args:
        features: dict من feature_engineer.extract_all()
        model: من train_model()
        explainer: من train_model()

    Returns:
        dict يحتوي على:
        - jahiz_ready_score: 0-1000
        - tier: التصنيف اللفظي
        - verdict: الحكم
        - suggested_amount: مبلغ التمويل المقترح
        - top_factors: أهم 5 عوامل مع أثرها
    """
    # التحقق من وجود الميزات
    missing = set(FEATURE_ORDER) - set(features.keys())
    if missing:
        raise ValueError(f"ميزات ناقصة: {missing}")

    X = pd.DataFrame([features])[FEATURE_ORDER]

    # احتمالية أن المنشأة "جيدة" (لن تتعثر)
    prob_good = float(model.predict_proba(X)[0, 1])
    score = int(round(prob_good * 1000))

    # تفسير SHAP
    shap_values = explainer.shap_values(X)[0]
    contributions = sorted(
        [
            {
                "feature": f,
                "value": float(features[f]),
                "impact": float(s),
            }
            for f, s in zip(FEATURE_ORDER, shap_values)
        ],
        key=lambda x: abs(x["impact"]),
        reverse=True,
    )

    return {
        "jahiz_ready_score": score,
        "score": score,                                  # alias للتوافق
        "probability_good": round(prob_good, 4),
        "tier": _tier(score),
        "verdict": _verdict(score),
        "suggested_amount": _suggested_amount(
            score, features["monthly_revenue_avg"]
        ),
        "top_factors": contributions[:5],
    }


# ============================================================
#  Classification Helpers
# ============================================================

def _tier(score: int) -> str:
    """تصنيف الفئة (يُعرض في تقرير البنك)"""
    if score >= 750:
        return "بلاتيني - جاهز فوري"
    if score >= 600:
        return "ذهبي - جاهز مشروط"
    if score >= 450:
        return "فضي - قريب من الجاهزية"
    return "قيد التأهيل"


def _verdict(score: int) -> str:
    """الحكم النصي التفصيلي"""
    if score >= 750:
        return "مؤهل بامتياز - خطر منخفض"
    if score >= 600:
        return "مؤهل - خطر متوسط"
    if score >= 450:
        return "يحتاج مراجعة - خطر مرتفع"
    return "غير مؤهل حالياً - خطر مرتفع جداً"


def _suggested_amount(score: int, monthly_rev: float) -> float:
    """
    مبلغ التمويل المقترح = مضاعف الإيراد الشهري × معامل السكور.

    المعامل يتدرج من 0.5x (سكور منخفض) إلى 2.0x (سكور ممتاز).
    يُقرّب لأقرب 1,000 ريال.
    """
    multiplier = 0.5 + (score / 1000) * 1.5     # 0.5 → 2.0
    return round(monthly_rev * multiplier, -3)


# ============================================================
#  Reporting Helper
# ============================================================

def score_summary(result: dict[str, Any]) -> str:
    """ملخص نصي للسكور (للعرض في logs أو تقرير البنك)"""
    lines = [
        "=" * 55,
        "  JAHIZ-Ready Score Summary",
        "=" * 55,
        f"  Score            : {result['jahiz_ready_score']} / 1000",
        f"  Tier             : {result['tier']}",
        f"  Verdict          : {result['verdict']}",
        f"  Suggested Amount : {result['suggested_amount']:,.0f} ريال",
        "-" * 55,
        "  Top Factors (SHAP):",
    ]
    for f in result["top_factors"]:
        arrow = "⬆️" if f["impact"] > 0 else "⬇️"
        lines.append(
            f"    {arrow} {f['feature']:22s} "
            f"= {f['value']:>10.2f}  (impact: {f['impact']:+.3f})"
        )
    lines.append("=" * 55)
    return "\n".join(lines)


# ============================================================
#  CLI entry point (اختبار سريع)
# ============================================================

if __name__ == "__main__":
    # بيانات منشأة "منيرة" الافتراضية
    sample_features = {
        "customer_hhi": 0.42,
        "dso_days": 35.0,
        "cashflow_volatility": 0.60,
        "invoice_value_trend": 0.12,
        "seasonality_strength": 1.25,
        "fixed_cost_ratio": 0.55,
        "supplier_delay_days": 28.0,
        "monthly_revenue_avg": 95_000.0,
    }

    print("⏳ تدريب النموذج...")
    model, explainer = train_model()

    print("📊 حساب السكور...")
    result = predict_score(sample_features, model, explainer)

    print()
    print(score_summary(result))
