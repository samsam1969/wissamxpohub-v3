import shutil, re
from datetime import datetime

f = open("WissamXpoHub_V3_Frontend_FIXED.html", encoding="utf-8")
html = f.read()
f.close()
shutil.copy2("WissamXpoHub_V3_Frontend_FIXED.html", f"WissamXpoHub_V3_Frontend_FIXED_BACKUP_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html")

# 1. Add navigation buttons after login/logout buttons
old_btns = """        <div class="btns hero-auth-btns">
          <button type="button" class="primary" id="loginBtn" onclick="loginUser()">Login</button>
          <button type="button" class="ghost"   id="logoutBtn" onclick="logoutUser()">Logout</button>
        </div>"""

new_btns = """        <div class="btns hero-auth-btns">
          <button type="button" class="primary" id="loginBtn" onclick="loginUser()">Login</button>
          <button type="button" class="ghost"   id="logoutBtn" onclick="logoutUser()">Logout</button>
        </div>

        <!-- Navigation Buttons -->
        <div style="display:flex;flex-direction:column;gap:8px;margin-top:14px;">
          <button type="button" onclick="window.location.href='ExportIntelligence.html'"
            style="width:100%;padding:11px;background:linear-gradient(135deg,#1d4ed8,#6366f1);border:none;border-radius:10px;color:#fff;font-size:13px;font-weight:800;font-family:'Cairo',Arial,sans-serif;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:8px;">
            📊 Export Intelligence
          </button>
          <button type="button" onclick="window.location.href='Blog.html'"
            style="width:100%;padding:11px;background:rgba(16,185,129,.15);border:1px solid rgba(16,185,129,.3);border-radius:10px;color:#6ee7b7;font-size:13px;font-weight:800;font-family:'Cairo',Arial,sans-serif;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:8px;">
            📝 المدونة والأخبار
          </button>
        </div>"""

if old_btns in html:
    html = html.replace(old_btns, new_btns, 1)
    print("OK1: navigation buttons added")
else:
    print("FAIL1: buttons not found")

# 2. Remove PotentialBuyers function
old_pb_fn = """  function goToBuyers() {
    const hs      = qs("hs")?.value?.trim() || "";
    const country = qs("country")?.value || "";
    if(hs) localStorage.setItem("wx_pb_hs", hs);
    if(country && country !== "__ALL__") localStorage.setItem("wx_pb_country", country);
    window.location.href = "PotentialBuyers.html";
  }"""

if old_pb_fn in html:
    html = html.replace(old_pb_fn, "", 1)
    print("OK2: goToBuyers function removed")
else:
    # Try partial match
    idx = html.find("PotentialBuyers.html")
    if idx != -1:
        start = html.rfind("function", 0, idx)
        end = html.find("}", idx) + 1
        old_block = html[start:end]
        html = html.replace(old_block, "", 1)
        print("OK2b: goToBuyers removed (partial match)")
    else:
        print("SKIP2: PotentialBuyers not found")

# 3. Remove any Potential Buyers button in the UI
patterns_to_remove = [
    # Button calling goToBuyers
    r'<button[^>]*onclick="goToBuyers\(\)"[^>]*>.*?</button>',
    # Any div/button mentioning Potential Buyers
    r'<button[^>]*>[^<]*[Pp]otential\s*[Bb]uyers[^<]*</button>',
    r'<button[^>]*>[^<]*المشترين المحتملين[^<]*</button>',
]
import re
for pat in patterns_to_remove:
    matches = re.findall(pat, html, re.DOTALL)
    if matches:
        for m in matches:
            html = html.replace(m, "", 1)
            print(f"OK3: removed button: {repr(m[:60])}")

# 4. Replace Potential Buyers text references with Export Intelligence
old_ref = 'راجع قسم Potential Buyers لعرض قائمة المشترين المحتملين'
new_ref = 'يمكن إضافة المشترين من خلال Export Intelligence'
if old_ref in html:
    html = html.replace(old_ref, new_ref, 1)
    print("OK4: text reference updated")

open("WissamXpoHub_V3_Frontend_FIXED.html", "w", encoding="utf-8").write(html)
print("Done - size:", len(html))
