import re

content = open('WissamXpoHub_V3_Frontend_FIXED.html', encoding='utf-8').read()

# شريط الرصيد - يُضاف بعد عرض بيانات المستخدم
plan_bar = '''
  <!-- Plan Bar -->
  <div id="planBar" style="display:none;margin:8px 0;padding:10px 16px;border-radius:12px;background:rgba(99,102,241,.1);border:1px solid rgba(99,102,241,.3);font-family:'Cairo',Arial,sans-serif;direction:rtl;">
    <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">
      <div style="font-size:13px;color:#a5b4fc;font-weight:700;">
        <span id="planName">Starter</span> 
        <span style="color:#6b7280;font-weight:400;margin:0 6px;">|</span>
        <span id="planUsed">0</span> / <span id="planLimit">5</span> تقارير
      </div>
      <div style="flex:1;max-width:200px;height:6px;background:rgba(255,255,255,.1);border-radius:99px;overflow:hidden;">
        <div id="planProgress" style="height:100%;background:linear-gradient(90deg,#6366f1,#8b5cf6);border-radius:99px;transition:width .4s;width:0%"></div>
      </div>
      <button onclick="showUpgradeModal()" style="font-size:12px;padding:5px 12px;border-radius:8px;background:linear-gradient(135deg,#6366f1,#8b5cf6);border:none;color:white;font-weight:700;cursor:pointer;font-family:'Cairo',Arial,sans-serif;">⬆️ ترقية</button>
    </div>
  </div>

  <!-- Upgrade Modal -->
  <div id="upgradeModal" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,.7);z-index:9999;justify-content:center;align-items:center;">
    <div style="background:#1e1b4b;border:1px solid rgba(99,102,241,.4);border-radius:20px;padding:32px;max-width:480px;width:90%;font-family:'Cairo',Arial,sans-serif;direction:rtl;text-align:center;">
      <div style="font-size:22px;font-weight:800;color:white;margin-bottom:8px;">🚀 ترقية باقتك</div>
      <div style="font-size:14px;color:#9ca3af;margin-bottom:24px;">اختر الباقة المناسبة لك</div>
      <div style="display:grid;gap:12px;margin-bottom:24px;">
        <div style="padding:16px;border-radius:12px;background:rgba(99,102,241,.1);border:1px solid rgba(99,102,241,.3);text-align:right;">
          <div style="font-weight:800;color:#a5b4fc;">🥉 Starter</div>
          <div style="color:#6b7280;font-size:13px;">5 تقارير / شهر</div>
          <div style="font-size:20px;font-weight:800;color:white;margin-top:4px;">299 ج.م / شهر</div>
        </div>
        <div style="padding:16px;border-radius:12px;background:rgba(139,92,246,.15);border:2px solid rgba(139,92,246,.5);text-align:right;">
          <div style="font-weight:800;color:#c4b5fd;">🥈 Pro ⭐ الأكثر طلباً</div>
          <div style="color:#6b7280;font-size:13px;">25 تقرير / شهر</div>
          <div style="font-size:20px;font-weight:800;color:white;margin-top:4px;">599 ج.م / شهر</div>
        </div>
        <div style="padding:16px;border-radius:12px;background:rgba(245,158,11,.1);border:1px solid rgba(245,158,11,.3);text-align:right;">
          <div style="font-weight:800;color:#fcd34d;">🥇 Agency</div>
          <div style="color:#6b7280;font-size:13px;">100 تقرير / شهر</div>
          <div style="font-size:20px;font-weight:800;color:white;margin-top:4px;">1,490 ج.م / شهر</div>
        </div>
      </div>
      <div style="font-size:12px;color:#6b7280;margin-bottom:16px;">للاشتراك تواصل معنا عبر واتساب</div>
      <div style="display:flex;gap:10px;justify-content:center;">
        <a href="https://wa.me/201XXXXXXXXX" target="_blank" style="padding:10px 24px;background:linear-gradient(135deg,#6366f1,#8b5cf6);color:white;border-radius:10px;font-weight:700;text-decoration:none;font-size:14px;">📱 تواصل معنا</a>
        <button onclick="document.getElementById('upgradeModal').style.display='none'" style="padding:10px 24px;background:rgba(255,255,255,.1);color:white;border:none;border-radius:10px;font-weight:700;cursor:pointer;font-size:14px;">إغلاق</button>
      </div>
    </div>
  </div>

  <script>
  function showUpgradeModal() {
    document.getElementById('upgradeModal').style.display = 'flex';
  }
  function updatePlanBar(used, limit, planType) {
    const bar = document.getElementById('planBar');
    if (!bar) return;
    bar.style.display = 'block';
    document.getElementById('planUsed').textContent = used;
    document.getElementById('planLimit').textContent = limit;
    document.getElementById('planName').textContent = 
      planType === 'starter' ? '🥉 Starter' :
      planType === 'pro' ? '🥈 Pro' : '🥇 Agency';
    const pct = Math.min((used/limit)*100, 100);
    document.getElementById('planProgress').style.width = pct + '%';
    document.getElementById('planProgress').style.background = 
      pct >= 90 ? 'linear-gradient(90deg,#ef4444,#dc2626)' :
      pct >= 70 ? 'linear-gradient(90deg,#f59e0b,#d97706)' :
      'linear-gradient(90deg,#6366f1,#8b5cf6)';
  }
  </script>
'''

# أضف بعد <body> مباشرة
content = content.replace('<body>', '<body>\n' + plan_bar, 1)

open('WissamXpoHub_V3_Frontend_FIXED.html', 'w', encoding='utf-8').write(content)
print('Done - plan bar added')
