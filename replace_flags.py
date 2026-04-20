import shutil
from datetime import datetime

f = open("WissamXpoHub_V3_Frontend_FIXED.html", encoding="utf-8")
html = f.read()
f.close()

shutil.copy2("WissamXpoHub_V3_Frontend_FIXED.html", f"WissamXpoHub_V3_Frontend_FIXED_BACKUP_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html")

# Find the exact block to replace
old = """        <div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:10px;">
          <button type="button" onclick="window.location.href='PotentialBuyers.html'" style="flex:1;background:#1e40af;border:none;border-radius:12px;padding:10px 16px;font-size:13px;font-weight:800;font-family:'Cairo',Arial,sans-serif;cursor:pointer;color:#fff;box-shadow:0 4px 12px rgba(0,0,0,.2);">&#127970; Potential Buyers</button>
          <button type="button" onclick="window.location.href='ExportOpportunityScanner.html'" style="flex:1;background:rgba(16,185,129,.18);border:1px solid rgba(16,185,129,.4);border-radius:12px;padding:10px 16px;font-size:13px;font-weight:800;font-family:'Cairo',Arial,sans-serif;cursor:pointer;color:#6ee7b7;box-shadow:0 4px 12px rgba(0,0,0,.2);">&#127757; Export Scanner</button>
        </div>"""

new = """        <!-- Animated Egypt-EU branding -->
        <div style="display:flex;align-items:center;justify-content:center;gap:20px;margin-top:18px;padding:16px;background:rgba(0,0,0,.15);border:1px solid var(--line);border-radius:14px;">
          <div style="display:flex;flex-direction:column;align-items:center;gap:6px;animation:flagFloat 3s ease-in-out infinite;">
            <div style="font-size:36px;filter:drop-shadow(0 2px 8px rgba(0,0,0,.4));">&#127466;&#127468;</div>
            <div style="font-size:10px;font-weight:700;color:var(--muted);letter-spacing:1px;">EGYPT</div>
          </div>
          <div style="display:flex;flex-direction:column;align-items:center;gap:4px;">
            <div style="display:flex;align-items:center;gap:6px;">
              <div style="width:20px;height:1px;background:linear-gradient(90deg,transparent,var(--line2));animation:pulse 2s ease-in-out infinite;"></div>
              <div style="font-size:16px;font-weight:800;color:var(--line2);animation:pulse 2s ease-in-out infinite;">&#8594;</div>
              <div style="width:20px;height:1px;background:linear-gradient(90deg,var(--line2),transparent);animation:pulse 2s ease-in-out infinite;"></div>
            </div>
            <div style="font-size:9px;color:var(--muted);font-weight:700;letter-spacing:1.5px;margin-top:2px;">EXPORT</div>
          </div>
          <div style="display:flex;flex-direction:column;align-items:center;gap:6px;animation:flagFloat 3s ease-in-out infinite;animation-delay:.5s;">
            <div style="font-size:36px;filter:drop-shadow(0 2px 8px rgba(0,0,0,.4));">&#127466;&#127482;</div>
            <div style="font-size:10px;font-weight:700;color:var(--muted);letter-spacing:1px;">EU</div>
          </div>
        </div>
        <style>
          @keyframes flagFloat {
            0%,100% { transform: translateY(0); }
            50%      { transform: translateY(-5px); }
          }
          @keyframes pulse {
            0%,100% { opacity:.4; }
            50%      { opacity:1; }
          }
        </style>"""

if old in html:
    html = html.replace(old, new, 1)
    open("WissamXpoHub_V3_Frontend_FIXED.html", "w", encoding="utf-8").write(html)
    print("OK - buttons replaced with animated flags")
else:
    print("Pattern not found - searching...")
    idx = html.find("PotentialBuyers.html")
    while idx != -1:
        ctx = html[idx-200:idx+100]
        if "flex:1" in ctx:
            print("Found at:", idx)
            print(repr(ctx))
            break
        idx = html.find("PotentialBuyers.html", idx+1)
