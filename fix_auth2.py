import shutil
from datetime import datetime

f = open("WissamXpoHub_V3_Frontend_FIXED.html", encoding="utf-8")
html = f.read()
f.close()

ts = datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2("WissamXpoHub_V3_Frontend_FIXED.html", f"WissamXpoHub_V3_Frontend_FIXED_BACKUP_{ts}.html")

start = html.find("checkExistingSession() {")
end   = html.find("\n\n\n  /* ─── ANALYTICS DASHBOARD ─── */")

if start != -1 and end != -1:
    new_fn = """checkExistingSession() {
    const sbSt = qs("sbStatus");

    // STEP 1: Restore from localStorage IMMEDIATELY (no network delay)
    const savedToken = localStorage.getItem("wx_access_token");
    const savedEmail = localStorage.getItem("wx_user_email");

    if (savedToken && savedEmail) {
      updateUserBar({ email: savedEmail });
      if (qs("accessToken")) qs("accessToken").value = savedToken;
      if (sbSt) { sbSt.textContent = "✓ مسجّل الدخول — " + savedEmail; sbSt.style.color = "#10b981"; }
      const plan = localStorage.getItem("wx_user_plan") || "pro";
      const rem  = localStorage.getItem("wx_user_remaining") || "";
      if (qs("userPlan"))      qs("userPlan").textContent  = plan;
      if (qs("statPlan"))      qs("statPlan").textContent  = plan;
      if (rem) {
        if (qs("userRemaining")) qs("userRemaining").textContent = rem + " credits";
        if (qs("statRemaining")) qs("statRemaining").textContent = rem;
      }
    }

    // STEP 2: Background Supabase refresh (non-blocking, never clears UI)
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
      if (error) { console.warn("getSession:", error.message); return; }

      if (data?.session?.access_token) {
        const token = data.session.access_token;
        const user  = data.session.user;
        localStorage.setItem("wx_access_token", token);
        localStorage.setItem("wx_user_email",   user?.email || "");
        if (qs("accessToken")) qs("accessToken").value = token;
        if (!savedToken) {
          updateUserBar(user);
          if (sbSt) sbSt.textContent = "✓ مسجّل الدخول — " + (user?.email || "");
        }
      }
      // CRITICAL: Never call updateUserBar(null) — causes logout
    } catch (e) {
      console.warn("Session check error:", e);
    }
  }"""

    html = html[:start] + new_fn + html[end:]
    open("WissamXpoHub_V3_Frontend_FIXED.html", "w", encoding="utf-8").write(html)
    print("OK - auth fixed, size:", len(html))
else:
    print("FAIL - start:", start, "end:", end)
