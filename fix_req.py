f = open("WissamXpoHub_V3_Frontend_FIXED.html", encoding="utf-8")
html = f.read()
f.close()
import shutil
from datetime import datetime
shutil.copy2("WissamXpoHub_V3_Frontend_FIXED.html", f"WissamXpoHub_V3_Frontend_FIXED_BACKUP_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html")

old = """  function requireSavedSettings(targetBoxId = "aiBox") {
    const s = getSettings();
    if (!s.backendUrl) {
      qs(targetBoxId).textContent = "خطأ: Backend URL غير محفوظ — احفظ الإعدادات أولًا.";
      return null;
    }
    if (!s.accessToken) {
      qs(targetBoxId).textContent = "خطأ: لا يوجد access token — سجّل الدخول أولًا ثم احفظ الإعدادات.";
      return null;
    }
    return s;
  }"""

new = """  function requireSavedSettings(targetBoxId = "aiBox") {
    const s = getSettings();
    const box = qs(targetBoxId);
    if (!s.backendUrl) {
      if(box) box.textContent = "خطأ: Backend URL غير محفوظ — احفظ الإعدادات أولًا.";
      return null;
    }
    if (!s.accessToken) {
      if(box) box.textContent = "خطأ: لا يوجد access token — سجّل الدخول أولًا ثم احفظ الإعدادات.";
      return null;
    }
    return s;
  }"""

if old in html:
    html = html.replace(old, new, 1)
    print("OK1: requireSavedSettings fixed")
else:
    print("FAIL1")

# Fix buildPayload - null-safe
old2 = """      product:      qs("statProduct").textContent,"""
new2 = """      product:      qs("statProduct")?.textContent || qs("productNameBox")?.textContent?.replace("Product: ","") || "","""
if old2 in html:
    html = html.replace(old2, new2, 1)
    print("OK2: buildPayload fixed")
else:
    print("FAIL2")

open("WissamXpoHub_V3_Frontend_FIXED.html", "w", encoding="utf-8").write(html)
print("Done")
