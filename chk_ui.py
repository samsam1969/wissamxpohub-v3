f = open("WissamXpoHub_V3_Frontend_FIXED.html", encoding="utf-8")
html = f.read()
f.close()
import re

# Count sources buttons
src_btns = [m.start() for m in re.finditer(r'مصادر البيانات', html)]
print(f"'مصادر البيانات' found {len(src_btns)} times at:", src_btns[:5])

# Find quick buttons area
idx = html.find("dash-q-btn")
print("\ndash-q-btn at:", idx)
print(repr(html[idx-20:idx+200]))

# Find runIntelligence function
idx2 = html.find("async function runIntelligence")
print("\nrunIntelligence at:", idx2)
