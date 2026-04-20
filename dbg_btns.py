f = open("WissamXpoHub_V3_Frontend_FIXED.html", encoding="utf-8")
html = f.read()
f.close()

# Show all setDashQ function definitions
import re
matches = list(re.finditer(r'function setDashQ', html))
print(f"setDashQ definitions: {len(matches)}")
for m in matches:
    print(f"  at {m.start()}: {repr(html[m.start():m.start()+100])}")

# Show onclick of first button
idx = html.find("dash-q-btn")
print(f"\nFirst dash-q-btn context:")
print(repr(html[idx-100:idx+200]))

# Check userQuestion element
idx2 = html.find('id="userQuestion"')
print(f"\nuserQuestion at: {idx2}")
