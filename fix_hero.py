f = open("WissamXpoHub_V3_Frontend_FIXED.html", encoding="utf-8")
html = f.read()
f.close()
import shutil
from datetime import datetime

changed = 0

# 1) حذف kpi-strip كاملاً
old_kpi = """
        <div class="kpi-strip" style="margin-top:16px;">
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

if old_kpi in html:
    html = html.replace(old_kpi, "", 1)
    changed += 1
    print("Patch 1 OK: kpi-strip removed")
else:
    print("Patch 1: kpi-strip not found - checking...")
    idx = html.find("kpi-strip")
    while idx != -1 and html[idx] == ".":
        idx = html.find("kpi-strip", idx+1)
    # find in HTML body not CSS
    body_idx = html.find("<body>")
    kpi_html = html.find("kpi-strip", body_idx)
    if kpi_html != -1:
        print("Found at:", kpi_html)
        print(repr(html[kpi_html-20:kpi_html+100]))

# 2) إضافة أزرار Potential Buyers + Scanner بعد Login/Logout
old_btns = """        <div class="btns hero-auth-btns">
          <button class="primary" id="loginBtn" onclick="loginUser()">Login</button>
          <button class="ghost"   id="logoutBtn" onclick="logoutUser()">Logout</button>
        </div>"""

new_btns = """        <div class="btns hero-auth-btns">
          <button class="primary" id="loginBtn" onclick="loginUser()">Login</button>
          <button class="ghost"   id="logoutBtn" onclick="logoutUser()">Logout</button>
        </div>

        <div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:10px;">
          <button onclick="window.location.href='PotentialBuyers.html'" style="flex:1;background:#1e40af;border:none;border-radius:12px;padding:10px 16px;font-size:13px;font-weight:800;font-family:'Cairo',Arial,sans-serif;cursor:pointer;color:#fff;box-shadow:0 4px 12px rgba(0,0,0,.2);">&#127970; Potential Buyers</button>
          <button onclick="window.location.href='ExportOpportunityScanner.html?v=v2603161930'" style="flex:1;background:rgba(16,185,129,.18);border:1px solid rgba(16,185,129,.4);border-radius:12px;padding:10px 16px;font-size:13px;font-weight:800;font-family:'Cairo',Arial,sans-serif;cursor:pointer;color:#6ee7b7;box-shadow:0 4px 12px rgba(0,0,0,.2);">&#127757; Export Scanner</button>
        </div>"""

if old_btns in html:
    html = html.replace(old_btns, new_btns, 1)
    changed += 1
    print("Patch 2 OK: nav buttons added below Login/Logout")
elif "hero-auth-btns" in html:
    print("Patch 2: already applied or different structure")
    changed += 1
else:
    print("Patch 2 FAILED")

if changed > 0:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    shutil.copy2("WissamXpoHub_V3_Frontend_FIXED.html", f"WissamXpoHub_V3_Frontend_FIXED_BACKUP_{ts}.html")
    open("WissamXpoHub_V3_Frontend_FIXED.html", "w", encoding="utf-8").write(html)
    print(f"\nDONE {changed}/2 patches - reload with Ctrl+Shift+R")
else:
    print("Nothing saved")
