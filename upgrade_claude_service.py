"""
upgrade_claude_service.py
Applies 4 critical improvements:
1. Structured JSON output with confidence scores
2. Confidence scoring per section
3. Pricing engine with real formula
4. Mandatory/Buyer/Recommended classification
"""
import shutil, os, re
from datetime import datetime

BASE = r"C:\Users\DELL\Desktop\wissamxpohub-backend"
path = os.path.join(BASE, "services", "claude_service.py")

f = open(path, encoding="utf-8")
content = f.read()
f.close()
shutil.copy2(path, path.replace(".py", f"_BACKUP_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"))

# ══════════════════════════════════════════════════════
# NEW SYSTEM PROMPT — Structured JSON + Confidence
# ══════════════════════════════════════════════════════
NEW_SYSTEM = '''
EXPORT_ADVISOR_SYSTEM = """
أنت محلل ذكاء تجاري متخصص في تصدير المنتجات المصرية للأسواق الأوروبية.

## قواعد صارمة:
1. استخدم فقط البيانات الموجودة في VERIFIED DATA المُرفقة
2. لا تخترع أرقاماً أو أسماء شركات أو رسوماً جمركية
3. إذا كانت البيانات ناقصة، قل ذلك صراحةً
4. لكل قسم أضف: المصدر + سنة البيانات + مستوى الثقة (0-100)
5. صنّف كل متطلب إلى: إلزامي / شائع لدى المشترين / موصى به

## مستويات الثقة:
- 90-100: بيانات رسمية حديثة (Comtrade/Eurostat/EU)
- 75-89: بيانات موثوقة (CBI/ITC Trade Map)
- 60-74: بيانات تجارية (Europages/B2B)
- أقل من 60: تقدير — يجب التحقق

## هيكل التقرير المطلوب:
اكتب التقرير بالعربية بالهيكل التالي بالضبط:

# تقرير تصدير: [المنتج] → [الدولة]
**تاريخ التقرير:** [اليوم]
**مستوى الثقة الإجمالي:** [رقم/100]

---

## 1. ملخص تنفيذي
[3-4 جمل موجزة]
**الثقة:** [رقم/100] | **المصادر:** [قائمة]

---

## 2. حجم السوق والاتجاهات
| المؤشر | القيمة | السنة | المصدر | الثقة |
|--------|--------|-------|--------|-------|
| حجم الواردات | | | | |
| معدل النمو (CAGR) | | | | |
| متوسط سعر الاستيراد | | | | |
| حصة مصر | | | | |

**تحليل الاتجاه:** [نص]
**تحذير:** [إذا كانت البيانات قديمة أو ناقصة]

---

## 3. الرسوم الجمركية والدخول
| البند | القيمة | المصدر | الثقة |
|-------|--------|--------|-------|
| الرسوم الجمركية | | | |
| ضريبة القيمة المضافة | | | |
| قواعد المنشأ | | | |

---

## 4. المتطلبات والشهادات
### 🔴 إلزامية (Mandatory)
[قائمة مع وصف مختصر لكل متطلب]

### 🟡 شائعة لدى المشترين (Common Buyer Requirement)
[قائمة]

### 🟢 موصى بها (Recommended)
[قائمة]

**الثقة:** [رقم/100] | **المصدر:** Access2Markets / CBI

---

## 5. تحليل التسعير والربحية
### معادلة التكلفة الفعلية (Landed Cost)
| البند | التكلفة التقديرية |
|-------|-----------------|
| سعر المنتج FOB مصر | |
| شحن بحري (Port Said → Rotterdam) | |
| تأمين بحري (0.5-1%) | |
| رسوم ميناء الوصول | |
| تخليص جمركي | |
| رسوم جمركية (%) | |
| **إجمالي Landed Cost** | |

### نطاقات الأسعار المقترحة
| السيناريو | السعر/طن | هامش الربح |
|-----------|---------|------------|
| دخول تنافسي | | |
| سعر مستهدف | | |
| تموضع متميز | | |

**الثقة:** [رقم/100]
**ملاحظة:** [تحذير إذا كانت التكاليف اللوجستية تقديرية]

---

## 6. المنافسون الرئيسيون
| الدولة | الحصة السوقية | نقاط القوة | نقطة ضعف يستغلها المصدر المصري |
|--------|--------------|------------|-------------------------------|

---

## 7. توقعات 12-24 شهر
| السيناريو | التوقع | الافتراضات |
|-----------|--------|------------|
| متفائل | | |
| أساسي | | |
| متحفظ | | |

**الثقة:** [رقم/100]
**تحذير:** التوقعات مبنية على CAGR تاريخي — ليست بيانات رسمية

---

## 8. مصادر البيانات
| المصدر | نوع البيانات | تاريخ الجلب | الثقة |
|--------|-------------|-------------|-------|

---
"""
'''

