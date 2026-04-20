import shutil, re
from datetime import datetime

f = open("WissamXpoHub_V3_Frontend_FIXED.html", encoding="utf-8")
html = f.read()
f.close()

# Backup
ts = datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2("WissamXpoHub_V3_Frontend_FIXED.html", f"WissamXpoHub_V3_Frontend_FIXED_BACKUP_{ts}.html")

removed = []

# 1) Remove AI RESEARCH SETTINGS section
s1 = html.find("    <!-- AI RESEARCH SETTINGS -->")
e1 = html.find("    <!-- STATS BAR -->")
if s1 != -1 and e1 != -1:
    html = html[:s1] + "\n" + html[e1:]
    removed.append("AI RESEARCH SETTINGS")

# 2) Remove STATS BAR section
s2 = html.find("    <!-- STATS BAR -->")
e2 = html.find("    <!-- MARKET INTEL + FIND BUYERS -->")
if s2 != -1 and e2 != -1:
    html = html[:s2] + "\n" + html[e2:]
    removed.append("STATS BAR")

# 3) Remove SOURCE REFERENCE SYSTEM
s3 = html.find("    <!-- MARKET INTEL + FIND BUYERS -->")
e3 = html.find("    <!-- OUTPUT SECTION -->")
if e3 == -1:
    e3 = html.find("  </div><!-- end .wrap -->")
if s3 != -1 and e3 != -1:
    html = html[:s3] + "\n" + html[e3:]
    removed.append("SOURCE REFERENCE SYSTEM")

# 4) Remove SETUP + CONNECTION (Product Setup + Connection card)
s4 = html.find("    <!-- SETUP + CONNECTION -->")
e4 = html.find("    <!-- AI RESEARCH SETTINGS -->")
if e4 == -1:
    e4 = html.find("    <!-- STATS BAR -->")
if s4 != -1 and e4 != -1:
    html = html[:s4] + "\n" + html[e4:]
    removed.append("SETUP + CONNECTION")

print("Removed sections:", removed)

# 5) Update Hero Right Panel — add quick launch card
old_kpi_strip = """        <div class="kpi-strip" style="margin-top:16px;">
          <div class="kpi-mini">
            <div class="label">Product</div>
            <div class="value" id="heroProduct">Frozen strawberries</div>
          </div>
          <div class="kpi-mini">
            <div class="label">Market</div>
            <div class="value" id="heroMarket">Germany</div>
          </div>
          <div class="kpi-mini">
            <div class="label">HS Code</div>
            <div class="value" id="heroHs">081110</div>
          </div>
        </div>"""

new_quick_launch = """
        <!-- Quick Launch -->
        <div style="margin-top:16px;display:flex;flex-direction:column;gap:10px;">
          <button onclick="window.location.href='ExportIntelligence.html'"
            style="width:100%;background:var(--btn);border:none;border-radius:14px;padding:14px 20px;font-size:15px;font-weight:800;font-family:'Cairo',Arial,sans-serif;cursor:pointer;color:#fff;box-shadow:0 6px 16px rgba(0,0,0,.22);display:flex;align-items:center;justify-content:center;gap:10px;transition:transform .13s,filter .13s;">
            &#128200; Export Intelligence
          </button>
          <button onclick="window.location.href='PotentialBuyers.html'"
            style="width:100%;background:#1e40af;border:none;border-radius:14px;padding:14px 20px;font-size:15px;font-weight:800;font-family:'Cairo',Arial,sans-serif;cursor:pointer;color:#fff;box-shadow:0 6px 16px rgba(0,0,0,.22);display:flex;align-items:center;justify-content:center;gap:10px;transition:transform .13s,filter .13s;">
            &#127970; Potential Buyers
          </button>
          <button onclick="window.location.href='ExportOpportunityScanner.html'"
            style="width:100%;background:rgba(16,185,129,.18);border:1px solid rgba(16,185,129,.4);border-radius:14px;padding:14px 20px;font-size:15px;font-weight:800;font-family:'Cairo',Arial,sans-serif;cursor:pointer;color:#6ee7b7;box-shadow:0 6px 16px rgba(0,0,0,.22);display:flex;align-items:center;justify-content:center;gap:10px;transition:transform .13s,filter .13s;">
            &#127757; Export Opportunity Scanner
          </button>
        </div>"""

if old_kpi_strip in html:
    html = html.replace(old_kpi_strip, new_quick_launch, 1)
    removed.append("kpi-strip → Quick Launch buttons")
else:
    print("kpi-strip not found - checking...")
    idx = html.find("heroProduct")
    if idx > 0:
        print(repr(html[idx-50:idx+50]))

open("WissamXpoHub_V3_Frontend_FIXED.html", "w", encoding="utf-8") .write(html)
print("\nDone - Dashboard cleaned")
print("Final size:", len(html), "chars")
