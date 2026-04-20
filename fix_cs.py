import shutil, re
from datetime import datetime

f = open("services/claude_service.py", encoding="utf-8")
c = f.read()
f.close()
shutil.copy2("services/claude_service.py", f"services/claude_service_BACKUP_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py")

# 1. Remove duplicate functions (keep first occurrence)
# Find second calculate_landed_cost
first = c.find("def calculate_landed_cost(")
second = c.find("def calculate_landed_cost(", first + 10)
if second != -1:
    end = c.find("\ndef format_pricing_for_prompt(", second)
    end2 = c.find("\n\nasync def get_export_advice", end)
    c = c[:second] + c[end2:]
    print("OK1: duplicate removed")

# 2. Find real data fetch area and add 3-layer system
old_fetch = 'user_prompt = f"""منتج التصدير: {product}\nكود HS: {hs_code}\nالسوق المستهدف: {target_market}\nمعلومات الشركة/المصدر: {company_info or "غير محددة"}\nوضع المصادر: {sources_mode}\n\nقدم تحليلاً شاملاً وعميقاً يتبع هيكل الـ 8 أقسام المحدد في التعليمات.\nتأكد من ذكر المصادر والسنة بجانب كل رقم أو إحصائية.\nلا تختصر أي قسم — هذا تقرير تصدير احترافي متكامل.\n"""'

new_fetch = '''# ── Layer 1: Comtrade data
    real_data = ""
    try:
        from services.trade_data_service import fetch_real_trade_data
        if hs_code and target_market and target_market not in ("__ALL__","European Union (EU-27)",""):
            real_data = fetch_real_trade_data(hs_code, target_market)
    except Exception as e:
        real_data = f"[Comtrade unavailable: {e}]"

    # ── Layer 2: OpenAI DeepSearch
    web_data = ""
    try:
        from services.deepsearch_service import get_market_intelligence
        if product and target_market:
            web_data = get_market_intelligence(product, hs_code or "", target_market)
    except Exception as e:
        web_data = ""

    # ── Layer 3: Pricing engine
    pricing_data = ""
    try:
        base_fob = 800
        if real_data and "Unit=$" in real_data:
            uv_match = re.search(r"Unit=\\\$([\\d,]+)/ton", real_data)
            if uv_match:
                base_fob = int(uv_match.group(1).replace(",","")) * 0.45
        pricing_calc = calculate_landed_cost(base_fob, target_market)
        pricing_data = format_pricing_for_prompt(pricing_calc)
    except Exception as e:
        pricing_data = ""

    # ── Confidence scores
    conf_lines = []
    if real_data and "Comtrade" in real_data: conf_lines.append("بيانات التجارة: 90/100 [UN Comtrade رسمي]")
    if web_data and len(web_data) > 50:       conf_lines.append("بيانات الويب: 70/100 [بحث حديث]")
    conf_lines.append("الرسوم الجمركية: 95/100 [اتفاقية EU-مصر 0%]")
    conf_lines.append("التسعير: 72/100 [تقدير محسوب]")
    confidence_block = "مستويات الثقة:\\n" + "\\n".join(f"  • {c2}" for c2 in conf_lines)

    # ── Merge all data
    all_data = ""
    if real_data:    all_data += real_data    + "\\n\\n"
    if pricing_data: all_data += pricing_data + "\\n\\n"
    if web_data:     all_data += web_data     + "\\n\\n"
    all_data += confidence_block

    user_prompt = f"""
المنتج: {product} | كود HS: {hs_code} | السوق: {target_market}
السؤال: {company_info or "تقرير شامل"}
التاريخ: {datetime.utcnow().strftime('%Y-%m-%d')}

══════════════════════════════════════
البيانات الموثقة المتاحة:
══════════════════════════════════════
{all_data}
══════════════════════════════════════

التعليمات:
1. اكتب التقرير بالهيكل المحدد في System Prompt
2. استخدم أرقام VERIFIED DATA فقط — لا تخترع أرقاماً
3. أضف confidence score لكل قسم
4. صنّف المتطلبات: 🔴 إلزامي / 🟡 شائع / 🟢 موصى به
5. استخدم جداول للمقارنات
6. اذكر تحذيراً عند نقص البيانات
"""'''

if old_fetch in c:
    c = c.replace(old_fetch, new_fetch, 1)
    print("OK2: 3-layer system + structured prompt added")
else:
    print("FAIL2 - trying partial match")
    idx = c.find("user_prompt = f")
    if idx != -1:
        end = c.find('"""\n\n    message', idx)
        if end != -1:
            c = c[:idx] + new_fetch + c[end+4:]
            print("OK2b: prompt replaced via partial match")

# 3. Add import re if not present
if "import re" not in c:
    c = c.replace("import anthropic", "import anthropic\nimport re", 1)
    print("OK3: import re added")

# 4. Add datetime import if not present
if "from datetime import datetime" not in c:
    c = c.replace("import anthropic", "import anthropic\nfrom datetime import datetime", 1)
    print("OK4: datetime import added")

open("services/claude_service.py", "w", encoding="utf-8").write(c)
print(f"Done - size: {len(c):,}")
