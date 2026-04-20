content = open('WissamXpoHub_V3_Frontend_FIXED.html', encoding='utf-8').read()

old_guide = '''          <h2>🧭 دليل الاستخدام</h2>
          <h3>كيف تستخدم منصة WissamXpoHub خطوة بخطوة</h3>
        </div>'''

new_guide = '''          <h2>🧭 دليل الاستخدام</h2>
          <h3>منصة الذكاء التصديري المصري نحو أوروبا</h3>
        </div>'''

content = content.replace(old_guide, new_guide, 1)

# Replace the entire guide content
old_content = '''        <!-- نبذة عن المنصة -->
        <div class="mini" style="background:rgba(59,130,246,.06);border:1px solid rgba(59,130,246,.2);border-radius:10px;padding:12px 16px;margin-bottom:10px;">
          <b style="color:#93c5fd;font-size:13px;">📌 ما هذه المنصة؟</b>
          <div style="margin-top:6px;font-size:13px;line-height:1.8;color:var(--text);">
            WissamXpoHub منصة ذكاء تصديري مدعومة بالذكاء الاصطناعي، مصمّمة للمصدّرين المصريين الراغبين في استكشاف الأسواق الأوروبية. تساعدك على تحليل فرص التصدير، فهم الأسواق المستهدفة، والتواصل مع المشترين المحتملين.
          </div>
        </div>'''

new_content = '''        <!-- نبذة عن المنصة -->
        <div class="mini" style="background:rgba(59,130,246,.06);border:1px solid rgba(59,130,246,.2);border-radius:10px;padding:12px 16px;margin-bottom:10px;">
          <b style="color:#93c5fd;font-size:13px;">📌 ما هي WissamXpoHub؟</b>
          <div style="margin-top:6px;font-size:13px;line-height:1.9;color:var(--text);">
            منصة ذكاء تصديري مدعومة بالذكاء الاصطناعي، مصمّمة خصيصاً للمصدّرين المصريين الراغبين في دخول الأسواق الأوروبية. تجمع بيانات التجارة الدولية (UN Comtrade، ITC TradeMap، Tavily 2025) مع تحليل Claude AI لإنتاج تقارير تصديرية احترافية في دقائق.
          </div>
        </div>'''

content = content.replace(old_content, new_content, 1)

open('WissamXpoHub_V3_Frontend_FIXED.html', 'w', encoding='utf-8').write(content)
print('Step 1 done')
