f = open("WissamXpoHub_V3_Frontend_FIXED.html", encoding="utf-8")
html = f.read()
f.close()
import shutil
from datetime import datetime

# حذف زر Potential Buyers من المكان القديم فقط
old = """          <button onclick="window.location.href='PotentialBuyers.html'" style="flex:1;background:#1e40af;border:none;border-radius:14px;padding:13px 20px;font-size:15px;font-weight:800;font-family:'Cairo',Arial,sans-serif;cursor:pointer;color:#fff;box-shadow:0 6px 16px rgba(0,0,0,.22);">🏢 Potential Buyers</button>"""

if old in html:
    html = html.replace(old, "", 1)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    shutil.copy2("WissamXpoHub_V3_Frontend_FIXED.html", f"WissamXpoHub_V3_Frontend_FIXED_BACKUP_{ts}.html")
    open("WissamXpoHub_V3_Frontend_FIXED.html", "w", encoding="utf-8").write(html)
    print("Done - Potential Buyers button removed from old location")
else:
    # Try to find it
    idx = html.find("Potential Buyers")
    while idx != -1:
        print("Found at:", idx, repr(html[idx-100:idx+50]))
        idx = html.find("Potential Buyers", idx+1)
