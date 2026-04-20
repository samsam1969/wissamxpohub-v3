import shutil
from datetime import datetime

f = open("services/claude_service.py", encoding="utf-8")
content = f.read()
f.close()
shutil.copy2("services/claude_service.py", f"services/claude_service_BACKUP_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py")

# Add the new verification system prompt
VERIFICATION_SYSTEM = '''VERIFICATION_ADVISOR_SYSTEM = """
You are an export market verification analyst, not a content writer.

CORE RULES — NON-NEGOTIABLE:
1. Do NOT invent numbers, sources, buyers, costs, rankings, or growth rates
2. Lock scope first: product | HS code | geography | year | unit | currency
3. Never mix HS 081110 with broader frozen berries/fruits categories
4. Never mix Netherlands data with EU totals
5. Every number MUST include: (Source | Year | Unit | Scope)
6. If not verified from a named public source → label: [UNVERIFIED]
7. If pricing inputs are incomplete → write: "Pricing model incomplete – not decision-safe"
8. If buyer category fit is not proven → label: [Needs Manual Check]
9. Optimize for ACCURACY, not impressiveness
10. If real data is provided in the prompt, use ONLY those numbers

OUTPUT STRUCTURE (always follow this):

## 1. Scope Lock
- Product: [exact name]
- HS Code: [exact 6-digit]
- Geography: [exact country — NOT "EU" unless stated]
- Period: [year(s)]
- Currency: [USD/EUR — specify]
- Flow: [imports/exports]

## 2. Evidence Table
| Claim | Source | Year | Value | Confidence |
|-------|--------|------|-------|------------|
(List all key numbers with source attribution)

## 3. Verified Findings
(Only findings backed by named sources)

## 4. Weak / Unverified Claims
(Clearly labeled — do not present as fact)

## 5. Decision Risk Flags
⚠️ Flag any claim that could lead to wrong business decisions if wrong

## 6. Pricing Readiness
(Is there enough data for a pricing model? What is missing?)

## 7. Buyer Verification
(For each buyer: name | country | activity fit | source | status)

## 8. Safe-to-Use Conclusions
(Only conclusions supported by verified data)

LANGUAGE: Arabic for analysis text, English for data tables and technical terms.
"""
'''

# Insert after existing constants
insert_after = "MAX_TOKENS_SCANNER = 4000"
if insert_after in content:
    content = content.replace(
        insert_after,
        insert_after + "\n\n" + VERIFICATION_SYSTEM
    )
    print("OK1: verification system prompt added")
else:
    print("FAIL1: insert point not found")

# Now update get_export_advice to use verification prompt when appropriate
old_quick = '''        if depth == "quick":
            return f"""أنت خبير تصدير. أجب بشكل مباشر ومختصر.

{base}
{q_line}

اكتب إجابة مركزة في 3-5 أقسام قصيرة فقط، مرتبطة بالسؤال مباشرة.
استخدم بيانات 2024-2025 فقط. لا تكتب تقريراً شاملاً.
الكلمات: 800-1200 فقط."""'''

new_quick = '''        if depth == "quick":
            return f"""أنت محلل تحقق من بيانات التصدير — ليس كاتب محتوى.

{base}
{q_line}

{real_data if real_data else ""}

قواعد صارمة:
- لا تخترع أي أرقام أو مصادر أو أسماء شركات
- كل رقم يجب أن يحمل: (المصدر | السنة | الوحدة)
- إذا لم تكن البيانات متوفرة → اكتب: [غير موثق — يحتاج تحقق]
- إذا كانت البيانات الحقيقية أعلاه موجودة → استخدمها فقط

اكتب إجابة مختصرة ومحددة (800-1000 كلمة) تجيب على السؤال بدقة.
الهيكل:
## نطاق التحليل (المنتج | HS | الدولة | السنة)
## الحقائق الموثقة
## تحذيرات وبيانات مفقودة
## الخلاصة الآمنة للقرار"""'''

if old_quick in content:
    content = content.replace(old_quick, new_quick, 1)
    print("OK2: quick prompt updated to verification mode")
else:
    print("FAIL2: quick prompt not found")

# Update the function signature to accept real_data
old_sig = "    def make_prompt(part=1):"
new_sig = "    def make_prompt(part=1, real_data=''):"
content = content.replace(old_sig, new_sig, 1)
print("OK3: function signature updated")

# Update all other prompts to include real_data and verification rules
old_pricing = '''        elif intent == "pricing":
            return f"""أنت خبير تسعير وتصدير متخصص.

{base}
{q_line}

اكتب تقريراً احترافياً عن التسعير والربحية يشمل:'''

new_pricing = '''        elif intent == "pricing":
            return f"""أنت محلل تحقق من بيانات التصدير والتسعير.

{base}
{q_line}

{real_data if real_data else ""}

قواعد غير قابلة للتفاوض:
- استخدم فقط الأرقام الواردة في "VERIFIED TRADE DATA" أعلاه إن وجدت
- لا تخترع أسعاراً أو هوامش أو تكاليف
- كل رقم: (المصدر | السنة | الوحدة | النطاق)
- إذا البيانات غير كافية للتسعير → اكتب: "نموذج التسعير غير مكتمل — غير آمن للقرار"

اكتب تقريراً عن التسعير والربحية:

## 1. قفل النطاق
المنتج | HS | الدولة | السنة | العملة

## 2. جدول الأدلة
| البيان | المصدر | السنة | القيمة | مستوى الثقة |

## 3. بيانات السوق الموثقة
(أسعار الاستيراد الحقيقية، حجم السوق الفعلي)

## 4. تحليل التسعير والتكاليف
(بناءً على البيانات الموثقة فقط)

## 5. تحذيرات ومخاطر القرار
⚠️ أي بيانات مفقودة قد تؤثر على التسعير

## 6. الخلاصة الآمنة للقرار'''

if old_pricing in content:
    content = content.replace(old_pricing, new_pricing, 1)
    print("OK4: pricing prompt updated to verification mode")
else:
    print("FAIL4: pricing prompt not found")

# Inject trade_data_service into get_export_advice
old_execute = "    # Execute calls\n    parts = []"
new_execute = """    # Fetch REAL trade data from UN Comtrade
    real_data = ""
    try:
        from services.trade_data_service import fetch_real_trade_data
        real_data = fetch_real_trade_data(hs_code or "", target_market or "")
        logger.info(f"Real trade data fetched: {len(real_data)} chars")
    except Exception as e:
        logger.warning(f"Trade data fetch failed: {e}")
        real_data = ""

    # Execute calls\n    parts = []"""

if old_execute in content:
    content = content.replace(old_execute, new_execute, 1)
    print("OK5: trade data injection added")
else:
    print("FAIL5: execute block not found")

# Pass real_data to make_prompt
old_call = "        prompt = make_prompt(i)"
new_call = "        prompt = make_prompt(i, real_data=real_data)"
content = content.replace(old_call, new_call)
print("OK6: real_data passed to prompts")

# Add logger import if not present
if "import logging" not in content:
    content = "import logging\n" + content
    print("OK7: logging import added")

if "logger = logging.getLogger" not in content:
    content = content.replace(
        "def get_client():",
        "logger = logging.getLogger(__name__)\n\ndef get_client():"
    )
    print("OK8: logger instance added")

open("services/claude_service.py", "w", encoding="utf-8").write(content)
print("\nDone - size:", len(content))
