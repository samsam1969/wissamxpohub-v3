import shutil
from datetime import datetime

f = open("WissamXpoHub_V3_Frontend_FIXED.html", encoding="utf-8")
html = f.read()
f.close()

ts = datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2("WissamXpoHub_V3_Frontend_FIXED.html", f"WissamXpoHub_V3_Frontend_FIXED_BACKUP_{ts}.html")

changed = 0

# 1) Remove SETUP + CONNECTION section
s = html.find("    <!-- SETUP + CONNECTION -->")
e = html.find("    <!-- end .wrap -->")
if s != -1 and e != -1:
    html = html[:s] + "\n" + html[e:]
    changed += 1
    print("OK1: SETUP+CONNECTION removed")
else:
    print("FAIL1: s=", s, "e=", e)

# 2) Replace kpi-strip with Quick Launch buttons
idx = html.find("heroProduct")
if idx > 0:
    print("heroProduct context:", repr(html[idx-100:idx+50]))

# Find the div containing heroProduct, heroMarket, heroHs
start = html.find('<div class="kpi-strip"')
if start != -1:
    end = html.find("</div>", start)
    # Find closing of parent div (3 nested divs)
    pos = start
    depth = 0
    while pos < len(html):
        if html[pos:pos+4] == "<div":
            depth += 1
        elif html[pos:pos+6] == "</div>":
            depth -= 1
            if depth == 0:
                end = pos + 6
                break
        pos += 1
    
    new_btns = """<div style="margin-top:16px;display:flex;flex-direction:column;gap:10px;">
          <button onclick="window.location.href='ExportIntelligence.html'" style="width:100%;background:#1d4ed8;border:none;border-radius:14px;padding:14px 20px;font-size:15px;font-weight:800;font-family:'Cairo',Arial,sans-serif;cursor:pointer;color:#fff;box-shadow:0 6px 16px rgba(0,0,0,.22);">
            Export Intelligence
          </button>
          <button onclick="window.location.href='PotentialBuyers.html'" style="width:100%;background:#1e40af;border:none;border-radius:14px;padding:14px 20px;font-size:15px;font-weight:800;font-family:'Cairo',Arial,sans-serif;cursor:pointer;color:#fff;box-shadow:0 6px 16px rgba(0,0,0,.22);">
            Potential Buyers
          </button>
          <button onclick="window.location.href='ExportOpportunityScanner.html'" style="width:100%;background:rgba(16,185,129,.18);border:1px solid rgba(16,185,129,.4);border-radius:14px;padding:14px 20px;font-size:15px;font-weight:800;font-family:'Cairo',Arial,sans-serif;cursor:pointer;color:#6ee7b7;box-shadow:0 6px 16px rgba(0,0,0,.22);">
            Export Opportunity Scanner
          </button>
        </div>"""
    
    html = html[:start] + new_btns + html[end:]
    changed += 1
    print("OK2: Quick Launch buttons added")
else:
    print("FAIL2: kpi-strip not found")

open("WissamXpoHub_V3_Frontend_FIXED.html", "w", encoding="utf-8").write(html)
print(f"\nDone - {changed}/2 - size: {len(html)}")
