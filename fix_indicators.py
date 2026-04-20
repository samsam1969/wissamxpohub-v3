f = open("WissamXpoHub_V3_Frontend_FIXED.html", encoding="utf-8")
html = f.read()
f.close()

old = "  /* ─── INIT ─── */"
new = """  /* ─── CONNECTION INDICATORS (stub - elements removed from dashboard) ─── */
  function updateConnectionIndicators(backendOk, authOk) {
    const beDot  = qs("beStatusDot");
    const beTxt  = qs("beStatusText");
    const authDot = qs("authStatusDot");
    const authTxt = qs("authStatusText");
    if (beDot)  beDot.style.background  = backendOk ? "var(--ok)" : "var(--muted)";
    if (beTxt)  beTxt.textContent       = backendOk ? "متصل" : "غير محدد";
    if (authDot) authDot.style.background = authOk ? "var(--ok)" : "var(--muted)";
    if (authTxt) authTxt.textContent      = authOk ? "مسجّل الدخول" : "غير مسجّل الدخول";
  }

  /* ─── INIT ─── */"""

if old in html:
    html = html.replace(old, new, 1)
    open("WissamXpoHub_V3_Frontend_FIXED.html", "w", encoding="utf-8").write(html)
    print("OK - stub added")
else:
    print("Not found")
