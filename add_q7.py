f = open("WissamXpoHub_V3_Frontend_FIXED.html", encoding="utf-8")
html = f.read()
f.close()

old = """          <button type="button" onclick="setQ(this)" data-q="ما هي أفضل قنوات التوزيع والدخول للسوق؟ هل عبر وسيط، أو مباشر لسلاسل التجزئة، أو عبر منصات B2B؟ مع أمثلة على شركات ناجحة." style="padding:8px 10px;background:rgba(245,158,11,.08);border:1px solid rgba(245,158,11,.25);border-radius:9px;color:#fcd34d;font-size:12px;font-weight:700;font-family:'Cairo',Arial,sans-serif;cursor:pointer;text-align:right;line-height:1.5;transition:border-color .15s;" onmouseover="this.style.borderColor='rgba(245,158,11,.6)'" onmouseout="this.style.borderColor='rgba(245,158,11,.25)'">🚀 قنوات التوزيع واستراتيجية الدخول</button>"""

new = """          <button type="button" onclick="setQ(this)" data-q="ما هي أفضل قنوات التوزيع والدخول للسوق؟ هل عبر وسيط، أو مباشر لسلاسل التجزئة، أو عبر منصات B2B؟ مع أمثلة على شركات ناجحة." style="padding:8px 10px;background:rgba(245,158,11,.08);border:1px solid rgba(245,158,11,.25);border-radius:9px;color:#fcd34d;font-size:12px;font-weight:700;font-family:'Cairo',Arial,sans-serif;cursor:pointer;text-align:right;line-height:1.5;transition:border-color .15s;" onmouseover="this.style.borderColor='rgba(245,158,11,.6)'" onmouseout="this.style.borderColor='rgba(245,158,11,.25)'">🚀 قنوات التوزيع واستراتيجية الدخول</button>
          <button type="button" onclick="setQ(this)" data-q="ما هو أفضل موسم وتوقيت للتصدير لهذا المنتج؟ حلل الطلب الموسمي في السوق المستهدف، أوقات الذروة، المواسم التنافسية، وأنسب شهور الشحن لتحقيق أعلى سعر وأقل منافسة." style="padding:8px 10px;background:rgba(139,92,246,.08);border:1px solid rgba(139,92,246,.25);border-radius:9px;color:#c4b5fd;font-size:12px;font-weight:700;font-family:'Cairo',Arial,sans-serif;cursor:pointer;text-align:right;line-height:1.5;transition:border-color .15s;" onmouseover="this.style.borderColor='rgba(139,92,246,.6)'" onmouseout="this.style.borderColor='rgba(139,92,246,.25)'">📅 أفضل موسم وتوقيت للتصدير</button>"""

if old in html:
    html = html.replace(old, new, 1)
    open("WissamXpoHub_V3_Frontend_FIXED.html", "w", encoding="utf-8").write(html)
    print("OK - question added")
else:
    print("Not found")
