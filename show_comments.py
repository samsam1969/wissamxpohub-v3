f = open("WissamXpoHub_V3_Frontend_FIXED.html", encoding="utf-8")
html = f.read()
f.close()

import re
body_start = html.find("<body>")
script_start = html.find("<script>")
body_html = html[body_start:script_start]

for m in re.finditer(r'<!--(.+?)-->', body_html):
    print(repr(m.group(1)[:60]))
