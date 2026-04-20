import sys
sys.path.insert(0, '.')
from dotenv import load_dotenv
load_dotenv()
from services.knowledge_service import add_knowledge

# اسعار شحن حقيقية
add_knowledge(
    category="shipping",
    title="أسعار شحن بورسعيد - شمال أوروبا 2025",
    content="""
- حاوية 20 قدم جافة: ,800-2,200 (بورسعيد → روتردام)
- حاوية 40 قدم جافة: ,500-3,200 (بورسعيد → روتردام)
- حاوية Reefer 40 قدم: ,500-4,500 (بورسعيد → روتردام)
- Feeder روتردام → هلسنكي: +-600 إضافية
- وقت العبور: 18-25 يوم بورسعيد → هلسنكي
- شركات موصى بها: Maersk, MSC, CMA CGM, Hapag-Lloyd
""",
    source="Freightos + Hapag-Lloyd Q1 2025",
    hs_code=None, market=None,
    priority=9
)

# اسعار FOB تمور
add_knowledge(
    category="pricing",
    title="أسعار FOB التمور المصرية 2025",
    content="""
- تمر مجهول Premium: ,800-3,500/طن FOB بورسعيد
- تمر مجهول Standard: ,800-2,400/طن FOB
- تمر زغلول طازج: -1,200/طن FOB (موسمي)
- تمر سيوي مجفف: ,200-1,800/طن FOB
- تمر بلح عام: -900/طن FOB
- موسم الذروة: أغسطس-أكتوبر (أسعار أعلى 15-20%)
""",
    source="بيانات مصدرين مصريين + USDA 2025",
    hs_code="080410", market=None,
    priority=10
)

# متطلبات EU 2025
add_knowledge(
    category="regulations",
    title="تحديثات لوائح EU للتمور 2024-2025",
    content="""
- MRL جديد للـ Chlorpyrifos: 0.01 mg/kg (أكثر صرامة من 2023)
- إلزامية EUDR (لوائح إزالة الغابات): تطبق من 2025
- تعديل Regulation 2023/2006: تغليف أكثر استدامة
- فحوصات مشددة على التمور القادمة من مصر وتونس منذ مارس 2024
- شهادة GlobalG.A.P أصبحت شبه إلزامية لسلاسل التجزئة الكبرى
""",
    source="EUR-Lex + EU Commission 2024",
    hs_code="080410", market="EU",
    priority=9
)

print("✅ Sample knowledge added successfully")
