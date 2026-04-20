f = open("WissamXpoHub_V3_Frontend_FIXED.html", encoding="utf-8")
html = f.read()
f.close()

import re
# Find all buttons with onclick or href
btns = re.findall(r'<button[^>]*onclick="[^"]*\.html[^"]*"[^>]*>.*?</button>', html, re.DOTALL)
for b in btns[:10]:
    print(repr(b[:120]))
    print()

# Also find links to .html
links = re.findall(r'href=["\']([^"\']*\.html)["\']', html)
print("HTML links:", set(links))
