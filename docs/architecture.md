# JAHIZ Architecture

> **محرك الجاهزية التمويلية الفوري للمنشآت الصغيرة والمتوسطة**
> Instant SME Financing Readiness Engine

---

## 📑 الفهرس

1. [نظرة عامة](#1-نظرة-عامة)
2. [المعمارية العامة](#2-المعمارية-العامة)
3. [مصادر البيانات](#3-مصادر-البيانات)
4. [محرك الذكاء الاصطناعي](#4-محرك-الذكاء-الاصطناعي)
5. [تدفق البيانات](#5-تدفق-البيانات)
6. [المكدس التقني](#6-المكدس-التقني)
7. [الأمان والامتثال](#7-الأمان-والامتثال)
8. [قابلية التوسع](#8-قابلية-التوسع)
9. [النشر والتشغيل](#9-النشر-والتشغيل)
10. [خارطة الطريق](#10-خارطة-الطريق)

---

## 1. نظرة عامة

**JAHIZ** منصة ذكاء اصطناعي تربط 3 مصادر بيانات مالية ومنشآت في **60 ثانية**، لتمنح:

| المخرج | الوصف | المستفيد |
|:---|:---|:---|
| 🎯 **JAHIZ-Ready Score** | سكور من 0 إلى 1000 مع تفسير SHAP | البنك + المنشأة |
| 🔔 **Liquidity Alert** | تنبؤ بفجوة سيولة قبل 45 يوماً | المنشأة |
| 📄 **Smart Bank Report** | تقرير ائتماني ذكي جاهز للقرار | البنك |

### المشكلة التي يحلها

### الحل

بناء **لغة مالية مشتركة** بين المنشأة والبنك، مستخرجة من بيانات موجودة فعلاً:
- 🧾 الفاتورة الإلكترونية (ZATCA)
- 💳 معاملات مدى / نقاط البيع
- 🏦 الحساب البنكي عبر المصرفية المفتوحة

---

## 2. المعمارية العامة

JAHIZ مبني على معمارية **3-tier** مع فصل صريح بين الواجهة، الخلفية، ومحرك الذكاء الاصطناعي.



---

## 3. مصادر البيانات

### 3.1 ZATCA e-Invoicing

| البُعد | التفاصيل |
|:---|:---|
| **طريقة الربط** | REST API + OAuth 2.0 |
| **البيانات المستخرجة** | فواتير، مشتريات، ضريبة، تركز العملاء |
| **التحديث** | Real-time / Daily batch |
| **الاستخدام** | الإيراد الحقيقي، مؤشر HHI، الموسمية |

**الميزات المستخرجة:**
- `customer_hhi` — تركيز العملاء
- `invoice_value_trend` — نمو قيمة الفاتورة
- `monthly_revenue_avg` — متوسط الإيراد الشهري

### 3.2 Mada / POS

| البُعد | التفاصيل |
|:---|:---|
| **طريقة الربط** | API من مزود نقاط البيع |
| **البيانات المستخرجة** | معاملات يومية، توزيع زمني |
| **التحديث** | Real-time |
| **الاستخدام** | التدفق اليومي، سلوك الدفع |

### 3.3 Open Banking (Lean Technologies)

| البُعد | التفاصيل |
|:---|:---|
| **طريقة الربط** | Lean SDK + OAuth 2.0 + PKCE |
| **البيانات المستخرجة** | رصيد، تحويلات، مصاريف، رواتب، إيجار |
| **التحديث** | Daily / On-demand |
| **الاستخدام** | المصاريف، الرواتب، الموردين، DSO |

**الميزات المستخرجة:**
- `cashflow_volatility` — تذبذب التدفق
- `fixed_cost_ratio` — نسبة المصاريف الثابتة
- `supplier_delay_days` — تأخر سداد الموردين
- `dso_days` — متوسط أيام التحصيل

---

## 4. محرك الذكاء الاصطناعي

### 4.1 تصنيف الفواتير والمصاريف


| المقياس | القيمة |
|:---|:---:|
| **البيانات التدريبية** | 12,000 فاتورة |
| **الدقة** | 92% |
| **زمن الاستدلال** | < 50ms / فاتورة |

### 4.2 التنبؤ بالسيولة


| المقياس | القيمة |
|:---|:---:|
| **نافذة التنبؤ** | 45 يوماً |
| **MAPE** | < 12% |
| **الموسمية المدمجة** | رواتب، إيجار، رمضان |
| **التحذير المبكر** | 45 يوماً قبل الفجوة |

**كيف يعمل Prophet؟**

### 4.3 السكور الائتماني


**الميزات الثمانية وأوزانها:**

| الميزة | الوزن | التأثير |
|:---|:---:|:---:|
| `customer_hhi` | -250 | ⬇️ كلما زاد تركيز العملاء |
| `dso_days` | -3 / يوم | ⬇️ كلما طال التحصيل |
| `cashflow_volatility` | -120 | ⬇️ كلما زاد التذبذب |
| `invoice_value_trend` | +200 | ⬆️ نمو قيمة الفاتورة |
| `seasonality_strength` | +30 | ⬆️ موسمية معتدلة |
| `fixed_cost_ratio` | -150 | ⬇️ هشاشة عالية |
| `supplier_delay_days` | -2 / يوم | ⬇️ ضغط سيولة |
| `monthly_revenue_avg` | +0.001 | ⬆️ حجم الإيراد |

**الفئات (Tiers):**

| السكور | الفئة | الحكم |
|:---:|:---|:---|
| 750-1000 | 🏆 بلاتيني | مؤهل بامتياز — جاهز فوري |
| 600-749 | 🥇 ذهبي | مؤهل — جاهز مشروط |
| 450-599 | 🥈 فضي | يحتاج مراجعة |
| 0-449 | ⏳ قيد التأهيل | غير مؤهل حالياً |

### 4.4 تقرير البنك الذكي


**بنية التقرير:**
1. JAHIZ-Ready Score + الفئة + الحكم
2. الملخص التنفيذي
3. المحركات الرئيسية (SHAP)
4. تنبؤ السيولة 45 يوماً
5. التوصية النهائية
6. الشفافية والمصادر

---

## 5. تدفق البيانات

```mermaid
sequenceDiagram
    autonumber
    participant U as User (Munira)
    participant F as Frontend (Next.js)
    participant B as Backend (FastAPI)
    participant AI as AI Engine
    participant DB as PostgreSQL

    Note over U,F: Step 1: Onboarding (60s)
    U->>F: ربط ZATCA (OAuth)
    U->>F: ربط Mada/POS (API Key)
    U->>F: ربط الحساب البنكي (Lean)
    F->>B: POST /connect (3 tokens)

    Note over B,AI: Step 2: Feature Extraction
    B->>AI: extract_all(invoices, bank)
    AI-->>B: 8 features

    Note over B,AI: Step 3: Liquidity Forecast
    B->>AI: forecast_liquidity(net)
    AI-->>B: 45-day forecast + gap

    Note over B,AI: Step 4: Scoring
    B->>AI: predict_score(features)
    AI-->>B: score + tier + SHAP

    Note over B,AI: Step 5: Bank Report
    B->>AI: generate_report()
    AI-->>B: Markdown report

    B->>DB: Save analysis (metadata only)
    B-->>F: Full JSON response
    F-->>U: Dashboard + Score + Report

OAuth 2.0 + PKCE
    ↓
JWT (short-lived, 15 min)
    ↓
Refresh Token (7 days)
Load Balancer (Nginx)
       │
       ├── App Instance 1 ──┐
       ├── App Instance 2 ──┼── PostgreSQL (Primary + Replica)
       └── App Instance 3 ──┘   Redis (Sentinel)
Push to main
    ↓
GitHub Actions:
  1. Install deps
  2. Generate synthetic data
  3. Run pipeline smoke test
  4. Run pytest (coverage > 80%)
  5. Lint (ruff + black)
    ↓
Deploy:
  - Frontend → Vercel (auto)
  - Backend → Railway (auto)
    ↓
Health check → Notify (Slack)
# App
APP_NAME=JAHIZ
ENVIRONMENT=production
LOG_LEVEL=INFO

# Database
DATABASE_URL=postgresql://...
REDIS_URL=redis://...

# Integrations
LEAN_APP_ID=...
LEAN_APP_SECRET=...
ZATCA_CLIENT_ID=...
ZATCA_CLIENT_SECRET=...

# LLM
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini

# Security
JWT_SECRET=...
ENCRYPTION_KEY=...
