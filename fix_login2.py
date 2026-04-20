f = open("WissamXpoHub_V3_Frontend_FIXED.html", encoding="utf-8")
html = f.read()
f.close()

# Fix saveSettings to not crash on missing elements
old = """  function saveSettings() {
    localStorage.setItem("wx_backend_url",   qs("backendUrl").value.trim().replace(/\\/$/, ""));
    localStorage.setItem("wx_access_token",  qs("accessToken").value.trim());
    loadSettings();
  }"""

new = """  function saveSettings() {
    const bu = qs("backendUrl");
    const at = qs("accessToken");
    if (bu) localStorage.setItem("wx_backend_url", bu.value.trim().replace(/\\/$/, ""));
    if (at) localStorage.setItem("wx_access_token", at.value.trim());
    if (typeof loadSettings === "function") loadSettings();
  }"""

if old in html:
    html = html.replace(old, new, 1)
    print("OK: saveSettings fixed")
else:
    print("Not found - trying alt...")
    idx = html.find("saveSettings")
    print(repr(html[idx:idx+200]))

# Fix loadSettings too
old2 = """  function loadSettings() {
    const s = getSettings();
    qs("backendUrl").value   = s.backendUrl;
    qs("accessToken").value  = s.accessToken;
    qs("connectionStatus").innerHTML = s.accessToken
      ? '<span class="status-ok">✓ الإعدادات محفوظة</span>'
      : '<span class="status-warn">⚠ لم يتم حفظ التوكن بعد — سجّل الدخول أولًا</span>';
  }"""

new2 = """  function loadSettings() {
    const s = getSettings();
    const bu = qs("backendUrl");
    const at = qs("accessToken");
    const cs = qs("connectionStatus");
    if (bu) bu.value = s.backendUrl;
    if (at) at.value = s.accessToken;
    if (cs) cs.innerHTML = s.accessToken
      ? '<span class="status-ok">✓ الإعدادات محفوظة</span>'
      : '<span class="status-warn">⚠ لم يتم حفظ التوكن بعد — سجّل الدخول أولًا</span>';
  }"""

if old2 in html:
    html = html.replace(old2, new2, 1)
    print("OK: loadSettings fixed")
else:
    print("loadSettings alt not found")

open("WissamXpoHub_V3_Frontend_FIXED.html", "w", encoding="utf-8").write(html)
print("Done")
