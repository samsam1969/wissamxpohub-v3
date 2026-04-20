import os, re

for fname in ["WissamXpoHub_V3_Frontend_FIXED.html", "ExportIntelligence.html", "PotentialBuyers.html", "auth_guard.js"]:
    if not os.path.exists(fname): continue
    content = open(fname, encoding="utf-8").read()
    matches = re.findall(r'.{20}(?:timeout|TIMEOUT).{20}', content, re.IGNORECASE)
    if matches:
        print(f"\n=== {fname} ===")
        for m in matches[:5]:
            print(repr(m))
