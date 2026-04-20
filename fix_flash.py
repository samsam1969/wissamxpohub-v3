import shutil
from datetime import datetime

f = open("WissamXpoHub_V3_Frontend_FIXED.html", encoding="utf-8")
html = f.read()
f.close()

shutil.copy2("WissamXpoHub_V3_Frontend_FIXED.html", f"WissamXpoHub_V3_Frontend_FIXED_BACKUP_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html")

# Fix 1: Remove filter from button transitions — main cause of flash
old = "    button:hover   { transform: translateY(-2px); filter: brightness(1.1); }\n    button:active  { transform: scale(.97); filter: brightness(.9); }"
new = "    button:hover   { transform: translateY(-2px); opacity: .92; }\n    button:active  { transform: scale(.98); opacity: .85; }"

if old in html:
    html = html.replace(old, new, 1)
    print("OK1: button filter removed")
else:
    print("FAIL1 - trying partial...")
    old2 = "filter: brightness(1.1);"
    if old2 in html:
        html = html.replace("filter: brightness(1.1);", "opacity: .92;")
        html = html.replace("filter: brightness(.9);",  "opacity: .85;")
        html = html.replace("filter: none;",            "")
        print("OK1b: brightness filters replaced")

# Fix 2: Remove the setTimeout updateConnectionIndicators (causes re-render)
old_st = """  // Initial indicator state
  setTimeout(() => {
    const hasToken = !!localStorage.getItem("wx_access_token");
    const hasEmail = !!localStorage.getItem("wx_user_email");
    updateConnectionIndicators(false, hasToken && hasEmail);
  }, 500);"""

if old_st in html:
    html = html.replace(old_st, "  // Connection indicators handled by checkExistingSession", 1)
    print("OK2: setTimeout flash removed")
else:
    print("FAIL2 - not found")

# Fix 3: Add will-change to prevent repaints
old_btn_css = "    button {\n      border: none;"
new_btn_css = "    button {\n      border: none;\n      will-change: transform;\n      backface-visibility: hidden;"
html = html.replace(old_btn_css, new_btn_css, 1)
print("OK3: will-change added")

open("WissamXpoHub_V3_Frontend_FIXED.html", "w", encoding="utf-8").write(html)
print("\nDone - reload with Ctrl+Shift+R")
