f = open("WissamXpoHub_V3_Frontend_FIXED.html", encoding="utf-8")
html = f.read()
f.close()

import re

# Find REQUEST_TIMEOUT_MS
matches = re.findall(r'.{10}REQUEST_TIMEOUT_MS.{40}', html)
for m in matches[:3]:
    print(repr(m))

# Fix it
new_html = re.sub(r'REQUEST_TIMEOUT_MS\s*=\s*\d+', 'REQUEST_TIMEOUT_MS = 600000', html)

if new_html != html:
    open("WissamXpoHub_V3_Frontend_FIXED.html", "w", encoding="utf-8").write(new_html)
    print("OK - REQUEST_TIMEOUT_MS updated to 600000")
else:
    print("Not found as constant - checking...")
    idx = html.find("REQUEST_TIMEOUT_MS")
    print("At:", idx, repr(html[idx-20:idx+60]))
