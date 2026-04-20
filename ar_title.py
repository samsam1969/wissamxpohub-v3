f = open("WissamXpoHub_V3_Frontend_FIXED.html", encoding="utf-8")
html = f.read()
f.close()

old = "Quick Access — Data Sources"
new = "روابط سريعة — مصادر البيانات"

html = html.replace(old, new, 1)
open("WissamXpoHub_V3_Frontend_FIXED.html", "w", encoding="utf-8").write(html)
print("OK")
