import shutil, re
from datetime import datetime

FILE = r"C:\Users\DELL\Desktop\wissamxpohub-backend\WissamXpoHub_V3_Frontend_FIXED.html"
with open(FILE, encoding="utf-8") as f:
    html = f.read()

changed = 0

# Patch 1: حذف OUTPUT SECTION
START = "    <!-- OUTPUT SECTION -->"
END   = "  </div><!-- end .wrap -->"
si = html.find(START)
ei = html.find(END)
if si != -1 and ei != -1 and si < ei:
    html = html[:si] + "\n  " + html[ei:]
    changed += 1
    print("Patch 1 OK: OUTPUT SECTION removed")
elif "dashboard-stack" not in html:
    print("Patch 1: already removed")
    changed += 1
else:
    print("Patch 1 FAILED")

# Patch 2: تحديث أزرار Action
old2 = 'onclick="runIntelligence()">Run Export Intelligence</button>'
new2 = 'onclick="goToExportIntelligence()">Export Intelligence</button>'
if old2 in html:
    html = html.replace(old2, new2, 1)
    changed += 1
    print("Patch 2 OK: Run button updated")
elif "goToExportIntelligence" in html:
    print("Patch 2: already applied")
    changed += 1
else:
    print("Patch 2 FAILED")

# Patch 3: إضافة زر Potential Buyers بجانب scanner button
old3 = "            🌍 ابحث عن الفرص\n          </button>"
new3 = "            🌍 ابحث عن الفرص\n          </button>\n          <button onclick=\"window.location.href='PotentialBuyers.html'\" style=\"background:#1e40af;border:none;border-radius:14px;padding:13px 20px;font-size:15px;font-weight:800;font-family:'Cairo',Arial,sans-serif;cursor:pointer;color:#fff;box-shadow:0 6px 16px rgba(0,0,0,.22);\">🏢 Potential Buyers</button>"
if old3 in html:
    html = html.replace(old3, new3, 1)
    changed += 1
    print("Patch 3 OK: Potential Buyers button added")
elif "Potential Buyers" in html and "window.location.href='PotentialBuyers.html'" in html:
    print("Patch 3: already applied")
    changed += 1
else:
    print("Patch 3 FAILED")

# Patch 4: Navigation JS
nav_js = """
  function goToExportIntelligence() {
    try { localStorage.setItem('wx_ei_hs', document.getElementById('hs').value || ''); } catch(e) {}
    try { localStorage.setItem('wx_ei_country', document.getElementById('country').value || ''); } catch(e) {}
    window.location.href = 'ExportIntelligence.html';
  }
  function goToPotentialBuyers() {
    try { localStorage.setItem('wx_pb_hs', document.getElementById('hs').value || ''); } catch(e) {}
    try { localStorage.setItem('wx_pb_country', document.getElementById('country').value || ''); } catch(e) {}
    window.location.href = 'PotentialBuyers.html';
  }

"""
if "goToExportIntelligence" not in html:
    html = html.replace("  /* ─── INIT ─── */", nav_js + "  /* ─── INIT ─── */", 1)
    changed += 1
    print("Patch 4 OK: Navigation JS added")
else:
    print("Patch 4: already present")
    changed += 1

if changed > 0:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    shutil.copy2(FILE, FILE.replace(".html", f"_BACKUP_{ts}.html"))
    with open(FILE, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"\nDONE {changed}/4 patches applied")
else:
    print("Nothing saved")
