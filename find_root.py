f = open("WissamXpoHub_V3_Frontend_FIXED.html", encoding="utf-8")
html = f.read()
f.close()

import re

# Check for form tags
forms = [m.start() for m in re.finditer(r'<form', html)]
print("Forms found:", len(forms))
for pos in forms:
    print(repr(html[pos:pos+100]))

# Check buttons without type="button"
buttons = re.findall(r'<button(?![^>]*type=)[^>]*>', html)
print(f"\nButtons WITHOUT type attribute: {len(buttons)}")
for b in buttons[:5]:
    print(repr(b[:80]))
