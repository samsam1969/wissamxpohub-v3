content = open('WissamXpoHub_V3_Frontend_FIXED.html', encoding='utf-8').read()

# Add Upgrade Modal with all 3 plans
upgrade_modal = '''
  <!-- Upgrade Modal -->
  <div id="upgradeModal" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,.85);z-index:99999;justify-content:center;align-items:center;">
    <div style="background:#1e1b4b;border:1px solid rgba(99,102,241,.4);border-radius:20px;padding:32px;max-width:500px;width:92%;font-family:Cairo,Arial,sans-serif;direction:rtl;text-align:center;">
      <div style="font-size:28px;margin-bottom:8px">🚀</div>
      <div style="font-size:20px;font-weight:800;color:white;margin-bottom:6px">ترقية باقتك</div>
      <div style="font-size:13px;color:#9ca3af;margin-bottom:24px" id="upgradeModalMsg">اختر الباقة المناسبة للاستمرار</div>
      <div style="display:grid;gap:10px;margin-bottom:20px">
        <div onclick="selectUpgradePlan('Starter','299')" style="cursor:pointer;padding:14px 16px;border-radius:12px;background:rgba(99,102,241,.1);border:1px solid rgba(99,102,241,.3);text-align:right;transition:all .2s" onmouseover="this.style.background='rgba(99,102,241,.2)'" onmouseout="this.style.background='rgba(99,102,241,.1)'">
          <div style="font-weight:800;color:#a5b4fc;font-size:15px">🥉 Starter</div>
          <div style="color:#6b7280;font-size:12px;margin:2px 0">5 تقارير AI / شهر + Blog + Scanner</div>
          <div style="font-size:20px;font-weight:800;color:white">299 ج.م / شهر</div>
        </div>
        <div onclick="selectUpgradePlan('Pro','599')" style="cursor:pointer;padding:14px 16px;border-radius:12px;background:rgba(139,92,246,.15);border:2px solid rgba(139,92,246,.5);text-align:right" onmouseover="this.style.background='rgba(139,92,246,.25)'" onmouseout="this.style.background='rgba(139,92,246,.15)'">
          <div style="font-weight:800;color:#c4b5fd;font-size:15px">🥈 Pro ⭐ الأكثر طلباً</div>
          <div style="color:#6b7280;font-size:12px;margin:2px 0">25 تقرير AI / شهر + كل الميزات + Buyers</div>
          <div style="font-size:20px;font-weight:800;color:white">599 ج.م / شهر</div>
        </div>
        <div onclick="selectUpgradePlan('Agency','1490')" style="cursor:pointer;padding:14px 16px;border-radius:12px;background:rgba(245,158,11,.1);border:1px solid rgba(245,158,11,.3);text-align:right" onmouseover="this.style.background='rgba(245,158,11,.2)'" onmouseout="this.style.background='rgba(245,158,11,.1)'">
          <div style="font-weight:800;color:#fcd34d;font-size:15px">🥇 Agency</div>
          <div style="color:#6b7280;font-size:12px;margin:2px 0">100 تقرير AI / شهر + كل الميزات</div>
          <div style="font-size:20px;font-weight:800;color:white">1,490 ج.م / شهر</div>
        </div>
      </div>
      <a id="upgradeWaLink" href="https://wa.me/201116415272" target="_blank" style="display:block;background:linear-gradient(135deg,#25d366,#128c7e);color:white;padding:13px 28px;border-radius:50px;text-decoration:none;font-weight:700;font-size:15px;margin-bottom:10px">📱 اشترك الآن عبر واتساب</a>
      <button onclick="document.getElementById('upgradeModal').style.display='none'" style="background:rgba(255,255,255,.08);border:none;color:#9ca3af;padding:10px 24px;border-radius:10px;cursor:pointer;font-family:Cairo,Arial,sans-serif;font-size:13px">إغلاق</button>
    </div>
  </div>

  <script>
  function showUpgradeModal(msg) {
    var m = document.getElementById('upgradeModal');
    var msgEl = document.getElementById('upgradeModalMsg');
    if(msgEl && msg) msgEl.textContent = msg;
    if(m) m.style.display = 'flex';
  }

  function selectUpgradePlan(plan, price) {
    var email = localStorage.getItem('wx_user_email') || '';
    var used  = localStorage.getItem('wx_plan_used') || '0';
    var limit = localStorage.getItem('wx_plan_limit') || '1';
    var msg = 'مرحباً، أريد الاشتراك في باقة ' + plan + ' (' + price + ' ج.م/شهر)' +
              '\\nبريدي: ' + email +
              '\\nاستخدمت: ' + used + '/' + limit + ' تقارير';
    var link = document.getElementById('upgradeWaLink');
    if(link) link.href = 'https://wa.me/201116415272?text=' + encodeURIComponent(msg);
  }
  </script>
'''

content = content.replace('</body>', upgrade_modal + '\n</body>', 1)
open('WissamXpoHub_V3_Frontend_FIXED.html', 'w', encoding='utf-8').write(content)
print('Done - Upgrade modal added')
