content = open('WissamXpoHub_V3_Frontend_FIXED.html', encoding='utf-8').read()

old_steps = '''        <!-- خطوات الاستخدام -->
        <div class="mini" style="background:rgba(16,185,129,.05);border:1px solid rgba(16,185,129,.18);border-radius:10px;padding:12px 16px;margin-bottom:10px;">
          <b style="color:#6ee7b7;font-size:13px;">🚀 خطوات الاستخدام بالترتيب</b>'''

new_steps = '''        <!-- خطوات الاستخدام -->
        <div class="mini" style="background:rgba(16,185,129,.05);border:1px solid rgba(16,185,129,.18);border-radius:10px;padding:12px 16px;margin-bottom:10px;">
          <b style="color:#6ee7b7;font-size:13px;">🚀 كيف تبدأ — 4 خطوات فقط</b>'''

content = content.replace(old_steps, new_steps, 1)

# Update step texts
steps = [
    ('سجّل الدخول:', 'اضغط Login أو سجّل حساباً جديداً مجاناً — تقرير واحد مجاني كل شهر'),
    ('احفظ الإعدادات:', 'أدخل عنوان الباك إند (Backend URL) واضغط Save Settings'),
    ('أدخل المنتج:', 'اكتب اسم المنتج أو كود HS مثل 080410 للتمور أو 081110 للفراولة المجمدة'),
    ('اختر السوق:', 'حدد دولة الاتحاد الأوروبي المستهدفة — 24 دولة متاحة'),
    ('شغّل التحليل:', 'اضغط Run Export Intelligence — التقرير يستغرق 30-60 ثانية'),
    ('راجع النتائج:', 'تقرير كامل بالبيانات والأسعار والمتطلبات والمستوردين المحتملين'),
    ('صدّر التقرير:', 'احفظ التقرير بصيغة PDF أو انسخه للمشاركة'),
    ('أنشئ رسالة:', 'استخدم Potential Buyers للتواصل المباشر مع المستوردين الأوروبيين'),
]

for title, desc in steps:
    old = f'<span style="font-weight:700;color:var(--text);font-size:12px;">{title}</span> <span style="color:var(--muted);font-size:12px;">'
    # just update description
    
# Replace old notes section and add plans
old_notes = '''        <!-- ملاحظات مهمة -->
        <div class="mini" style="background:rgba(239,68,68,.05);border:1px solid rgba(239,68,68,.15);border-radius:10px;padding:12px 16px;">
          <b style="color:#fca5a5;font-size:13px;">⚠️ ملاحظات مهمة</b>
          <div style="margin-top:7px;display:flex;flex-direction:column;gap:5px;">
            <div style="font-size:12px;color:var(--muted);">• تأكد من صحة اسم المنتج أو كود HS قبل تشغيل التحليل للحصول على نتائج دقيقة</div>
            <div style="font-size:12px;color:var(--muted);">• النتائج والتوصيات مساعِدة في اتخاذ القرار، وليست بديلاً عن البحث الميداني</div>
            <div style="font-size:12px;color:var(--muted);">• راجع السوق المستهدف والمنافسين قبل التواصل المباشر مع المشترين</div>
            <div style="font-size:12px;color:var(--muted);">• تأكد من تشغيل الباك إند قبل استخدام أي أداة تحليل</div>
          </div>
        </div>'''

new_notes = '''        <!-- الباقات -->
        <div class="mini" style="background:rgba(99,102,241,.06);border:1px solid rgba(99,102,241,.2);border-radius:10px;padding:12px 16px;margin-bottom:10px;">
          <b style="color:#a5b4fc;font-size:13px;">💎 باقات الاشتراك</b>
          <div style="margin-top:10px;display:flex;flex-direction:column;gap:8px;">
            <div style="background:rgba(107,114,128,.1);border-radius:8px;padding:10px 12px;">
              <div style="display:flex;justify-content:space-between;align-items:center;">
                <span style="color:#9ca3af;font-weight:800;font-size:12px;">🆓 مجاني</span>
                <span style="color:#6b7280;font-size:11px;">0 ج.م</span>
              </div>
              <div style="color:#6b7280;font-size:11px;margin-top:3px;">تقرير واحد شهرياً — للتجربة</div>
            </div>
            <div style="background:rgba(99,102,241,.1);border:1px solid rgba(99,102,241,.3);border-radius:8px;padding:10px 12px;">
              <div style="display:flex;justify-content:space-between;align-items:center;">
                <span style="color:#a5b4fc;font-weight:800;font-size:12px;">🥉 Starter</span>
                <span style="color:#a5b4fc;font-size:12px;font-weight:800;">299 ج.م / شهر</span>
              </div>
              <div style="color:#6b7280;font-size:11px;margin-top:3px;">5 تقارير + Blog + Scanner</div>
            </div>
            <div style="background:rgba(139,92,246,.12);border:2px solid rgba(139,92,246,.4);border-radius:8px;padding:10px 12px;">
              <div style="display:flex;justify-content:space-between;align-items:center;">
                <span style="color:#c4b5fd;font-weight:800;font-size:12px;">🥈 Pro ⭐ الأشهر</span>
                <span style="color:#c4b5fd;font-size:12px;font-weight:800;">599 ج.م / شهر</span>
              </div>
              <div style="color:#6b7280;font-size:11px;margin-top:3px;">25 تقرير + كل الميزات + Buyers</div>
            </div>
            <div style="background:rgba(245,158,11,.08);border:1px solid rgba(245,158,11,.25);border-radius:8px;padding:10px 12px;">
              <div style="display:flex;justify-content:space-between;align-items:center;">
                <span style="color:#fcd34d;font-weight:800;font-size:12px;">🥇 Agency</span>
                <span style="color:#fcd34d;font-size:12px;font-weight:800;">1,490 ج.م / شهر</span>
              </div>
              <div style="color:#6b7280;font-size:11px;margin-top:3px;">100 تقرير + كل الميزات + أولوية الدعم</div>
            </div>
            <button onclick="showUpgradeModal()" style="width:100%;background:linear-gradient(135deg,#25d366,#128c7e);color:white;border:none;padding:10px;border-radius:8px;font-family:Cairo,Arial,sans-serif;font-weight:700;font-size:13px;cursor:pointer;margin-top:4px;">📱 اشترك عبر واتساب</button>
          </div>
        </div>

        <!-- ملاحظات مهمة -->
        <div class="mini" style="background:rgba(239,68,68,.05);border:1px solid rgba(239,68,68,.15);border-radius:10px;padding:12px 16px;">
          <b style="color:#fca5a5;font-size:13px;">⚠️ ملاحظات مهمة</b>
          <div style="margin-top:7px;display:flex;flex-direction:column;gap:5px;">
            <div style="font-size:12px;color:var(--muted);">• أدخل كود HS الصحيح للحصول على بيانات دقيقة — مثال: 080410 للتمور</div>
            <div style="font-size:12px;color:var(--muted);">• التقارير مساعِدة في اتخاذ القرار وليست بديلاً عن البحث الميداني</div>
            <div style="font-size:12px;color:var(--muted);">• بيانات 2020-2024 من مصادر رسمية — 2025 من Tavily Web Intelligence</div>
            <div style="font-size:12px;color:var(--muted);">• للدعم والاستفسار: <a href="https://wa.me/201116415272" target="_blank" style="color:#25d366;">واتساب 201116415272+</a></div>
          </div>
        </div>'''

content = content.replace(old_notes, new_notes, 1)
open('WissamXpoHub_V3_Frontend_FIXED.html', 'w', encoding='utf-8').write(content)
print('Done - guide updated with plans')