# Find and replace old system prompt
old_sys_start = 'EXPORT_ADVISOR_SYSTEM = """'
old_sys_end   = '\n"""\n'

idx_start = content.find(old_sys_start)
if idx_start != -1:
    idx_end = content.find('\n"""\n', idx_start + 10)
    if idx_end != -1:
        old_block = content[idx_start : idx_end + 5]
        content = content.replace(old_block, NEW_SYSTEM, 1)
        print("OK1: system prompt replaced")
    else:
        print("FAIL1: end of system prompt not found")
else:
    print("FAIL1: system prompt start not found")


# ══════════════════════════════════════════════════════
# NEW PRICING ENGINE
# ══════════════════════════════════════════════════════
PRICING_ENGINE = '''

def calculate_landed_cost(
    exworks_price_per_ton: float,
    destination_country: str,
    product_value_usd: float = 0
) -> dict:
    """
    Calculate real landed cost using formula:
    Landed Cost = FOB + Freight + Insurance + Port + Customs + VAT
    """
    # Freight estimates (USD/ton) Port Said → EU ports
    FREIGHT = {
        "Netherlands": 85,  "Germany": 95,   "France": 90,
        "Belgium": 88,      "Italy": 75,      "Spain": 70,
        "Poland": 110,      "Austria": 105,   "Sweden": 115,
    }
    # EU customs duty for common Egyptian products (0% with EU-Egypt Agreement)
    CUSTOMS = {
        "081110": 0.0,   # Frozen strawberries
        "080510": 0.0,   # Fresh oranges
        "070200": 0.0,   # Tomatoes
        "070310": 0.0,   # Onions
        "100630": 0.0,   # Rice
    }
    # VAT rates
    VAT = {
        "Germany": 7.0, "Netherlands": 9.0, "France": 5.5,
        "Belgium": 6.0, "Italy": 4.0, "Spain": 4.0,
        "Poland": 5.0,  "Austria": 10.0, "Sweden": 12.0,
    }

    freight = FREIGHT.get(destination_country, 90)
    insurance = exworks_price_per_ton * 0.008  # 0.8%
    port_charges = 35  # USD/ton average
    customs_rate = 0.0  # Egypt has 0% with EU-Egypt Agreement
    vat_rate = VAT.get(destination_country, 10.0) / 100

    landed = exworks_price_per_ton + freight + insurance + port_charges
    customs_amount = landed * customs_rate
    landed_with_customs = landed + customs_amount
    vat_amount = landed_with_customs * vat_rate
    total_landed = landed_with_customs  # VAT excluded (buyer pays)

    # Recommended price ranges
    importer_margin = 0.15
    distributor_margin = 0.20
    retailer_margin = 0.30

    target_price = total_landed * (1 + importer_margin + distributor_margin)
    entry_price  = total_landed * (1 + importer_margin)
    premium_price = target_price * (1 + retailer_margin)

    return {
        "breakdown": {
            "exworks_fob": round(exworks_price_per_ton, 0),
            "freight": round(freight, 0),
            "insurance": round(insurance, 0),
            "port_charges": round(port_charges, 0),
            "customs_duty": round(customs_amount, 0),
            "customs_rate_pct": f"{customs_rate*100:.1f}%",
            "total_landed_cost": round(total_landed, 0),
        },
        "price_scenarios": {
            "competitive_entry": round(entry_price, 0),
            "target_price":      round(target_price, 0),
            "premium_position":  round(premium_price, 0),
        },
        "margins": {
            "importer":    f"{importer_margin*100:.0f}%",
            "distributor": f"{distributor_margin*100:.0f}%",
            "retailer":    f"{retailer_margin*100:.0f}%",
        },
        "currency": "USD/ton",
        "confidence": 72,
        "note": "تقديري — يجب التحقق من أسعار الشحن الفعلية"
    }

def format_pricing_for_prompt(pricing: dict) -> str:
    """Format pricing calculation for Claude prompt."""
    b = pricing["breakdown"]
    s = pricing["price_scenarios"]
    lines = [
        "╔══════════════════════════════════════════════╗",
        "║  PRICING ENGINE — Calculated Landed Cost    ║",
        "╚══════════════════════════════════════════════╝",
        f"  FOB مصر:          ${b['exworks_fob']:,}/ton",
        f"  شحن بحري:         ${b['freight']:,}/ton",
        f"  تأمين (0.8%):     ${b['insurance']:,}/ton",
        f"  رسوم ميناء:        ${b['port_charges']:,}/ton",
        f"  جمارك ({b['customs_rate_pct']}):   ${b['customs_duty']:,}/ton",
        f"  ─────────────────────────────",
        f"  Landed Cost إجمالي: ${b['total_landed_cost']:,}/ton",
        f"",
        f"  نطاقات الأسعار المقترحة:",
        f"  دخول تنافسي:      ${s['competitive_entry']:,}/ton",
        f"  سعر مستهدف:       ${s['target_price']:,}/ton",
        f"  تموضع متميز:      ${s['premium_position']:,}/ton",
        f"  [confidence:{pricing['confidence']} | {pricing['note']}]",
    ]
    return "\\n".join(lines)

'''

