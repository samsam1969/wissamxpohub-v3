f = open("WissamXpoHub_V3_Frontend_FIXED.html", encoding="utf-8")
html = f.read()
f.close()

# Find blog references
import re
for m in re.finditer(r'.{0,50}[Bb]log.{0,50}', html):
    print(repr(m.group()))
