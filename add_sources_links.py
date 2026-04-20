import shutil
from datetime import datetime

f = open("WissamXpoHub_V3_Frontend_FIXED.html", encoding="utf-8")
html = f.read()
f.close()
shutil.copy2("WissamXpoHub_V3_Frontend_FIXED.html", f"WissamXpoHub_V3_Frontend_FIXED_BACKUP_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html")

si = html.find("        <!-- Flags Showcase -->")
ei = html.find("        </div>\n        </div>", si) + len("        </div>\n        </div>")

new_block = """        <!-- Data Sources Quick Access -->
        <div style="margin-top:16px;">
          <div style="font-size:11px;font-weight:700;color:var(--muted);letter-spacing:1.5px;text-transform:uppercase;margin-bottom:10px;padding-bottom:6px;border-bottom:1px solid var(--line);">Quick Access — Data Sources</div>
          <div style="display:flex;flex-direction:column;gap:6px;">
            <a href="https://www.trademap.org/" target="_blank" rel="noopener" style="display:flex;align-items:center;gap:10px;padding:9px 12px;background:rgba(29,78,216,.08);border:1px solid rgba(29,78,216,.25);border-radius:10px;text-decoration:none;transition:border-color .15s;" onmouseover="this.style.borderColor='rgba(59,130,246,.6)'" onmouseout="this.style.borderColor='rgba(29,78,216,.25)'">
              <span style="width:8px;height:8px;border-radius:50%;background:#3b82f6;flex-shrink:0;"></span>
              <span style="font-size:13px;font-weight:700;color:#93c5fd;flex:1;">ITC Trade Map</span>
              <span style="font-size:11px;color:var(--muted);">trademap.org &#8599;</span>
            </a>
            <a href="https://comtrade.un.org/" target="_blank" rel="noopener" style="display:flex;align-items:center;gap:10px;padding:9px 12px;background:rgba(29,78,216,.08);border:1px solid rgba(29,78,216,.25);border-radius:10px;text-decoration:none;transition:border-color .15s;" onmouseover="this.style.borderColor='rgba(59,130,246,.6)'" onmouseout="this.style.borderColor='rgba(29,78,216,.25)'">
              <span style="width:8px;height:8px;border-radius:50%;background:#3b82f6;flex-shrink:0;"></span>
              <span style="font-size:13px;font-weight:700;color:#93c5fd;flex:1;">UN Comtrade</span>
              <span style="font-size:11px;color:var(--muted);">comtrade.un.org &#8599;</span>
            </a>
            <a href="https://trade.ec.europa.eu/access-to-markets/" target="_blank" rel="noopener" style="display:flex;align-items:center;gap:10px;padding:9px 12px;background:rgba(29,78,216,.08);border:1px solid rgba(29,78,216,.25);border-radius:10px;text-decoration:none;transition:border-color .15s;" onmouseover="this.style.borderColor='rgba(59,130,246,.6)'" onmouseout="this.style.borderColor='rgba(29,78,216,.25)'">
              <span style="width:8px;height:8px;border-radius:50%;background:#3b82f6;flex-shrink:0;"></span>
              <span style="font-size:13px;font-weight:700;color:#93c5fd;flex:1;">EU Access2Markets</span>
              <span style="font-size:11px;color:var(--muted);">trade.ec.europa.eu &#8599;</span>
            </a>
            <a href="https://taxation-customs.ec.europa.eu/customs-4/calculation-customs-duties/customs-tariff/eu-customs-tariff-taric_en" target="_blank" rel="noopener" style="display:flex;align-items:center;gap:10px;padding:9px 12px;background:rgba(29,78,216,.08);border:1px solid rgba(29,78,216,.25);border-radius:10px;text-decoration:none;transition:border-color .15s;" onmouseover="this.style.borderColor='rgba(59,130,246,.6)'" onmouseout="this.style.borderColor='rgba(29,78,216,.25)'">
              <span style="width:8px;height:8px;border-radius:50%;background:#3b82f6;flex-shrink:0;"></span>
              <span style="font-size:13px;font-weight:700;color:#93c5fd;flex:1;">EU TARIC</span>
              <span style="font-size:11px;color:var(--muted);">ec.europa.eu &#8599;</span>
            </a>
            <a href="https://ec.europa.eu/eurostat" target="_blank" rel="noopener" style="display:flex;align-items:center;gap:10px;padding:9px 12px;background:rgba(16,185,129,.06);border:1px solid rgba(16,185,129,.2);border-radius:10px;text-decoration:none;transition:border-color .15s;" onmouseover="this.style.borderColor='rgba(16,185,129,.5)'" onmouseout="this.style.borderColor='rgba(16,185,129,.2)'">
              <span style="width:8px;height:8px;border-radius:50%;background:#10b981;flex-shrink:0;"></span>
              <span style="font-size:13px;font-weight:700;color:#6ee7b7;flex:1;">Eurostat</span>
              <span style="font-size:11px;color:var(--muted);">ec.europa.eu/eurostat &#8599;</span>
            </a>
            <a href="https://www.cbi.eu/market-information" target="_blank" rel="noopener" style="display:flex;align-items:center;gap:10px;padding:9px 12px;background:rgba(16,185,129,.06);border:1px solid rgba(16,185,129,.2);border-radius:10px;text-decoration:none;transition:border-color .15s;" onmouseover="this.style.borderColor='rgba(16,185,129,.5)'" onmouseout="this.style.borderColor='rgba(16,185,129,.2)'">
              <span style="width:8px;height:8px;border-radius:50%;background:#10b981;flex-shrink:0;"></span>
              <span style="font-size:13px;font-weight:700;color:#6ee7b7;flex:1;">CBI Netherlands</span>
              <span style="font-size:11px;color:var(--muted);">cbi.eu &#8599;</span>
            </a>
            <a href="https://globy.com/" target="_blank" rel="noopener" style="display:flex;align-items:center;gap:10px;padding:9px 12px;background:rgba(139,92,246,.08);border:1px solid rgba(139,92,246,.25);border-radius:10px;text-decoration:none;transition:border-color .15s;" onmouseover="this.style.borderColor='rgba(139,92,246,.6)'" onmouseout="this.style.borderColor='rgba(139,92,246,.25)'">
              <span style="width:8px;height:8px;border-radius:50%;background:#8b5cf6;flex-shrink:0;"></span>
              <span style="font-size:13px;font-weight:700;color:#c4b5fd;flex:1;">Globy B2B</span>
              <span style="font-size:11px;color:var(--muted);">globy.com &#8599;</span>
            </a>
            <a href="https://www.europages.com/" target="_blank" rel="noopener" style="display:flex;align-items:center;gap:10px;padding:9px 12px;background:rgba(139,92,246,.08);border:1px solid rgba(139,92,246,.25);border-radius:10px;text-decoration:none;transition:border-color .15s;" onmouseover="this.style.borderColor='rgba(139,92,246,.6)'" onmouseout="this.style.borderColor='rgba(139,92,246,.25)'">
              <span style="width:8px;height:8px;border-radius:50%;background:#8b5cf6;flex-shrink:0;"></span>
              <span style="font-size:13px;font-weight:700;color:#c4b5fd;flex:1;">Europages</span>
              <span style="font-size:11px;color:var(--muted);">europages.com &#8599;</span>
            </a>
            <a href="https://www.exportegypt.gov.eg/" target="_blank" rel="noopener" style="display:flex;align-items:center;gap:10px;padding:9px 12px;background:rgba(220,38,38,.08);border:1px solid rgba(220,38,38,.2);border-radius:10px;text-decoration:none;transition:border-color .15s;" onmouseover="this.style.borderColor='rgba(220,38,38,.5)'" onmouseout="this.style.borderColor='rgba(220,38,38,.2)'">
              <span style="width:8px;height:8px;border-radius:50%;background:#dc2626;flex-shrink:0;"></span>
              <span style="font-size:13px;font-weight:700;color:#fca5a5;flex:1;">صادر مصر</span>
              <span style="font-size:11px;color:var(--muted);">exportegypt.gov.eg &#8599;</span>
            </a>
            <a href="http://www.customs.gov.eg/" target="_blank" rel="noopener" style="display:flex;align-items:center;gap:10px;padding:9px 12px;background:rgba(220,38,38,.08);border:1px solid rgba(220,38,38,.2);border-radius:10px;text-decoration:none;transition:border-color .15s;" onmouseover="this.style.borderColor='rgba(220,38,38,.5)'" onmouseout="this.style.borderColor='rgba(220,38,38,.2)'">
              <span style="width:8px;height:8px;border-radius:50%;background:#dc2626;flex-shrink:0;"></span>
              <span style="font-size:13px;font-weight:700;color:#fca5a5;flex:1;">الجمارك المصرية</span>
              <span style="font-size:11px;color:var(--muted);">customs.gov.eg &#8599;</span>
            </a>
          </div>
        </div>"""

if si != -1 and ei > si:
    html = html[:si] + new_block + html[ei:]
    open("WissamXpoHub_V3_Frontend_FIXED.html", "w", encoding="utf-8").write(html)
    print("OK - sources links added, size:", len(html))
else:
    print("FAIL si:", si, "ei:", ei)
