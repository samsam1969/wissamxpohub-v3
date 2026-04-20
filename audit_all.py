import os, re

f = open("WissamXpoHub_V3_Frontend_FIXED.html", encoding="utf-8")
html = f.read()
f.close()

print("=== DASHBOARD SIZE:", len(html))
print("=== KEY CHECKS:")
print("preset buttons removed:", "presetSources" not in html[html.find("<body>"):html.find("<script>")])
print("OUTPUT SECTION removed:", "dashboard-stack" not in html)
print("SETUP+CONNECTION removed:", "<!-- SETUP + CONNECTION -->" not in html)
print("Quick Launch buttons:", "ExportIntelligence.html" in html)
print("Potential Buyers btn:", "PotentialBuyers.html" in html)
print("")

files = ["PotentialBuyers.html", "ExportIntelligence.html", 
         "services/buyers_service.py", "routers/buyers.py"]
for f in files:
    exists = os.path.exists(f)
    size = os.path.getsize(f) if exists else 0
    print(f"{'OK' if exists else 'MISSING'} {f} ({size} bytes)")

print("")
print("main.py buyers_blueprint:", "buyers_blueprint" in open("main.py").read())
