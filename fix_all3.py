import shutil, re
from datetime import datetime

f = open("services/claude_service.py", encoding="utf-8")
c = f.read()
f.close()
shutil.copy2("services/claude_service.py", f"services/claude_service_BACKUP_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py")

# ── Fix 1: trademap_data indentation bug (it's inside except block)
old_bug = '''    except Exception as e:
        trademap_data = f"[TradeMap: {e}]"

        real_data = ""'''
new_fix = '''    except Exception as e:
        trademap_data = f"[TradeMap: {e}]"

    real_data = ""'''

if old_bug in c:
    c = c.replace(old_bug, new_fix, 1)
    print("OK1: trademap indentation fixed")
else:
    print("FAIL1")

# ── Fix 2: Add trademap_data to merge + fix FOB defaults
old_merge = '''    # ── Merge all data
    all_data = ""
    if real_data:    all_data += real_data    + "\\n\\n"
    if pricing_data: all_data += pricing_data + "\\n\\n"
    if web_data:     all_data += web_data     + "\\n\\n"
    all_data += confidence_block'''

new_merge = '''    # ── Merge all data (TradeMap first = most recent)
    all_data = ""
    if trademap_data and len(trademap_data) > 100: all_data += trademap_data + "\\n\\n"
    if real_data     and len(real_data) > 100:     all_data += real_data     + "\\n\\n"
    if pricing_data  and len(pricing_data) > 50:   all_data += pricing_data  + "\\n\\n"
    if web_data      and len(web_data) > 50:        all_data += web_data      + "\\n\\n"
    all_data += confidence_block'''

if old_merge in c:
    c = c.replace(old_merge, new_merge, 1)
    print("OK2: trademap_data added to merge")
else:
    print("FAIL2")

# ── Fix 3: FOB defaults per product
old_fob = '''    # ── Layer 3: Pricing engine
    pricing_data = ""
    try:
        base_fob = 800
        if real_data and "Unit=$" in real_data:
            uv_match = re.search(r"Unit=\\\\$([\\d,]+)/ton", real_data)
            if uv_match:
                base_fob = int(uv_match.group(1).replace(",","")) * 0.45
        pricing_calc = calculate_landed_cost(base_fob, target_market)
        pricing_data = format_pricing_for_prompt(pricing_calc)
    except Exception as e:
        pricing_data = ""'''

new_fob = '''    # ── Layer 3: Pricing engine
    pricing_data = ""
    try:
        FOB_DEFAULTS = {
            "081110": 550, "081120": 600, "081190": 580,
            "080510": 350, "080520": 380, "080550": 360,
            "080410": 420, "080440": 600, "080430": 800,
            "070200": 300, "070310": 250, "070320": 300,
            "100630": 400, "160414": 1200, "090111": 2500,
            "060310": 800, "060390": 700,
        }
        hs6 = (hs_code or "")[:6]
        base_fob = FOB_DEFAULTS.get(hs6, 500)
        # Override with real TradeMap unit value if available
        if trademap_data and "Unit=" in trademap_data:
            uv_match = re.search(r"\\$([\\d,]+)/ton", trademap_data)
            if uv_match:
                uv = int(uv_match.group(1).replace(",",""))
                if 100 < uv < 10000:
                    base_fob = int(uv * 0.75)  # CIF→FOB
        # Fallback: use Comtrade unit value
        elif real_data and "Unit=$" in real_data:
            uv_match = re.search(r"Unit=\\$([\\d,]+)/ton", real_data)
            if uv_match:
                uv = int(uv_match.group(1).replace(",",""))
                if 100 < uv < 10000:
                    base_fob = int(uv * 0.80)
        pricing_calc = calculate_landed_cost(base_fob, target_market)
        pricing_data = format_pricing_for_prompt(pricing_calc)
    except Exception as e:
        pricing_data = f"[Pricing error: {e}]"'''

if old_fob in c:
    c = c.replace(old_fob, new_fob, 1)
    print("OK3: FOB defaults fixed per product")
else:
    print("FAIL3")

# ── Fix 4: Intent-based prompt customization
old_prompt = '''    user_prompt = f"""
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

new_prompt = '''    # Build intent-specific focus instructions
    question = company_info or ""
    q_lower = question.lower()
    if any(w in q_lower for w in ["مستورد","موزع","buyer","importer","شركات","عملاء"]):
        focus = """التركيز المطلوب: قائمة المستوردين والموزعين
- ركّز على القسم 6 (قائمة المشترين) واجعله أطول وأكثر تفصيلاً
- اذكر 15-20 شركة مستوردة حقيقية بالاسم والموقع والنشاط
- أضف نصائح التواصل والتفاوض مع كل فئة
- اختصر الأقسام الأخرى"""
    elif any(w in q_lower for w in ["شحن","freight","لوجستي","ميناء","حاوية"]):
        focus = """التركيز المطلوب: الشحن واللوجستيات
- ركّز على تحليل الشحن: المسارات، الموانئ، الحاويات، التكاليف، المدة
- فصّل Landed Cost بالكامل مع كل بند
- اذكر شركات الشحن الموصى بها
- اختصر الأقسام الأخرى"""
    elif any(w in q_lower for w in ["جمارك","رسوم","tariff","متطلبات","شهادة"]):
        focus = """التركيز المطلوب: الجمارك والمتطلبات
- ركّز على القسم 3 و4 (الجمارك والشهادات) بشكل مفصّل جداً
- اذكر كل متطلب مع جهة الإصدار وتكلفة الحصول عليه
- اختصر الأقسام الأخرى"""
    elif any(w in q_lower for w in ["سعر","تسعير","ربح","هامش","pricing"]):
        focus = """التركيز المطلوب: التسعير والربحية
- ركّز على القسم 5 (التسعير) بشكل مفصّل جداً
- أضف جدول حساسية الأسعار لعدة سيناريوهات
- احسب نقطة التعادل ومتى تبدأ الربحية
- اختصر الأقسام الأخرى"""
    else:
        focus = "اكتب تقريراً شاملاً متوازناً في جميع الأقسام"

    user_prompt = f"""
المنتج: {product} | كود HS: {hs_code} | السوق: {target_market}
السؤال: {question or "تقرير شامل"}
التاريخ: {datetime.utcnow().strftime("%Y-%m-%d")}

══════════════════════════════════════
البيانات الموثقة المتاحة:
══════════════════════════════════════
{all_data}
══════════════════════════════════════

{focus}

قواعد الكتابة:
1. استخدم أرقام VERIFIED DATA / TRADE MAP فقط — لا تخترع أرقاماً مختلفة
2. أضف confidence score لكل قسم
3. صنّف المتطلبات: 🔴 إلزامي / 🟡 شائع / 🟢 موصى به
4. استخدم جداول للمقارنات
5. اذكر تحذيراً واضحاً عند نقص البيانات
"""'''

if old_prompt in c:
    c = c.replace(old_prompt, new_prompt, 1)
    print("OK4: intent-based prompt added")
else:
    print("FAIL4 - prompt not found")

open("services/claude_service.py", "w", encoding="utf-8").write(c)
print("Done - size:", len(c))
