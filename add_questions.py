import shutil
from datetime import datetime

f = open("WissamXpoHub_V3_Frontend_FIXED.html", encoding="utf-8")
html = f.read()
f.close()
shutil.copy2("WissamXpoHub_V3_Frontend_FIXED.html", f"WissamXpoHub_V3_Frontend_FIXED_BACKUP_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html")

old = """        <label for="userQuestion">Custom Question (optional)</label>
        <textarea id="userQuestion" placeholder="e.g. Focus on cold chain requirements and top importers..." style="min-height:80px;resize:vertical;"></textarea>"""

new = """        <label for="userQuestion" style="margin-bottom:4px;">سؤال مخصص <span style="color:var(--muted);font-size:12px;font-weight:400;">(اختياري — اختر أو اكتب)</span></label>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-bottom:8px;">
          <button type="button" onclick="setQ(this)" data-q="حلل بالتفصيل أهم 5 مستوردين حقيقيين في هذا السوق مع بيانات التواصل والمواقع الإلكترونية وحجم الاستيراد السنوي." style="padding:8px 10px;background:rgba(29,78,216,.1);border:1px solid rgba(29,78,216,.3);border-radius:9px;color:#93c5fd;font-size:12px;font-weight:700;font-family:'Cairo',Arial,sans-serif;cursor:pointer;text-align:right;line-height:1.5;transition:border-color .15s;" onmouseover="this.style.borderColor='rgba(59,130,246,.7)'" onmouseout="this.style.borderColor='rgba(29,78,216,.3)'">🏢 أهم المستوردين والموزعين</button>
          <button type="button" onclick="setQ(this)" data-q="ما هي الرسوم الجمركية الدقيقة ومتطلبات الدخول الكاملة للسوق الأوروبي لهذا المنتج؟ وهل هناك اتفاقيات تفضيلية مع مصر؟" style="padding:8px 10px;background:rgba(29,78,216,.1);border:1px solid rgba(29,78,216,.3);border-radius:9px;color:#93c5fd;font-size:12px;font-weight:700;font-family:'Cairo',Arial,sans-serif;cursor:pointer;text-align:right;line-height:1.5;transition:border-color .15s;" onmouseover="this.style.borderColor='rgba(59,130,246,.7)'" onmouseout="this.style.borderColor='rgba(29,78,216,.3)'">⚖️ الرسوم الجمركية والاتفاقيات</button>
          <button type="button" onclick="setQ(this)" data-q="ما هي متطلبات السلامة الغذائية الأوروبية الكاملة لهذا المنتج؟ شهادات الجودة، معايير التغليف والوسم، ومتطلبات المبيدات والمواد الحافظة." style="padding:8px 10px;background:rgba(16,185,129,.08);border:1px solid rgba(16,185,129,.25);border-radius:9px;color:#6ee7b7;font-size:12px;font-weight:700;font-family:'Cairo',Arial,sans-serif;cursor:pointer;text-align:right;line-height:1.5;transition:border-color .15s;" onmouseover="this.style.borderColor='rgba(16,185,129,.6)'" onmouseout="this.style.borderColor='rgba(16,185,129,.25)'">🥗 السلامة الغذائية والشهادات</button>
          <button type="button" onclick="setQ(this)" data-q="حلل المنافسين الرئيسيين لمصر في هذا السوق: من هم؟ ما أسعارهم؟ ما نقاط ضعفهم؟ وأين الفرصة التنافسية للمنتج المصري؟" style="padding:8px 10px;background:rgba(16,185,129,.08);border:1px solid rgba(16,185,129,.25);border-radius:9px;color:#6ee7b7;font-size:12px;font-weight:700;font-family:'Cairo',Arial,sans-serif;cursor:pointer;text-align:right;line-height:1.5;transition:border-color .15s;" onmouseover="this.style.borderColor='rgba(16,185,129,.6)'" onmouseout="this.style.borderColor='rgba(16,185,129,.25)'">📊 تحليل المنافسين والتموضع</button>
          <button type="button" onclick="setQ(this)" data-q="ما هي استراتيجية التسعير المثلى للمنتج المصري في هذا السوق؟ حلل أسعار المنافسين، هامش الربح المتوقع، وتكاليف الشحن واللوجستيات." style="padding:8px 10px;background:rgba(245,158,11,.08);border:1px solid rgba(245,158,11,.25);border-radius:9px;color:#fcd34d;font-size:12px;font-weight:700;font-family:'Cairo',Arial,sans-serif;cursor:pointer;text-align:right;line-height:1.5;transition:border-color .15s;" onmouseover="this.style.borderColor='rgba(245,158,11,.6)'" onmouseout="this.style.borderColor='rgba(245,158,11,.25)'">💰 استراتيجية التسعير والربحية</button>
          <button type="button" onclick="setQ(this)" data-q="ما هي أفضل قنوات التوزيع والدخول للسوق؟ هل عبر وسيط، أو مباشر لسلاسل التجزئة، أو عبر منصات B2B؟ مع أمثلة على شركات ناجحة." style="padding:8px 10px;background:rgba(245,158,11,.08);border:1px solid rgba(245,158,11,.25);border-radius:9px;color:#fcd34d;font-size:12px;font-weight:700;font-family:'Cairo',Arial,sans-serif;cursor:pointer;text-align:right;line-height:1.5;transition:border-color .15s;" onmouseover="this.style.borderColor='rgba(245,158,11,.6)'" onmouseout="this.style.borderColor='rgba(245,158,11,.25)'">🚀 قنوات التوزيع واستراتيجية الدخول</button>
        </div>
        <textarea id="userQuestion" placeholder="اكتب سؤالك المخصص أو اختر أحد الأسئلة أعلاه..." style="min-height:75px;resize:vertical;font-size:13px;"></textarea>
        <script>
          function setQ(btn){
            document.getElementById("userQuestion").value = btn.getAttribute("data-q");
            document.querySelectorAll("[data-q]").forEach(b=>b.style.background=b.style.background.replace(".3)",",.1)"));
            btn.style.borderColor = btn.style.borderColor.replace(".25)",".7)");
          }
        </script>"""

if old in html:
    html = html.replace(old, new, 1)
    open("WissamXpoHub_V3_Frontend_FIXED.html", "w", encoding="utf-8").write(html)
    print("OK - strategic questions added")
else:
    print("Not found")
    idx = html.find("userQuestion")
    print("userQuestion at:", idx)
