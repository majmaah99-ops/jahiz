"""JAHIZ - محرك الجاهزية التمويلية الفوري
Configuration constants and paths
"""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# App metadata
APP_NAME = "JAHIZ"
APP_NAME_AR = "جاهز"
TAGLINE = "محرك الجاهزية التمويلية الفوري للمنشآت"
TAGLINE_EN = "Instant SME Financing Readiness Engine"
SCORE_NAME = "JAHIZ-Ready Score"

# Business profile (simulated "Munira's Café")
BUSINESS = {
    "name": "Cairo Café",
    "vat_number": "310123456700003",
    "sector": "Food & Beverage",
    "city": "Riyadh",
    "monthly_target": 90_000,
    "employees": 8,
    "branches": 3,
}

# Time windows
HISTORY_DAYS = 180
FORECAST_DAYS = 45
INVOICE_COUNT = 1200

# Saudi seasonality
WEEKEND_DAYS = [4, 5]       # Friday, Saturday
SALARY_DAY = 27
RENT_DAY = 1
VAT_QUARTER_MONTHS = [3, 6, 9, 12]

# Theme
COLOR_PRIMARY = "#0F766E"
COLOR_ACCENT = "#14B8A6"
