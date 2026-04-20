f = open("WissamXpoHub_V3_Frontend_FIXED.html", encoding="utf-8")
html = f.read()
f.close()
import re

# Count ALL sources buttons
all = [m.start() for m in re.finditer(r'مصادر البيانات', html)]
print(f"Total 'مصادر البيانات': {len(all)}")
for i in all:
    print(f"  at {i}: {repr(html[i-50:i+30])}")

# Check quick buttons
print("\ndash-q-btn count:", html.count("dash-q-btn"))
print("setDashQ count:", html.count("setDashQ"))

# Check if buttons have onclick
idx = html.find("setDashQ")
print("\nsetDashQ context:", repr(html[idx-100:idx+100]))
