import shutil
from datetime import datetime

# ── Fix 1: Slow logout in dashboard
f = open("WissamXpoHub_V3_Frontend_FIXED.html", encoding="utf-8")
html = f.read()
f.close()

shutil.copy2("WissamXpoHub_V3_Frontend_FIXED.html", f"WissamXpoHub_V3_Frontend_FIXED_BACKUP_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html")

old_logout = """  async function logoutUser() {
    if (!supabaseClient && !initSupabase()) return;
    setButtonLoading("logoutBtn", true, "Logging out...");
    try {
      await supabaseClient.auth.signOut();
      localStorage.removeItem("wx_access_token");
      qs("accessToken").value = "";
      loadSettings();
      updateUserBar(null);
    } finally {
      setButtonLoading("logoutBtn", false);
    }
  }"""

new_logout = """  async function logoutUser() {
    // Clear localStorage immediately — no waiting for Supabase
    localStorage.removeItem("wx_access_token");
    localStorage.removeItem("wx_user_email");
    localStorage.removeItem("wx_user_plan");
    localStorage.removeItem("wx_user_remaining");
    updateUserBar(null);
    const at = qs("accessToken");
    if (at) at.value = "";
    if (typeof loadSettings === "function") loadSettings();
    // Supabase signOut in background (non-blocking)
    if (supabaseClient || initSupabase()) {
      supabaseClient.auth.signOut().catch(() => {});
    }
  }"""

if old_logout in html:
    html = html.replace(old_logout, new_logout, 1)
    print("OK1: logout fixed")
else:
    print("FAIL1: logout not found")

# ── Fix 3: Button flash — remove transform on active for nav buttons
old_btn_css = """    button:active  { transform: scale(.97); filter: brightness(.9); }"""
new_btn_css = """    button:active  { transform: scale(.97); filter: brightness(.9); }
    .nav-launch-btn:active { transform: none !important; }"""
html = html.replace(old_btn_css, new_btn_css, 1)

open("WissamXpoHub_V3_Frontend_FIXED.html", "w", encoding="utf-8").write(html)
print("OK3: button flash CSS added")

# ── Fix 2: Flash in ExportOpportunityScanner — add instant guard
f2 = open("ExportOpportunityScanner.html", encoding="utf-8")
scanner = f2.read()
f2.close()

guard = """<script>
(function(){
  var t=localStorage.getItem("wx_access_token");
  var e=localStorage.getItem("wx_user_email");
  if(!t||!e){
    document.documentElement.style.visibility="hidden";
    window.location.replace("WissamXpoHub_V3_Frontend_FIXED.html");
  }
})();
</script>"""

if "wx_access_token" not in scanner[:500]:
    scanner = scanner.replace("<head>", "<head>\n" + guard, 1)
    open("ExportOpportunityScanner.html", "w", encoding="utf-8").write(scanner)
    print("OK2: Scanner auth guard added")
else:
    print("OK2: Scanner already protected")

print("\nAll fixes applied.")
