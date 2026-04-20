f = open("WissamXpoHub_V3_Frontend_FIXED.html", encoding="utf-8")
html = f.read()
f.close()

import re
body = html[html.find("<body>"):html.find("<script>")]
for m in re.finditer(r'<!--(.+?)-->', body):
    print(repr(m.group(1).strip()[:60]))
print("\nSize:", len(html))
print("Has dashboard-stack:", "dashboard-stack" in html)
print("Has runIntelligence:", "runIntelligence" in html)
