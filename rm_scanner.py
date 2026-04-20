import shutil
from datetime import datetime

f = open("WissamXpoHub_V3_Frontend_FIXED.html", encoding="utf-8")
html = f.read()
f.close()
shutil.copy2("WissamXpoHub_V3_Frontend_FIXED.html", f"WissamXpoHub_V3_Frontend_FIXED_BACKUP_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html")

# Remove Export Scanner button from Tools section
old = """          <button type="button" onclick="window.location.href='ExportOpportunityScanner.html'"
            style="width:100%;background:rgba(16,185,129,.15);border:1px solid rgba(16,185,129,.4);border-radius:14px;padding:16px 20px;font-size:15px;font-weight:800;font-family:'Cairo',Arial,sans-serif;cursor:pointer;color:#6ee7b7;text-align:left;display:flex;align-items:center;gap:12px;">
            <span style="font-size:24px;">&#127757;</span>
            <div>
              <div>Export Opportunity Scanner</div>
              <div style="font-size:12px;font-weight:600;color:#6ee7b7;margin-top:2px;opacity:.8;">Discover top 10 export markets</div>
            </div>
          </button>"""

if old in html:
    html = html.replace(old, "", 1)
    print("OK1: Scanner button removed from Tools")
else:
    # Try alternate
    idx = html.find("ExportOpportunityScanner.html")
    while idx != -1:
        ctx = html[idx-300:idx+200]
        if "button" in ctx and "onclick" in ctx:
            print("Found at:", idx)
            print(repr(ctx))
            break
        idx = html.find("ExportOpportunityScanner.html", idx+1)

open("WissamXpoHub_V3_Frontend_FIXED.html", "w", encoding="utf-8").write(html)
print("Done - size:", len(html))
