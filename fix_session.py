f = open("WissamXpoHub_V3_Frontend_FIXED.html", encoding="utf-8")
html = f.read()
f.close()

old = """    // No active session — restore saved token if any
    const savedToken = localStorage.getItem("wx_access_token");
    if (savedToken) {
      if (qs("accessToken")) qs("accessToken").value = savedToken;
      if (sbSt) sbSt.textContent = "⚠️ توكن محفوظ — سجّل الدخول مجدداً للتحقق";
    } else {
      if (sbSt) sbSt.textContent = "";
    }
  }"""

new = """    // No active session — restore from localStorage
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

if old in html:
    html = html.replace(old, new, 1)
    open("WissamXpoHub_V3_Frontend_FIXED.html", "w", encoding="utf-8").write(html)
    print("OK - session restore fixed")
else:
    print("Not found - searching...")
    idx = html.find("No active session")
    print(repr(html[idx-10:idx+200]))