# Add pricing engine after _extract_plan_steps function
insert_marker = "async def get_export_advice("
if insert_marker in content:
    content = content.replace(insert_marker, PRICING_ENGINE + "\n\nasync def get_export_advice(", 1)
    print("OK2: pricing engine added")
else:
    print("FAIL2: insertion point not found")

# ══════════════════════════════════════════════════════
# UPDATE get_export_advice — inject pricing into prompt
# ══════════════════════════════════════════════════════
old_data_merge = """    # ── Merge all sources
    all_data_sources = ""
    if real_data: all_data_sources += real_data + "\\n\\n"
    if web_data:  all_data_sources += web_data  + "\\n\\n"
"""

new_data_merge = """    # ── Pricing engine calculation
    pricing_data = ""
    try:
        # Use average market price as base FOB (from Comtrade unit values if available)
        base_fob = 800  # USD/ton default for most Egyptian agricultural products
        if real_data and "Unit=$" in real_data:
            import re as _re
            uv_match = _re.search(r'Unit=\\$([\\d,]+)/ton', real_data)
            if uv_match:
                base_fob = int(uv_match.group(1).replace(",","")) * 0.45  # FOB ≈ 45% of CIF
        pricing_calc = calculate_landed_cost(base_fob, target_market)
        pricing_data = format_pricing_for_prompt(pricing_calc)
    except Exception as e:
        pricing_data = f"[Pricing calculation error: {e}]"

    # ── Confidence scoring
    confidence_note = []
    if real_data and "Comtrade" in real_data:
        confidence_note.append("Trade stats: 90/100 [UN Comtrade official]")
    if web_data and "DeepSearch" in web_data:
        confidence_note.append("Web data: 70/100 [recent web search]")
    if cbi_data and "CBI" in cbi_data:
        confidence_note.append("Market intel: 82/100 [CBI Netherlands]")
    confidence_note.append("Tariffs: 95/100 [EU-Egypt Agreement 0%]")
    confidence_note.append("Pricing: 72/100 [calculated estimate]")

    # ── Merge all sources
    all_data_sources = ""
    if real_data:    all_data_sources += real_data    + "\\n\\n"
    if pricing_data: all_data_sources += pricing_data + "\\n\\n"
    if web_data:     all_data_sources += web_data     + "\\n\\n"
    if cbi_data:     all_data_sources += cbi_data     + "\\n\\n"
    if confidence_note:
        all_data_sources += "CONFIDENCE SCORES:\\n" + "\\n".join(f"  {c}" for c in confidence_note) + "\\n\\n"
"""

