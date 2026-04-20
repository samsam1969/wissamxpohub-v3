f = open("WissamXpoHub_V3_Frontend_FIXED.html", encoding="utf-8")
html = f.read()
f.close()

import re
body = html[html.find("<body>"):html.find("<script>")]
for m in re.finditer(r'<!--(.+?)-->', body):
    print(repr(m.group(1).strip()[:50]))
print("\nSize:", len(html))
print("Has Export Advisor output:", "aiBox" in html)
print("Has dashboard-stack:", "dashboard-stack" in html)
print("Has Quick Launch:", "ExportIntelligence.html" in body)
