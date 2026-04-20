f = open("WissamXpoHub_V3_Frontend_FIXED.html", encoding="utf-8")
html = f.read()
f.close()

old = """            <a href="https://www.mti.gov.eg/" target="_blank" rel="noopener" style="display:flex;align-items:center;gap:10px;padding:9px 12px;background:rgba(220,38,38,.08);border:1px solid rgba(220,38,38,.2);border-radius:10px;text-decoration:none;transition:border-color .15s;" onmouseover="this.style.borderColor='rgba(220,38,38,.5)'" onmouseout="this.style.borderColor='rgba(220,38,38,.2)'">
              <span style="width:8px;height:8px;border-radius:50%;background:#dc2626;flex-shrink:0;"></span>
              <span style="font-size:13px;font-weight:700;color:#fca5a5;flex:1;">وزارة التجارة والصناعة</span>
              <span style="font-size:11px;color:var(--muted);">mti.gov.eg &#8599;</span>
            </a>"""

new = """            <a href="https://www.ecs.gov.eg/" target="_blank" rel="noopener" style="display:flex;align-items:center;gap:10px;padding:9px 12px;background:rgba(220,38,38,.08);border:1px solid rgba(220,38,38,.2);border-radius:10px;text-decoration:none;transition:border-color .15s;" onmouseover="this.style.borderColor='rgba(220,38,38,.5)'" onmouseout="this.style.borderColor='rgba(220,38,38,.2)'">
              <span style="width:8px;height:8px;border-radius:50%;background:#dc2626;flex-shrink:0;"></span>
              <span style="font-size:13px;font-weight:700;color:#fca5a5;flex:1;">التمثيل التجاري المصري</span>
              <span style="font-size:11px;color:var(--muted);">ecs.gov.eg &#8599;</span>
            </a>"""

if old in html:
    html = html.replace(old, new, 1)
    open("WissamXpoHub_V3_Frontend_FIXED.html", "w", encoding="utf-8").write(html)
    print("OK - replaced with ecs.gov.eg")
else:
    print("Not found")
