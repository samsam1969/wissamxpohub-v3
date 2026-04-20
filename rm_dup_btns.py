f = open("WissamXpoHub_V3_Frontend_FIXED.html", encoding="utf-8")
html = f.read()
f.close()
import shutil
from datetime import datetime
shutil.copy2("WissamXpoHub_V3_Frontend_FIXED.html", f"WissamXpoHub_V3_Frontend_FIXED_BACKUP_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html")

# Find and remove the duplicate buttons div
old = """
        <div style="margin-top:14px;display:flex;flex-direction:column;gap:10px;">
          <button type="button" onclick="window.location.href='ExportIntelligence.html'" style="width:100%;background:#1d4ed8;border:none;border-radius:14px;padding:13px 20px;font-size:14px;font-weight:800;font-family:'Cairo',Arial,sans-serif;cursor:pointer;color:#fff;">
            &#128200; Export Intelligence
          </button>
          <button type="button" onclick="window.location.href='PotentialBuyers.html'" style="width:100%;background:#1e40af;border:none;border-radius:14px;padding:13px 20px;font-size:14px;font-weight:800;font-family:'Cairo',Arial,sans-serif;cursor:pointer;color:#fff;">
            &#127970; Potential Buyers
          </button>
          <button type="button" onclick="window.location.href='ExportOpportunityScanner.html'" style="width:100%;background:rgba(16,185,129,.15);border:1px solid rgba(16,185,129,.4);border-radius:14px;padding:13px 20px;font-size:14px;font-weight:800;font-family:'Cairo',Arial,sans-serif;cursor:pointer;color:#6ee7b7;">
            &#127757; Export Opportunity Scanner
          </button>
        </div>"""

if old in html:
    html = html.replace(old, "", 1)
    open("WissamXpoHub_V3_Frontend_FIXED.html", "w", encoding="utf-8").write(html)
    print("OK - duplicate buttons removed")
else:
    # Find by content
    idx = html.find("Export Scanner")
    if idx == -1:
        idx = html.find("Export Opportunity Scanner")
    print("Found at:", idx)
    print(repr(html[idx-300:idx+100]))
