f = open("WissamXpoHub_V3_Frontend_FIXED.html", encoding="utf-8")
html = f.read()
f.close()

# Fix reset button - rename + fix function
old = """        <button type="button" onclick="resetAll()" class="ghost" style="padding:15px 18px;">إعادة</button>"""
new = """        <button type="button" onclick="resetDashboard()" class="ghost" style="padding:15px 18px;font-weight:800;">← BACK</button>"""

if old in html:
    html = html.replace(old, new, 1)
    print("OK1: button renamed")
else:
    print("FAIL1")

# Add resetDashboard function
old_marker = "  /* ─── DASHBOARD AI ADVISOR NEW UX ─── */"
new_fn = """  /* ─── DASHBOARD AI ADVISOR NEW UX ─── */
  function resetDashboard() {
    // Clear inputs
    const q = qs("userQuestion"); if(q) q.value = "";
    const hs = qs("hs"); if(hs) hs.value = "";
    const country = qs("country"); if(country) country.value = "__ALL__";
    // Clear output
    const box = qs("aiBox");
    if(box) box.innerHTML = "شغّل Export Intelligence لإنشاء تقرير مخصص بناءً على سؤالك.";
    const sub = qs("reportSubtitle"); if(sub) sub.textContent = "";
    const disc = qs("aiDisclaimer"); if(disc) disc.style.display = "none";
    // Clear quick buttons
    document.querySelectorAll(".dash-q-btn").forEach(b => b.classList.remove("dq-active"));
    // Reset depth to pro
    setDashDepth("pro");
    // Hide preview
    const prev = qs("dashPreview"); if(prev) prev.style.display = "none";
    // Reset product hint
    const hint = qs("productNameBox"); if(hint) hint.textContent = "";
    // Scroll to top
    window.scrollTo({top: 0, behavior: "smooth"});
  }
"""

if old_marker in html:
    html = html.replace(old_marker, new_fn, 1)
    print("OK2: resetDashboard function added")
else:
    print("FAIL2: marker not found")

open("WissamXpoHub_V3_Frontend_FIXED.html", "w", encoding="utf-8").write(html)
print("Done")
