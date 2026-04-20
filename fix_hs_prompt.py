f = open("services/claude_service.py", encoding="utf-8")
c = f.read()
f.close()

old = "⚠️ استخدم الأرقام من VERIFIED DATA فقط. لا تخترع أرقاماً مختلفة."
new = """⚠️ استخدم الأرقام من VERIFIED DATA فقط. لا تخترع أرقاماً مختلفة.
⚠️ تحذير HS CODE: بيانات Trade Map تشمل جميع منتجات الكود HS 6 أرقام.
   مثال: HS 080410 = تمر + أفوكادو + مانجو + أناناس معاً.
   عند تحليل سوق التمر فقط: اذكر صراحةً أن الأرقام تشمل كل المنتجات تحت هذا الكود.
   لا تنسب الأرقام الكاملة للتمر فقط."""

if old in c:
    c = c.replace(old, new, 1)
    print("OK: HS scope instruction added to prompt")
else:
    print("FAIL")

open("services/claude_service.py", "w", encoding="utf-8").write(c)
print("Done")
