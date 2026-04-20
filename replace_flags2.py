import shutil
from datetime import datetime

f = open("WissamXpoHub_V3_Frontend_FIXED.html", encoding="utf-8")
html = f.read()
f.close()

shutil.copy2("WissamXpoHub_V3_Frontend_FIXED.html", f"WissamXpoHub_V3_Frontend_FIXED_BACKUP_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html")

# Find start of the buttons div
start = html.find('\n\n\n        <div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:10px;">')
# Find end
end = html.find("</div>", start) + 6

print("start:", start, "end:", end)
print("BLOCK:", repr(html[start:end]))

new = """

        <!-- Animated Egypt-EU branding -->
        <div style="display:flex;align-items:center;justify-content:center;gap:20px;margin-top:18px;padding:16px;background:rgba(0,0,0,.15);border:1px solid var(--line);border-radius:14px;">
          <div style="display:flex;flex-direction:column;align-items:center;gap:6px;animation:flagFloat 3s ease-in-out infinite;">
            <div style="font-size:36px;filter:drop-shadow(0 2px 8px rgba(0,0,0,.4));">&#127466;&#127468;</div>
            <div style="font-size:10px;font-weight:700;color:var(--muted);letter-spacing:1px;">EGYPT</div>
          </div>
          <div style="display:flex;flex-direction:column;align-items:center;gap:4px;">
            <div style="display:flex;align-items:center;gap:6px;">
              <div style="width:20px;height:1px;background:linear-gradient(90deg,transparent,var(--line2));animation:arrowPulse 2s ease-in-out infinite;"></div>
              <div style="font-size:16px;font-weight:800;color:#60a5fa;animation:arrowPulse 2s ease-in-out infinite;">&#8594;</div>
              <div style="width:20px;height:1px;background:linear-gradient(90deg,var(--line2),transparent);animation:arrowPulse 2s ease-in-out infinite;"></div>
            </div>
            <div style="font-size:9px;color:var(--muted);font-weight:700;letter-spacing:1.5px;margin-top:2px;">EXPORT</div>
          </div>
          <div style="display:flex;flex-direction:column;align-items:center;gap:6px;animation:flagFloat 3s ease-in-out infinite;animation-delay:.5s;">
            <div style="font-size:36px;filter:drop-shadow(0 2px 8px rgba(0,0,0,.4));">&#127466;&#127482;</div>
            <div style="font-size:10px;font-weight:700;color:var(--muted);letter-spacing:1px;">EU</div>
          </div>
        </div>"""

if start != -1 and end > start:
    html = html[:start] + new + html[end:]
    open("WissamXpoHub_V3_Frontend_FIXED.html", "w", encoding="utf-8").write(html)
    print("OK - done")
else:
    print("FAIL")
