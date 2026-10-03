<div align="center">

<img src="docs/screenshots/banner.png" alt="JAHIZ Banner" width="100%">

# جاهز | JAHIZ

### محرك الجاهزية التمويلية الفوري للمنشآت الصغيرة والمتوسطة

**هاكاثون التقنية المالية | منشآت × البنك السعودي للاستثمار**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-14-000000?style=for-the-badge&logo=next.js&logoColor=white)](https://nextjs.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

</div>

---

## 🎯 المشكلة

> **78%** من طلبات تمويل المنشآت الصغيرة والمتوسطة في السعودية تُرفض — ليس لعدم أهليتها، بل لعدم قدرة البنوك على "رؤيتها" بسبب غياب القوائم المالية المدققة.

النتيجة:
- **5 مليار ريال** في محفظة البنك السعودي للاستثمار تبقى نائمة
- **22 يوماً** متوسط زمن الموافقة على التمويل
- منشآت حقيقية مثل "منيرة - صاحبة كافيه" تُغلق فروعها بسبب فجوات سيولة لم تكن متوقعة

---

## 💡 الحل

**جاهز** يبني "اللغة المشتركة" بين المنشأة والبنك في **60 ثانية**، من خلال ربط 3 مصادر بيانات:

| المصدر | ما يقدمه |
|:---:|:---|
| 🧾 **ZATCA e-Invoicing** | الإيراد الحقيقي، تركيز العملاء، الموسمية |
| 💳 **Mada / POS** | التدفق اليومي، سلوك الدفع |
| 🏦 **Open Banking (Lean)** | المصاريف، الرواتب، الإيجار، الموردين |

### المخرجات:

- **JAHIZ-Ready Score** من 1000 مع تفسير SHAP لكل نقطة
- **تنبؤ بفجوات السيولة قبل 45 يوماً** مع خطة سداد موسمية
- **تقرير ائتماني ذكي** للبنك يشرح لماذا هذا السكور؟ ما المخاطر؟ ما التوصية؟

---

## 📊 الأثر القابل للقياس

| المؤشر | قبل | بعد |
|:---|:---:|:---:|
| ⏱️ زمن الموافقة | 22 يوماً | **5 دقائق** |
| ✅ نسبة القبول | 22% | **65%** |
| 🔔 الإنذار المبكر للتعثر | ❌ غائب | **45 يوماً مقدماً** |
| 🎯 دقة النموذج | — | **85%+** |

---

## 🏗️ البنية التقنية

```mermaid
flowchart LR
    A[ZATCA<br/>e-Invoicing] --> D[JAHIZ AI Engine]
    B[Mada / POS] --> D
    C[Open Banking<br/>Lean] --> D
    D --> E[JAHIZ-Ready<br/>Score 0-1000]
    D --> F[Liquidity<br/>Alert 45d]
    D --> G[Smart Bank<br/>Report]

    style D fill:#0F766E,color:#fff
    style E fill:#14B8A6,color:#fff
    style F fill:#14B8A6,color:#fff
    style G fill:#14B8A6,color:#fff
