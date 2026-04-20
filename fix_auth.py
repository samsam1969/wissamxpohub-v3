f = open("WissamXpoHub_V3_Frontend_FIXED.html", encoding="utf-8")
html = f.read()
f.close()
import shutil
from datetime import datetime
ts = datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2("WissamXpoHub_V3_Frontend_FIXED.html", f"WissamXpoHub_V3_Frontend_FIXED_BACKUP_{ts}.html")

# Fix checkExistingSession - use localStorage as primary source
old = """  /* ─── CHECK EXISTING SESSION ON LOAD ─── */
  async function checkExistingSession() {
    const sbSt = qs("sbStatus");

    // Wait for Supabase lib (max 5 seconds)
    let attempts = 0;
    while (typeof window.supabase === "undefined" && attempts < 50) {
      await new Promise(r => setTimeout(r, 100));
      attempts++;
    }

    if (typeof window.supabase === "undefined") {
      if (sbSt) sbSt.textContent = "⚠️ Supabase غير محمّل — تأكد من اتصال الإنترنت";
      return;
    }

    if (!initSupabase()) return;
    if (sbSt) sbSt.textContent = "✓ Supabase متصل";

    try {
      const { data, error } = await supabaseClient.auth.getSession();
      if (error) { console.warn("getSession error:", error.message); }

      if (data?.session?.access_token) {
        const token = data.session.access_token;
        localStorage.setItem("wx_access_token", token);
        if (qs("accessToken")) qs("accessToken").value = token;
        saveSettings();
        updateUserBar(data.session.user);
        if (sbSt) sbSt.textContent = "✓ مسجّل الدخول — " + (data.session.user?.email || "");

        // Restore plan + credits
        const plan      = localStorage.getItem("wx_user_plan")      || "pro";
        const remaining = localStorage.getItem("wx_user_remaining")  || "";
        if (qs("userPlan"))      qs("userPlan").textContent      = plan;
        if (qs("statPlan"))      qs("statPlan").textContent      = plan;
        if (remaining) {
          if (qs("userRemaining"))  qs("userRemaining").textContent  = remaining + " credits";
          if (qs("statRemaining"))  qs("statRemaining").textContent  = remaining;
        }
        return;
      }
    } catch (e) { console.warn("Session check error:", e); }

    // No active session — restore saved token if any
    const savedToken = localStorage.getItem("wx_access_token");
    const savedEmail = localStorage.getItem("wx_user_email");
    if (savedToken && savedEmail) {
      if (qs("accessToken")) qs("accessToken").value = savedToken;
      // Restore user bar from saved data
      updateUserBar({ email: savedEmail });
      if (sbSt) { sbSt.textContent = "✓ مسجّل الدخول — " + savedEmail; sbSt.style.color = "#10b981"; }
      // Restore plan + credits
      const plan      = localStorage.getItem("wx_user_plan")      || "pro";
      const remaining = localStorage.getItem("wx_user_remaining")  || "";
      if (qs("userPlan"))      qs("userPlan").textContent      = plan;
      if (qs("statPlan"))      qs("statPlan").textContent      = plan;
      if (remaining) {
        if (qs("userRemaining")) qs("userRemaining").textContent = remaining + " credits";
        if (qs("statRemaining")) qs("statRemaining").textContent = remaining;
      }
    } else {
      if (sbSt) sbSt.textContent = "";
    }
  }"""

new = """  /* ─── CHECK EXISTING SESSION ON LOAD ─── */
  async function checkExistingSession() {
    const sbSt = qs("sbStatus");

    // STEP 1: Restore from localStorage FIRST (instant, no network)
    const savedToken = localStorage.getItem("wx_access_token");
    const savedEmail = localStorage.getItem("wx_user_email");

    if (savedToken && savedEmail) {
      // Restore UI immediately
      updateUserBar({ email: savedEmail });
      if (qs("accessToken")) qs("accessToken").value = savedToken;
      if (sbSt) { sbSt.textContent = "✓ مسجّل الدخول — " + savedEmail; sbSt.style.color = "#10b981"; }
      const plan      = localStorage.getItem("wx_user_plan")      || "pro";
      const remaining = localStorage.getItem("wx_user_remaining")  || "";
      if (qs("userPlan"))      qs("userPlan").textContent      = plan;
      if (qs("statPlan"))      qs("statPlan").textContent      = plan;
      if (remaining) {
        if (qs("userRemaining"))  qs("userRemaining").textContent  = remaining + " credits";
        if (qs("statRemaining"))  qs("statRemaining").textContent  = remaining;
      }
    }

    // STEP 2: Try Supabase in background to refresh token (non-blocking)
    let attempts = 0;
    while (typeof window.supabase === "undefined" && attempts < 30) {
      await new Promise(r => setTimeout(r, 100));
      attempts++;
    }
    if (typeof window.supabase === "undefined") {
      if (sbSt && !savedToken) sbSt.textContent = "⚠️ Supabase غير محمّل";
      return;
    }
    if (!initSupabase()) return;

    try {
      const { data, error } = await supabaseClient.auth.getSession();
      if (error) { console.warn("getSession error:", error.message); return; }

      if (data?.session?.access_token) {
        const token = data.session.access_token;
        const user  = data.session.user;
        // Update token silently
        localStorage.setItem("wx_access_token", token);
        localStorage.setItem("wx_user_email",   user?.email || "");
        if (qs("accessToken")) qs("accessToken").value = token;
        // Only update UI if not already logged in
        if (!savedToken) {
          updateUserBar(user);
          if (sbSt) sbSt.textContent = "✓ مسجّل الدخول — " + (user?.email || "");
        }
      } else if (!savedToken) {
        // Truly no session
        if (sbSt) sbSt.textContent = "";
      }
      // IMPORTANT: Never call updateUserBar(null) here — that causes logout
    } catch (e) {
      console.warn("Session check error:", e);
      // Keep localStorage session intact on error
    }
  }"""

if old in html:
    html = html.replace(old, new, 1)
    open("WissamXpoHub_V3_Frontend_FIXED.html", "w", encoding="utf-8").write(html)
    print("OK - checkExistingSession fixed")
else:
    print("Pattern not found")
    idx = html.find("checkExistingSession")
    print("Found at:", idx)
