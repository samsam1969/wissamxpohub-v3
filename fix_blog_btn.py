f = open("WissamXpoHub_V3_Frontend_FIXED.html", encoding="utf-8")
html = f.read()
f.close()

old = """          <button type="button" onclick="window.location.href='Blog.html'"
            style="width:100%;padding:11px;background:rgba(16,185,129,.15);border:1px solid rgba(16,185,129,.3);border-radius:10px;color:#6ee7b7;font-size:13px;font-weight:800;font-family:'Cairo',Arial,sans-serif;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:8px;">
            📝 المدونة والأخبار
          </button>"""

new = """          <button type="button" onclick="window.location.href='Blog.html'"
            style="width:100%;padding:11px;background:rgba(234,179,8,.15);border:1px solid rgba(234,179,8,.4);border-radius:10px;color:#fde047;font-size:13px;font-weight:800;font-family:'Cairo',Arial,sans-serif;cursor:pointer;display:flex;flex-direction:column;align-items:center;gap:3px;">
            <span>📝 Blog — المدونة والأخبار التصديرية</span>
            <span style="font-size:10px;font-weight:400;color:rgba(253,224,71,.7);">أخبار التصدير · فرص السوق · طلبات الشراء · تحليلات</span>
          </button>"""

if old in html:
    html = html.replace(old, new, 1)
    print("OK: Blog button updated")
else:
    print("Not found")

open("WissamXpoHub_V3_Frontend_FIXED.html", "w", encoding="utf-8").write(html)
