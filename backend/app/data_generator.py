
"""
JAHIZ - توليد بيانات محاكاة واقعية لمنشأة صغيرة سعودية

يولّد:
- 1,200 فاتورة إلكترونية (ZATCA format)
- معاملات مدى / نقاط بيع (Mada/POS)
- معاملات بنكية (إيجار، رواتب، موردين، ضريبة، تحصيلات)

يُستخدم كبديل عن بيانات الإنتاج في مرحلة الهاكاثون.
"""
import random
import uuid
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from faker import Faker

from app.config import (
    BUSINESS,
    DATA_DIR,
    HISTORY_DAYS,
    INVOICE_COUNT,
    RENT_DAY,
    SALARY_DAY,
    WEEKEND_DAYS,
)

fake = Faker("ar_SA")
random.seed(42)
np.random.seed(42)


# ============================================================
#  Helper functions
# ============================================================

def _customer_pool(n: int = 40) -> list:
    """
    عملاء بتركيز خطر: عميل واحد يستحوذ على 55% من الإيراد.
    هذا يحاكي واقع كثير من المنشآت الصغيرة (خطر الاعتماد على عميل واحد).
    """
    customers = [
        {"id": f"C{i:03d}", "name": fake.company(), "weight": 0.02}
        for i in range(n)
    ]
    # العملاء الكبار (تركيز خطر)
    customers[0]["weight"] = 0.55
    customers[1]["weight"] = 0.15
    customers[2]["weight"] = 0.08
    return customers


def _daily_revenue_factor(date: datetime) -> float:
    """
    معامل موسمية يومي يحاكي نمط كافيه في الرياض:
    - نهاية الأسبوع (جمعة/سبت) = ذروة
    - بداية الأسبوع = هدوء
    - نهاية الشهر (رواتب) = ارتفاع
    - رمضان = ارتفاع مسائي
    """
    factor = 1.0

    # نهاية الأسبوع - كافيه يزدهر
    if date.weekday() in WEEKEND_DAYS:
        factor *= 1.35

    # منتصف الأسبوع انخفاض
    if date.weekday() in [0, 1]:
        factor *= 0.90

    # نهاية الشهر - رواتب
    if date.day >= 25:
        factor *= 1.15

    # رمضان (تقريبي - شهر 3)
    if date.month == 3:
        factor *= 1.20

    return factor


# ============================================================
#  Generators
# ============================================================

def generate_invoices(seed: int = 42) -> pd.DataFrame:
    """توليد 1,200 فاتورة إلكترونية بصيغة ZATCA"""
    np.random.seed(seed)
    random.seed(seed)

    customers = _customer_pool()
    start = datetime.now() - timedelta(days=HISTORY_DAYS)
    rows = []
    weights = [c["weight"] for c in customers]

    for i in range(INVOICE_COUNT):
        # توزيع غير منتظم للتواريخ (بيتا) لمحاكاة سلوك حقيقي
        day_offset = int(np.random.beta(2, 2) * HISTORY_DAYS)
        date = start + timedelta(days=day_offset, hours=random.randint(8, 22))
        factor = _daily_revenue_factor(date)
        base = np.random.lognormal(mean=4.6, sigma=0.6)   # ~ 320 ريال
        amount = round(base * factor, 2)

        customer = random.choices(customers, weights=weights, k=1)[0]
        vat = round(amount * 0.15, 2)

        rows.append({
            "invoice_uuid": str(uuid.uuid4()),
            "invoice_number": f"INV-2024-{i + 1:05d}",
            "issue_date": date,
            "seller_name": BUSINESS["name"],
            "seller_vat": BUSINESS["vat_number"],
            "buyer_id": customer["id"],
            "buyer_name": customer["name"],
            "subtotal": amount,
            "vat_amount": vat,
            "total": round(amount + vat, 2),
            "payment_method": random.choice(["Mada", "Cash", "Credit"]),
            "status": "Paid" if random.random() > 0.05 else "Pending",
        })

    return (
        pd.DataFrame(rows)
        .sort_values("issue_date")
        .reset_index(drop=True)
    )


def generate_pos_transactions(invoices: pd.DataFrame) -> pd.DataFrame:
    """محاكاة معاملات مدى اليومية (كل فاتورة مدفوعة بمدى = معاملة POS)"""
    paid = invoices[invoices["payment_method"] == "Mada"].copy()
    paid["transaction_id"] = [
        f"POS-{uuid.uuid4().hex[:10].upper()}" for _ in range(len(paid))
    ]
    paid["terminal_id"] = np.random.choice(
        ["T-001", "T-002", "T-003"], size=len(paid)
    )
    return paid[
        ["transaction_id", "terminal_id", "issue_date", "total"]
    ].rename(columns={"issue_date": "timestamp", "total": "amount"})


def generate_bank_transactions(seed: int = 42) -> pd.DataFrame:
    """
    توليد معاملات بنكية:
    - إيجار شهري
    - رواتب شهرية
    - موردين أسبوعي
    - ضريبة فصلية
    - تحصيلات عشوائية
    """
    np.random.seed(seed)
    random.seed(seed)

    rows = []
    start = datetime.now() - timedelta(days=HISTORY_DAYS)

    for d in range(HISTORY_DAYS + 1):
        date = start + timedelta(days=d)

        # إيجار شهري
        if date.day == RENT_DAY:
            rows.append({
                "date": date,
                "type": "out",
                "category": "Rent",
                "amount": 18_000,
                "counterparty": "Aqar Co.",
            })

        # رواتب
        if date.day == SALARY_DAY:
            rows.append({
                "date": date,
                "type": "out",
                "category": "Salaries",
                "amount": BUSINESS["employees"] * 4_500,
                "counterparty": "Payroll",
            })

        # موردين أسبوعي (كل اثنين)
        if date.weekday() == 0:
            rows.append({
                "date": date,
                "type": "out",
                "category": "Suppliers",
                "amount": round(np.random.normal(6_500, 900), 2),
                "counterparty": fake.company(),
            })

        # ضريبة فصلية
        if date.month in (3, 6, 9, 12) and date.day == 20:
            rows.append({
                "date": date,
                "type": "out",
                "category": "VAT",
                "amount": 12_500,
                "counterparty": "ZATCA",
            })

        # تحصيلات بنكية عشوائية
        if random.random() < 0.60:
            rows.append({
                "date": date,
                "type": "in",
                "category": "Collections",
                "amount": round(np.random.lognormal(8, 0.4), 2),
                "counterparty": fake.company(),
            })

    return (
        pd.DataFrame(rows)
        .sort_values("date")
        .reset_index(drop=True)
    )


# ============================================================
#  Orchestrator
# ============================================================

def save_all():
    """يولّد ويحفظ كل البيانات في DATA_DIR"""
    print("⏳ توليد البيانات...")

    invoices = generate_invoices()
    pos = generate_pos_transactions(invoices)
    bank = generate_bank_transactions()

    invoices_path = DATA_DIR / "invoices.csv"
    pos_path = DATA_DIR / "pos.csv"
    bank_path = DATA_DIR / "bank.csv"

    invoices.to_csv(invoices_path, index=False)
    pos.to_csv(pos_path, index=False)
    bank.to_csv(bank_path, index=False)

    print(f"✅ {len(invoices):,} فاتورة       → {invoices_path.name}")
    print(f"✅ {len(pos):,} معاملة مدى    → {pos_path.name}")
    print(f"✅ {len(bank):,} معاملة بنكية → {bank_path.name}")

    return invoices, pos, bank


# ============================================================
#  CLI entry point
# ============================================================

if __name__ == "__main__":
    save_all()
