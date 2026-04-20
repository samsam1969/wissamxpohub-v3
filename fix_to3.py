import re

for fname in ["WissamXpoHub_V3_Frontend_FIXED.html", "ExportIntelligence.html"]:
    f = open(fname, encoding="utf-8")
    html = f.read()
    f.close()
    
    # Fix fetchWithTimeout - increase to 600 seconds (10 min)
    new_html = re.sub(r'c\.abort\(\),\s*180000', 'c.abort(),600000', html)
    new_html = re.sub(r'c\.abort\(\),\s*TIMEOUT', 'c.abort(),600000', new_html)
    
    # Fix TIMEOUT constant
    new_html = re.sub(r'TIMEOUT\s*=\s*180000', 'TIMEOUT=600000', new_html)
    new_html = re.sub(r'TIMEOUT\s*=\s*480000', 'TIMEOUT=600000', new_html)
    
    # Fix error message
    new_html = new_html.replace("انتهت مهلة الاتصال (180 ثانية)", "انتهت مهلة الاتصال (600 ثانية)")
    new_html = new_html.replace("Request timeout (180s)", "Request timeout (600s)")
    new_html = new_html.replace("Request timeout", "Request timeout (600s)")
    
    if new_html != html:
        open(fname, "w", encoding="utf-8").write(new_html)
        print(f"OK: {fname} timeout updated to 600s")
    else:
        print(f"No change: {fname}")

# Also fix dashboard fetchWithTimeout function
f = open("WissamXpoHub_V3_Frontend_FIXED.html", encoding="utf-8")
html = f.read()
f.close()

idx = html.find("fetchWithTimeout")
print("\nDashboard fetchWithTimeout:")
print(repr(html[idx:idx+200]))
