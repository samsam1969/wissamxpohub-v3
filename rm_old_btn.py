f = open("WissamXpoHub_V3_Frontend_FIXED.html", encoding="utf-8")
html = f.read()
f.close()
import shutil
from datetime import datetime

old = """
          <button onclick="window.location.href='PotentialBuyers.html'" style="flex:1;background:#1e40af;border:none;border-radius:14px;padding:13px 20px;font-size:15px;font-weight:800;font-family:'Cairo',Arial,sans-serif;cursor:pointer;color:#fff;box-shadow:0 6px 16px rgba(0,0,0,.22);">🏢 Potential Buyers</button>"""

if old in html:
    html = html.replace(old, "", 1)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    shutil.copy2("WissamXpoHub_V3_Frontend_FIXED.html", f"WissamXpoHub_V3_Frontend_FIXED_BACKUP_{ts}.html")
    open("WissamXpoHub_V3_Frontend_FIXED.html", "w", encoding="utf-8").write(html)
    print("Done - removed")
else:
    # manual slice removal
    idx = html.find("\U0001f3e2 Potential Buyers</button>")
    if idx != -1:
        start = html.rfind("<button", 0, idx)
        end = html.find("</button>", idx) + len("</button>")
        html = html[:start] + html[end:]
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        shutil.copy2("WissamXpoHub_V3_Frontend_FIXED.html", f"WissamXpoHub_V3_Frontend_FIXED_BACKUP_{ts}.html")
        open("WissamXpoHub_V3_Frontend_FIXED.html", "w", encoding="utf-8").write(html)
        print("Done via slice - removed")
    else:
        print("Not found")
