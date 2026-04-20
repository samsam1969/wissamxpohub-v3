f = open("WissamXpoHub_V3_Frontend_FIXED.html", encoding="utf-8")
html = f.read()
f.close()

import re
matches = re.findall(r'.{30}180.{30}', html)
for m in matches:
    print(repr(m))
