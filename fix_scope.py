f = open("services/claude_service.py", encoding="utf-8")
c = f.read()
f.close()

old = "⚠️ تحذير HS CODE: بيانات Trade Map تشمل جميع منتجات الكود HS 6 أرقام."
new = """⚠️ تحذير HS CODE: بيانات Trade Map تشمل جميع منتجات الكود HS 6 أرقام.
   استخدم هذه البيانات مع إيضاح النطاق. مثال:
   "واردات قبرص من HS 080410 (يشمل تمر+أفوكادو+مانجو) = $X مليون"
   ثم قدّر حصة التمر تقريباً بناءً على السياق والمعرفة العامة.
   لا تقل "غير متاح" إذا كانت البيانات موجودة — استخدمها مع التحذير المناسب."""

if old in c:
    c = c.replace(old, new, 1)
    print("OK: Claude instruction updated")
else:
    print("FAIL")

open("services/claude_service.py", "w", encoding="utf-8").write(c)
