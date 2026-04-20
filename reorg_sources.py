import shutil
from datetime import datetime

f = open("WissamXpoHub_V3_Frontend_FIXED.html", encoding="utf-8")
html = f.read()
f.close()
shutil.copy2("WissamXpoHub_V3_Frontend_FIXED.html", f"WissamXpoHub_V3_Frontend_FIXED_BACKUP_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html")

old_start = "        <!-- Data Sources Quick Access -->"
old_end   = "        </div>"

si = html.find(old_start)
ei = html.find(old_end, si) + len(old_end)

def src_link(url, label, sublabel, color):
    colors = {
        "blue":   ("rgba(29,78,216,.08)",  "rgba(29,78,216,.25)",  "rgba(59,130,246,.6)",  "#3b82f6", "#93c5fd"),
        "green":  ("rgba(16,185,129,.06)", "rgba(16,185,129,.2)",  "rgba(16,185,129,.5)",  "#10b981", "#6ee7b7"),
        "purple": ("rgba(139,92,246,.08)", "rgba(139,92,246,.25)", "rgba(139,92,246,.6)",  "#8b5cf6", "#c4b5fd"),
        "red":    ("rgba(220,38,38,.08)",  "rgba(220,38,38,.2)",   "rgba(220,38,38,.5)",   "#dc2626", "#fca5a5"),
        "amber":  ("rgba(217,119,6,.08)",  "rgba(217,119,6,.2)",   "rgba(217,119,6,.5)",   "#d97706", "#fcd34d"),
    }
    bg, border, hover, dot, text = colors[color]
    return f"""            <a href="{url}" target="_blank" rel="noopener" style="display:flex;align-items:center;gap:10px;padding:9px 12px;background:{bg};border:1px solid {border};border-radius:10px;text-decoration:none;transition:border-color .15s;" onmouseover="this.style.borderColor='{hover}'" onmouseout="this.style.borderColor='{border}'">
              <span style="width:8px;height:8px;border-radius:50%;background:{dot};flex-shrink:0;"></span>
              <span style="font-size:13px;font-weight:700;color:{text};flex:1;">{label}</span>
              <span style="font-size:11px;color:var(--muted);">{sublabel} &#8599;</span>
            </a>"""

def section(title, color):
    colors = {"blue":"#3b82f6","green":"#10b981","purple":"#8b5cf6","red":"#dc2626","amber":"#d97706"}
    c = colors[color]
    return f"""            <div style="font-size:10px;font-weight:700;color:{c};letter-spacing:1.2px;text-transform:uppercase;margin:10px 0 6px;padding-bottom:4px;border-bottom:1px solid rgba(255,255,255,.06);">{title}</div>"""

new_block = """        <!-- Data Sources Quick Access -->
        <div style="margin-top:16px;">
          <div style="font-size:11px;font-weight:700;color:var(--muted);letter-spacing:1.5px;text-transform:uppercase;margin-bottom:10px;padding-bottom:6px;border-bottom:1px solid var(--line);">Quick Access — Data Sources</div>
          <div style="display:flex;flex-direction:column;gap:5px;max-height:420px;overflow-y:auto;padding-right:2px;">
""" + section("EU & International Trade", "blue") + """
""" + src_link("https://www.trademap.org/", "ITC Trade Map", "trademap.org", "blue") + """
""" + src_link("https://comtrade.un.org/", "UN Comtrade", "comtrade.un.org", "blue") + """
""" + src_link("https://wits.worldbank.org/", "World Bank WITS", "wits.worldbank.org", "blue") + """
""" + src_link("https://www.worldbank.org/", "World Bank Group", "worldbank.org", "blue") + """
""" + src_link("https://trade.ec.europa.eu/access-to-markets/", "EU Access2Markets", "trade.ec.europa.eu", "blue") + """
""" + src_link("https://taxation-customs.ec.europa.eu/customs-4/calculation-customs-duties/customs-tariff/eu-customs-tariff-taric_en", "EU TARIC", "ec.europa.eu", "blue") + """
""" + src_link("https://ec.europa.eu/eurostat", "Eurostat", "eurostat.eu", "blue") + """
""" + src_link("https://ted.europa.eu/", "TED Tenders (EU)", "ted.europa.eu", "blue") + """
""" + section("Market Research & Analysis", "green") + """
""" + src_link("https://www.cbi.eu/market-information", "CBI Netherlands", "cbi.eu", "green") + """
""" + src_link("https://east-fruit.com/", "EastFruit", "east-fruit.com", "green") + """
""" + section("B2B & Buyer Discovery", "purple") + """
""" + src_link("https://globy.com/", "Globy B2B", "globy.com", "purple") + """
""" + src_link("https://www.europages.com/", "Europages", "europages.com", "purple") + """
""" + src_link("https://www.jctrans.net/zhyx/tgc/pc/indexEN.htm", "JCTrans", "jctrans.net", "purple") + """
""" + src_link("https://www.apollo.io/sign-up", "Apollo.io", "apollo.io", "purple") + """
""" + section("Egyptian Official Sources", "red") + """
""" + src_link("https://www.expoegypt.gov.eg/map", "بوابة الصادرات المصرية", "expoegypt.gov.eg", "red") + """
""" + src_link("https://www.goeic.gov.eg/users/default/login/lang/ar", "GOEIC — هيئة الرقابة", "goeic.gov.eg", "red") + """
""" + src_link("http://www.customs.gov.eg/", "الجمارك المصرية", "customs.gov.eg", "red") + """
          </div>
        </div>"""

if si != -1 and ei > si:
    html = html[:si] + new_block + html[ei:]
    open("WissamXpoHub_V3_Frontend_FIXED.html", "w", encoding="utf-8").write(html)
    print("OK - sources reorganized, size:", len(html))
else:
    print("FAIL - si:", si, "ei:", ei)
