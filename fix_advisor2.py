import shutil
from datetime import datetime

f = open("services/claude_service.py", encoding="utf-8")
content = f.read()
f.close()
shutil.copy2("services/claude_service.py", f"services/claude_service_BACKUP_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py")

old_fn = '''async def get_export_advice(product, hs_code, target_market, company_info=None, sources_mode="auto"):'''
end_marker = "async def get_buyer_message"
si = content.find(old_fn)
ei = content.find(end_marker)

new_fn = '''async def get_export_advice(product, hs_code, target_market, company_info=None, sources_mode="auto"):
    """Smart advisor - adapts to question type and depth."""
    client = get_client()
    sources_used, source_urls = _extract_sources(product, target_market)
    info = company_info or ""

    # Parse depth and intent from company_info
    depth = "pro"
    intent = "general"
    question = info
    if "Depth:" in info:
        for part in info.split("|"):
            part = part.strip()
            if part.startswith("Depth:"):
                depth = part.replace("Depth:","").strip()
            elif part.startswith("Intent:"):
                intent = part.replace("Intent:","").strip()
            elif part.startswith("Focus:"):
                pass
            else:
                question = part.strip()

    # Max tokens based on depth
    token_map = {"quick": 2000, "pro": 6000, "full": 8192}
    max_tok = token_map.get(depth, 6000)

    # Number of calls based on depth
    calls = {"quick": 1, "pro": 1, "full": 4}.get(depth, 1)

    # Build prompt based on intent + depth
    def make_prompt(part=1):
        base = f"المنتج: {product} | كود HS: {hs_code} | السوق: {target_market} | تاريخ: 2025"
        q_line = f"السؤال: {question}" if question else "اكتب تقريراً شاملاً"

        if depth == "quick":
            return f"""أنت خبير تصدير. أجب بشكل مباشر ومختصر.

{base}
{q_line}

اكتب إجابة مركزة في 3-5 أقسام قصيرة فقط، مرتبطة بالسؤال مباشرة.
استخدم بيانات 2024-2025 فقط. لا تكتب تقريراً شاملاً.
الكلمات: 800-1200 فقط."""

        elif intent == "pricing":
            return f"""أنت خبير تسعير وتصدير متخصص.

{base}
{q_line}

اكتب تقريراً احترافياً عن التسعير والربحية يشمل:
## 1. أسعار السوق الحالية (2024-2025)
- متوسط سعر الاستيراد FOB/CIF في {target_market} [المصدر، 2024-2025]
- نطاق الأسعار حسب الجودة والموسم
- مقارنة أسعار مصر مع المنافسين الرئيسيين

## 2. تحليل هامش الربح
- تكلفة الإنتاج المصري التقديرية
- تكاليف الشحن والتخليص
- هامش الربح المتوقع بالأرقام

## 3. استراتيجية التسعير المقترحة
- سعر الدخول المناسب للسوق
- استراتيجية التسعير التنافسي
- متى ترفع/تخفض السعر

## 4. Incoterms المناسبة
- FOB vs CIF vs DDP — الأنسب لـ {target_market}

## 5. نصائح عملية فورية
اكتب بالعربية. بيانات 2024-2025 فقط. أضف [المصدر، السنة] لكل رقم."""

        elif intent == "shipping":
            return f"""أنت خبير لوجستيات وشحن دولي.

{base}
{q_line}

اكتب تقريراً عن الشحن واللوجستيات يشمل:
## 1. المسارات والموانئ (2025)
## 2. التكاليف التفصيلية الحالية
## 3. أنواع الحاويات المناسبة
## 4. مدة الشحن والجداول الزمنية
## 5. الشركات الموصى بها
## 6. نصائح تقليل التكاليف

بيانات 2024-2025. أرقام حقيقية. [المصدر، السنة]."""

        elif intent == "tariffs":
            return f"""أنت خبير قانوني تجاري متخصص في اشتراطات السوق الأوروبي.

{base}
{q_line}

اكتب تقريراً عن الرسوم الجمركية ومتطلبات الدخول:
## 1. الرسوم الجمركية المطبقة (2024-2025)
## 2. الاتفاقيات التجارية وكيف تستفيد منها
## 3. متطلبات الدخول والشهادات
## 4. إجراءات التخليص الجمركي
## 5. التكاليف الإجمالية للامتثال

بيانات محدثة 2024-2025. [المصدر، السنة]."""

        elif intent == "buyers":
            return f"""أنت خبير B2B متخصص في السوق الأوروبي.

{base}
{q_line}

اكتب تقريراً عن المشترين والموزعين:
## 1. أكبر 10 مستوردين في {target_market} (2024-2025)
جدول: الاسم | النشاط | الموقع | حجم المشتريات | أولوية التواصل
## 2. كيفية التواصل مع كل فئة
## 3. استراتيجية دخول السوق عبر الموزعين
## 4. نصائح التفاوض

بيانات 2024-2025 موثقة."""

        elif intent == "compliance":
            return f"""أنت خبير في اشتراطات السلامة الغذائية الأوروبية.

{base}
{q_line}

اكتب تقريراً عن الشهادات والمتطلبات:
## 1. الشهادات الإلزامية لـ {target_market} (2024-2025)
## 2. متطلبات التغليف والتوسيم
## 3. حدود المبيدات MRL المحدثة
## 4. خطوات الحصول على كل شهادة
## 5. التكاليف والجهات المعتمدة في مصر

محدث لـ 2024-2025."""

        else:
            # general or market_entry - full report
            if part == 1:
                return f"""أنت خبير استشاري للتصدير المصري للأسواق الأوروبية.

{base}
{q_line}

اكتب الجزء الأول من تقرير التصدير الشامل - بيانات 2024-2025:

# تقرير التصدير — {product} إلى {target_market}

## 1. تحليل السوق (2023-2025 مقارنة)
- حجم السوق 2023 vs 2024 vs 2025 [المصدر]
- معدلات النمو المحدثة
- موقع مصر وتطوره

## 2. أفضل 5 دول للتصدير (بيانات 2024-2025)
جدول مقارن محدث مع أحدث الأرقام

## 3. اتجاهات الطلب (2024-2026)
- الاتجاهات الجديدة في 2024-2025
- توقعات 2026 مع أرقام

بيانات 2024-2025 فقط. [المصدر، السنة]."""

            elif part == 2:
                return f"""أنت خبير استشاري للتصدير.

{base}

اكتب الجزء الثاني:

## 4. تحليل المنافسين (2024-2025)
- الحصص السوقية المحدثة
- التغيرات مقارنة 2023

## 5. خطة دخول السوق التنفيذية
- 10 خطوات مع ميزانية 2025

## 6. المزايا التنافسية المصرية (محدثة 2024-2025)

بيانات 2024-2025."""

            elif part == 3:
                return f"""أنت خبير استشاري للتصدير.

{base}

اكتب الجزء الثالث:

## 7. التحديات والحلول (2025)
## 8. التوقعات المستقبلية (2026-2027)
- السيناريوهات الثلاثة مع أرقام

## 9. الخلاصة والتوصيات الفورية
## المصادر (2024-2025)"""

            else:
                return None

    # Execute calls
    parts = []
    for i in range(1, calls + 1):
        prompt = make_prompt(i)
        if not prompt:
            break
        try:
            msg = client.messages.create(
                model=MODEL_HEAVY,
                max_tokens=max_tok,
                messages=[{"role": "user", "content": prompt}]
            )
            parts.append(msg.content[0].text)
        except Exception as e:
            parts.append(f"\\n[خطأ: {str(e)}]\\n")

    full_report = "\\n\\n---\\n\\n".join(parts)

    return {
        "advisor": full_report,
        "plan": _extract_plan_steps(full_report),
        "sourcesUsed": sources_used,
        "sourceUrls": source_urls,
        "tokensUsed": 0
    }


'''

if si != -1 and ei != -1:
    content = content[:si] + new_fn + content[ei:]
    open("services/claude_service.py", "w", encoding="utf-8").write(content)
    print("OK - smart advisor with depth/intent, size:", len(content))
else:
    print("FAIL si:", si, "ei:", ei)
