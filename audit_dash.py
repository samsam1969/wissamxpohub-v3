f = open("WissamXpoHub_V3_Frontend_FIXED.html", encoding="utf-8")
html = f.read()
f.close()

# تحقق من حجم الملف وما تبقى من sections
body_start = html.find("<body>")
script_start = html.find("<script>")
body_html = html[body_start:script_start]

# ابحث عن الـ sections الموجودة
sections = []
import re
for m in re.finditer(r'<!-- (.+?) -->', body_html):
    sections.append((m.start(), m.group(1)))

for pos, name in sections[:30]:
    print(f"{pos:6d} | {name}")
