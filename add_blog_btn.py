f = open("WissamXpoHub_V3_Frontend_FIXED.html", encoding="utf-8")
html = f.read()
f.close()

old = """          <button type="button" onclick="goToPotentialBuyers()"
            style="width:100%;background:#1e40af;border:none;border-radius:14px;padding:16px 20px;font-size:15px;font-weight:800;font-family:'Cairo',Arial,sans-serif;cursor:pointer;color:#fff;text-align:left;display:flex;align-items:center;gap:12px;">
            <span style="font-size:24px;">&#127970;</span>
            <div>
              <div>Potential Buyers</div>
              <div style="font-size:12px;font-weight:600;color:#93c5fd;margin-top:2px;">Find real importers by HS Code + Country</div>
            </div>
          </button>"""

new = """          <button type="button" onclick="goToPotentialBuyers()"
            style="width:100%;background:#1e40af;border:none;border-radius:14px;padding:16px 20px;font-size:15px;font-weight:800;font-family:'Cairo',Arial,sans-serif;cursor:pointer;color:#fff;text-align:left;display:flex;align-items:center;gap:12px;">
            <span style="font-size:24px;">&#127970;</span>
            <div>
              <div>Potential Buyers</div>
              <div style="font-size:12px;font-weight:600;color:#93c5fd;margin-top:2px;">Find real importers by HS Code + Country</div>
            </div>
          </button>
          <button type="button" onclick="window.location.href='Blog.html'"
            style="width:100%;background:rgba(139,92,246,.18);border:1px solid rgba(139,92,246,.4);border-radius:14px;padding:16px 20px;font-size:15px;font-weight:800;font-family:'Cairo',Arial,sans-serif;cursor:pointer;color:#c4b5fd;text-align:left;display:flex;align-items:center;gap:12px;">
            <span style="font-size:24px;">&#128240;</span>
            <div>
              <div>Blog & Intelligence</div>
              <div style="font-size:12px;font-weight:600;color:#c4b5fd;margin-top:2px;opacity:.8;">أخبار، فرص، طلبات شراء، تحليلات</div>
            </div>
          </button>"""

if old in html:
    html = html.replace(old, new, 1)
    open("WissamXpoHub_V3_Frontend_FIXED.html", "w", encoding="utf-8").write(html)
    print("OK - Blog button added")
else:
    print("Not found")
