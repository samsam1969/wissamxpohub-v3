import shutil
from datetime import datetime

f = open("WissamXpoHub_V3_Frontend_FIXED.html", encoding="utf-8")
html = f.read()
f.close()
shutil.copy2("WissamXpoHub_V3_Frontend_FIXED.html", f"WissamXpoHub_V3_Frontend_FIXED_BACKUP_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html")

old = """          <button type="button" onclick="window.location.href='ExportIntelligence.html'"
            style="width:100%;padding:11px;background:linear-gradient(135deg,#1d4ed8,#6366f1);border:none;border-radius:10px;color:#fff;font-size:13px;font-weight:800;font-family:'Cairo',Arial,sans-serif;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:8px;">
            📊 Export Intelligence
          </button>"""

if old in html:
    html = html.replace(old, "", 1)
    print("OK: Export Intelligence button removed")
else:
    print("Not found")

open("WissamXpoHub_V3_Frontend_FIXED.html", "w", encoding="utf-8").write(html)
print("Done")
