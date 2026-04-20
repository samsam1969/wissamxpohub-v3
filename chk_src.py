f = open("WissamXpoHub_V3_Frontend_FIXED.html", encoding="utf-8")
html = f.read()
f.close()
import re

# Show all sources button contexts
for m in re.finditer(r'.{30}مصادر البيانات.{30}', html):
    print(repr(m.group()))
    print()