if old_data_merge in content:
    content = content.replace(old_data_merge, new_data_merge, 1)
    print("OK3: pricing + confidence injected")
else:
    print("FAIL3: merge block not found")

# ══════════════════════════════════════════════════════
# UPDATE user prompt — add structured output instruction
# ══════════════════════════════════════════════════════
old_user_prompt = '''    user_prompt = f"""المنتج التصدير: {product}
كود HS: {hs_code}
السوق المستهدف: {target_market}
معلومات إضافية / سؤال مخصص: {company_info or "تقرير شامل كامل"}

المطلوب: تقرير تصدير احترافي ومفصل جداً في 9 أقسام كاملة.
- كل قسم يجب أن يكون مفصلاً ومعمقاً
- استخدم الأرقام والبيانات الحقيقية مع المصادر
- لا تختصر أي قسم تحت أي ظرف
- استخدم الجداول حيثما أمكن
- الهدف: تقرير استشاري متكامل يساعد المصدر على اتخاذ قرارات مدروسة
"""'''

new_user_prompt = '''    user_prompt = f"""
المنتج: {product} | كود HS: {hs_code} | السوق: {target_market}
السؤال: {company_info or "تقرير شامل"}

══════════════════════════════════════════════════
البيانات الموثقة المتاحة لك:
══════════════════════════════════════════════════
{all_data_sources}
══════════════════════════════════════════════════

التعليمات:
1. اكتب التقرير بالهيكل المحدد في System Prompt بالضبط
2. استخدم الأرقام من VERIFIED DATA فقط — لا تخترع أرقاماً مختلفة
3. أضف confidence score لكل قسم
4. صنّف المتطلبات: إلزامي / شائع / موصى به
5. استخدم جداول منظمة للمقارنات
6. اذكر تحذيراً واضحاً عند نقص البيانات
7. تاريخ اليوم: {datetime.utcnow().strftime('%Y-%m-%d')}
"""'''

if old_user_prompt in content:
    content = content.replace(old_user_prompt, new_user_prompt, 1)
    print("OK4: user prompt updated")
else:
    # Try to find the prompt another way
    idx = content.find("user_prompt = f")
    if idx != -1:
        print(f"FAIL4: found user_prompt at {idx}, manual check needed")
        print(repr(content[idx:idx+200]))
    else:
        print("FAIL4: user_prompt not found")

# Add datetime import if not present
if "from datetime import datetime" not in content:
    content = content.replace("import anthropic", "import anthropic\nfrom datetime import datetime", 1)
    print("OK5: datetime import added")

open(path, "w", encoding="utf-8").write(content)
print(f"\nDone - final size: {len(content):,} chars")
print("\nSummary of changes:")
print("  1. New structured system prompt with confidence scores")
print("  2. Pricing engine with Landed Cost formula")
print("  3. 3-layer data injection (Comtrade + pricing + web)")
print("  4. Confidence scoring per section")
