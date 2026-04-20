import shutil
from datetime import datetime

f = open("WissamXpoHub_V3_Frontend_FIXED.html", encoding="utf-8")
html = f.read()
f.close()

ts = datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2("WissamXpoHub_V3_Frontend_FIXED.html", f"WissamXpoHub_V3_Frontend_FIXED_BACKUP_{ts}.html")

changed = 0

# 1) Remove SETUP + CONNECTION
s = html.find("<!-- SETUP + CONNECTION -->")
e = html.find("</div><!-- end .wrap -->")
if s != -1 and e != -1:
    html = html[:s] + "\n\n  " + html[e:]
    changed += 1
    print("OK1: SETUP+CONNECTION removed")
else:
    print("FAIL1 s=",s,"e=",e)

# 2) Replace heroProduct kpi-strip with Quick Launch
# Find in JS - heroProduct is only in JS now, find in HTML hero section
hero_right = html.find("<!-- Right panel -->")
hero_end = html.find("</section>", hero_right)
right_block = html[hero_right:hero_end]
print("Right panel size:", len(right_block))

# Find btns hero-auth-btns block end to insert after it  
auth_end = html.find("</div>\n\n", html.find("hero-auth-btns"))
if auth_end == -1:
    auth_end = html.find("logoutBtn")
    auth_end = html.find("</div>", auth_end) + 6

print("auth_end:", auth_end, repr(html[auth_end:auth_end+50]))

quick_btns = """\n\n        <div style="margin-top:14px;display:flex;flex-direction:column;gap:10px;">
          <button onclick="window.location.href='ExportIntelligence.html'" style="width:100%;background:#1d4ed8;border:none;border-radius:14px;padding:13px 20px;font-size:14px;font-weight:800;font-family:'Cairo',Arial,sans-serif;cursor:pointer;color:#fff;">
            &#128200; Export Intelligence
          </button>
          <button onclick="window.location.href='PotentialBuyers.html'" style="width:100%;background:#1e40af;border:none;border-radius:14px;padding:13px 20px;font-size:14px;font-weight:800;font-family:'Cairo',Arial,sans-serif;cursor:pointer;color:#fff;">
            &#127970; Potential Buyers
          </button>
          <button onclick="window.location.href='ExportOpportunityScanner.html'" style="width:100%;background:rgba(16,185,129,.15);border:1px solid rgba(16,185,129,.4);border-radius:14px;padding:13px 20px;font-size:14px;font-weight:800;font-family:'Cairo',Arial,sans-serif;cursor:pointer;color:#6ee7b7;">
            &#127757; Export Opportunity Scanner
          </button>
        </div>"""

# Insert after hero-auth-btns closing div
old_btns_div = """        <div class="btns hero-auth-btns">
          <button class="primary" id="loginBtn" onclick="loginUser()">Login</button>
          <button class="ghost"   id="logoutBtn" onclick="logoutUser()">Logout</button>
        </div>"""

if old_btns_div in html:
    html = html.replace(old_btns_div, old_btns_div + quick_btns, 1)
    changed += 1
    print("OK2: Quick Launch buttons added")
else:
    print("FAIL2: auth btns div not found")
    idx = html.find("hero-auth-btns")
    print(repr(html[idx-10:idx+150]))

open("WissamXpoHub_V3_Frontend_FIXED.html", "w", encoding="utf-8").write(html)
print(f"\nDone {changed}/2 - size: {len(html)}")
