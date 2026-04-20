f = open("WissamXpoHub_V3_Frontend_FIXED.html", encoding="utf-8")
html = f.read()
f.close()

import re
# Find navigation functions
fns = re.findall(r'function \w+\(\)[^{]*\{[^}]*\.html[^}]*\}', html)
for fn in fns[:10]:
    print(repr(fn[:150]))
    print()

# Find Right panel section
idx = html.find("Right panel")
print("Right panel at:", idx)
print(repr(html[idx:idx+500]))
