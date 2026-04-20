f = open("WissamXpoHub_V3_Frontend_FIXED.html", encoding="utf-8")
html = f.read()
f.close()

import re
# Find all .textContent assignments that might fail
matches = re.findall(r'qs\("([^"]+)"\)\.textContent\s*=', html)
print("textContent assignments:")
for m in matches:
    print(f"  qs('{m}').textContent")
