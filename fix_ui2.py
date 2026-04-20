import shutil, re
from datetime import datetime

f = open("WissamXpoHub_V3_Frontend_FIXED.html", encoding="utf-8")
html = f.read()
f.close()
shutil.copy2("WissamXpoHub_V3_Frontend_FIXED.html", f"WissamXpoHub_V3_Frontend_FIXED_BACKUP_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html")

# 1. Remove duplicate sources button (keep only one)
btn1 = """          <button type="button" id="showSourcesBtn" onclick="toggleSourcesPanel()" style="padding:8px 14px;font-size:13px;border-radius:10px;background:rgba(99,102,241,.15);border:1px solid rgba(99,102,241,.4);color:#a5b4fc;font-weight:700;font-family:'Cairo',Arial,sans-serif;cursor:pointer;">🔍 مصادر البيانات</button>"""

count = html.count(btn1)
print(f"Sources button count: {count}")
if count > 1:
    # Remove all then add one
    html = html.replace(btn1, "", count)
    # Add back once in right place
    old_copy = """          <button type="button" class="secondary" onclick="copyBoxText('aiBox')" style="padding:8px 14px;font-size:13px;border-radius:10px;">📋 نسخ</button>
          <button type="button" class="success" onclick="exportBoxToPdf('AI Export Advisor','aiBox')" style="padding:8px 14px;font-size:13px;border-radius:10px;">📄 PDF</button>"""
    new_copy = old_copy + "\n" + btn1
    if old_copy in html:
        html = html.replace(old_copy, new_copy, 1)
        print("OK1: duplicate removed, kept one")

# 2. Fix setDashQ - check if function exists
if "function setDashQ(" in html:
    print("OK: setDashQ exists")
else:
    print("MISSING: setDashQ not found - adding...")
    # Add after toggleSourcesPanel function
    old_marker = "  function toggleSourcesPanel() {"
    new_fn = """  function setDashQ(btn, text) {
    document.querySelectorAll(".dash-q-btn").forEach(b => b.classList.remove("dq-active"));
    btn.classList.add("dq-active");
    const q = qs("userQuestion");
    if(q) { q.value = text; onDashQuestion(); }
  }

  function setDashDepth(d) {
    dashDepth = d;
    ["quick","pro","full"].forEach(x => {
      const el = qs("dd-"+x);
      if(!el) return;
      el.style.borderColor = x===d ? "var(--btn,#3b82f6)" : "var(--line)";
      el.style.background  = x===d ? "rgba(59,130,246,.1)" : "rgba(0,0,0,.25)";
    });
  }

  function toggleSourcesPanel() {"""
    if old_marker in html:
        html = html.replace(old_marker, new_fn, 1)
        print("OK2: setDashQ added")

# 3. Check onDashQuestion exists
if "function onDashQuestion(" in html:
    print("OK: onDashQuestion exists")
else:
    print("MISSING: onDashQuestion - adding...")
    old_toggle = "  function toggleSourcesPanel() {"
    add_fn = """  function onDashQuestion() {
    detectDashIntent();
    updateDashPreview();
  }

  function toggleSourcesPanel() {"""
    if old_toggle in html:
        html = html.replace(old_toggle, add_fn, 1)
        print("OK3: onDashQuestion added")

# 4. Verify quick buttons call correct function
q_btn_count = html.count("onclick=\"setDashQ(")
print(f"setDashQ calls in HTML: {q_btn_count}")

# 5. Add CSS for active state if missing
if ".dq-active" not in html:
    old_css = ".dash-q-btn:hover,.dash-q-btn.dq-active{"
    if old_css not in html:
        old_css2 = "    .dash-q-btn{"
        new_css = """    .dash-q-btn{
      padding:7px 13px;background:rgba(59,130,246,.08);border:1px solid rgba(59,130,246,.2);
      border-radius:999px;color:#60a5fa;font-size:12px;font-weight:700;
      font-family:'Cairo',Arial,sans-serif;cursor:pointer;transition:all .15s;white-space:nowrap;
    }
    .dash-q-btn:hover,.dash-q-btn.dq-active{
      background:rgba(59,130,246,.25);border-color:var(--blue,#3b82f6);color:#fff;
    }"""
        if old_css2 in html:
            html = html.replace(old_css2, new_css, 1)
            print("OK5: CSS active state added")

open("WissamXpoHub_V3_Frontend_FIXED.html", "w", encoding="utf-8").write(html)
print("Done - size:", len(html))
