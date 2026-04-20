import shutil, re
from datetime import datetime

for fname in ["ExportIntelligence.html", "WissamXpoHub_V3_Frontend_FIXED.html"]:
    f = open(fname, encoding="utf-8")
    html = f.read()
    f.close()
    shutil.copy2(fname, fname.replace(".html", f"_BACKUP_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"))
    changed = False

    # Remove depth section from ExportIntelligence.html
    patterns = [
        # Step 2 depth card section
        r'<!-- Step 2.*?</section>\s*\n\s*<!-- Step 3',
        r'<!-- Step 2.*?</div>\s*\n\s*<!-- Step 3',
        # Depth grid div
        r'<div class="depth-grid">.*?</div>\s*\n\s*</div>\s*\n\s*</div>',
    ]

    # Simple string replacements for depth cards
    removals = [
        # ExportIntelligence depth section
        ('''<!-- Step 2: Depth -->
<div class="card">
  <div class="step-header">
    <div class="step-num">2</div>
    <div>
      <div class="step-title">مستوى التحليل</div>
      <div class="step-sub">اختر عمق التقرير المناسب لاحتياجك</div>
    </div>
  </div>

  <div class="depth-grid">
    <div class="depth-card" id="d-quick" onclick="setDepth('quick')">
      <div class="depth-icon">⚡</div>
      <div class="depth-name">إجابة سريعة</div>
      <div class="depth-desc">إجابة مباشرة ومختصرة</div>
      <div class="depth-time">~30 ثانية</div>
    </div>
    <div class="depth-card active" id="d-pro" onclick="setDepth('pro')">
      <div class="depth-icon">📊</div>
      <div class="depth-name">تحليل احترافي</div>
      <div class="depth-desc">تقرير مفصل مع بيانات</div>
      <div class="depth-time">~60-90 ثانية</div>
    </div>
    <div class="depth-card" id="d-full" onclick="setDepth('full')">
      <div class="depth-icon">📚</div>
      <div class="depth-name">تقرير شامل</div>
      <div class="depth-desc">تحليل معمق متكامل</div>
      <div class="depth-time">~3-5 دقائق</div>
    </div>
  </div>
</div>''', ""),
        # Dashboard depth section
        ('''    <!-- Step 2: Depth -->
    <section class="card" style="margin-top:14px;">
      <div style="display:flex;align-items:center;gap:12px;margin-bottom:14px;">
        <div style="width:26px;height:26px;border-radius:50%;background:linear-gradient(135deg,#3b82f6,#6366f1);display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:800;color:#fff;flex-shrink:0;">2</div>
        <div style="font-size:17px;font-weight:800;">مستوى التحليل</div>
      </div>
      <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;">
        <div id="dd-quick" onclick="setDashDepth('quick')" style="padding:14px;background:rgba(0,0,0,.25);border:1.5px solid var(--line);border-radius:12px;cursor:pointer;text-align:center;transition:all .15s;">
          <div style="font-size:20px;margin-bottom:5px;">⚡</div>
          <div style="font-size:12px;font-weight:800;">إجابة سريعة</div>
          <div style="font-size:10px;color:var(--muted);margin-top:3px;">~30 ثانية</div>
        </div>
        <div id="dd-pro" onclick="setDashDepth('pro')" style="padding:14px;background:rgba(59,130,246,.1);border:1.5px solid var(--btn);border-radius:12px;cursor:pointer;text-align:center;transition:all .15s;">
          <div style="font-size:20px;margin-bottom:5px;">📊</div>
          <div style="font-size:12px;font-weight:800;">تحليل احترافي</div>
          <div style="font-size:10px;color:var(--muted);margin-top:3px;">~90 ثانية</div>
        </div>
        <div id="dd-full" onclick="setDashDepth('full')" style="padding:14px;background:rgba(0,0,0,.25);border:1.5px solid var(--line);border-radius:12px;cursor:pointer;text-align:center;transition:all .15s;">
          <div style="font-size:20px;margin-bottom:5px;">📚</div>
          <div style="font-size:12px;font-weight:800;">تقرير شامل</div>
          <div style="font-size:10px;color:var(--muted);margin-top:3px;">~5 دقائق</div>
        </div>
      </div>
    </section>''', ""),
    ]

    for old, new in removals:
        if old in html:
            html = html.replace(old, new, 1)
            print(f"OK: depth section removed from {fname}")
            changed = True

    # Fix step numbers - Step 3 becomes Step 2
    html = html.replace(
        '<div class="step-num">3</div>\n      <div>\n        <div class="step-title">المنتج والسوق</div>',
        '<div class="step-num">2</div>\n      <div>\n        <div class="step-title">المنتج والسوق</div>'
    )
    html = html.replace(
        '<div style="width:26px;height:26px;border-radius:50%;background:linear-gradient(135deg,#3b82f6,#6366f1);display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:800;color:#fff;flex-shrink:0;">3</div>\n        <div style="font-size:17px;font-weight:800;">المنتج والسوق</div>',
        '<div style="width:26px;height:26px;border-radius:50%;background:linear-gradient(135deg,#3b82f6,#6366f1);display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:800;color:#fff;flex-shrink:0;">2</div>\n        <div style="font-size:17px;font-weight:800;">المنتج والسوق</div>'
    )

    if changed:
        open(fname, "w", encoding="utf-8").write(html)
        print(f"Saved: {fname}")
    else:
        print(f"No change: {fname}")

# Fix claude_service to always use "pro" depth
f = open("services/claude_service.py", encoding="utf-8")
c = f.read()
f.close()
# Force depth to full always
old_depth = '    depth = "pro"\n    intent = "general"\n    question = info'
new_depth = '    depth = "full"  # Always full report — depth selector removed from UI\n    intent = "general"\n    question = info'
if old_depth in c:
    c = c.replace(old_depth, new_depth, 1)
    print("OK: claude_service forced to full depth")
open("services/claude_service.py", "w", encoding="utf-8").write(c)
print("Done")
