content = open('WissamXpoHub_V3_Frontend_FIXED.html', encoding='utf-8').read()

# Remove any existing upgrade modal first
import re
content = re.sub(r'\s*<!-- Upgrade Modal -->.*?</script>', '', content, flags=re.DOTALL)

# Add correctly before real </body>
upgrade = '''
  <!-- Upgrade Modal -->
  <div id="upgradeModal" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,.85);z-index:99999;justify-content:center;align-items:center;">
    <div style="background:#1e1b4b;border:1px solid rgba(99,102,241,.4);border-radius:20px;padding:32px;max-width:500px;width:92%;font-family:Cairo,Arial,sans-serif;direction:rtl;text-align:center;">
      <div style="font-size:28px;margin-bottom:8px">upgrade</div>
      <div style="font-size:20px;font-weight:800;color:white;margin-bottom:6px">ترقية باقتك</div>
      <div style="font-size:13px;color:#9ca3af;margin-bottom:24px" id="upgradeModalMsg">اختر الباقة للاستمرار</div>
      <div style="display:grid;gap:10px;margin-bottom:20px">
        <div onclick="selectUpgradePlan(this,'Starter','299')" style="cursor:pointer;padding:14px;border-radius:12px;background:rgba(99,102,241,.1);border:1px solid rgba(99,102,241,.3);text-align:right">
          <div style="font-weight:800;color:#a5b4fc">Starter</div>
          <div style="color:#6b7280;font-size:12px">5 تقارير + Blog + Scanner</div>
          <div style="font-size:18px;font-weight:800;color:white">299 ج.م / شهر</div>
        </div>
        <div onclick="selectUpgradePlan(this,'Pro','599')" style="cursor:pointer;padding:14px;border-radius:12px;background:rgba(139,92,246,.15);border:2px solid rgba(139,92,246,.5);text-align:right">
          <div style="font-weight:800;color:#c4b5fd">Pro - الاكثر طلبا</div>
          <div style="color:#6b7280;font-size:12px">25 تقرير + كل الميزات + Buyers</div>
          <div style="font-size:18px;font-weight:800;color:white">599 ج.م / شهر</div>
        </div>
        <div onclick="selectUpgradePlan(this,'Agency','1490')" style="cursor:pointer;padding:14px;border-radius:12px;background:rgba(245,158,11,.1);border:1px solid rgba(245,158,11,.3);text-align:right">
          <div style="font-weight:800;color:#fcd34d">Agency</div>
          <div style="color:#6b7280;font-size:12px">100 تقرير + كل الميزات</div>
          <div style="font-size:18px;font-weight:800;color:white">1,490 ج.م / شهر</div>
        </div>
      </div>
      <a id="upgradeWaLink" href="https://wa.me/201116415272" target="_blank" style="display:block;background:linear-gradient(135deg,#25d366,#128c7e);color:white;padding:13px 28px;border-radius:50px;text-decoration:none;font-weight:700;font-size:15px;margin-bottom:10px">اشترك الان عبر واتساب</a>
      <button onclick="document.getElementById('upgradeModal').style.display='none'" style="background:rgba(255,255,255,.08);border:none;color:#9ca3af;padding:10px 24px;border-radius:10px;cursor:pointer;font-family:Cairo,Arial,sans-serif;font-size:13px">اغلاق</button>
    </div>
  </div>
  <script>
  function showUpgradeModal(msg) {
    var m = document.getElementById('upgradeModal');
    var msgEl = document.getElementById('upgradeModalMsg');
    if(msgEl && msg) msgEl.textContent = msg;
    if(m) m.style.display = 'flex';
  }
  function selectUpgradePlan(el, plan, price) {
    var email = localStorage.getItem('wx_user_email') || '';
    var used  = localStorage.getItem('wx_plan_used') || '0';
    var limit = localStorage.getItem('wx_plan_limit') || '1';
    var msg = 'مرحبا، اريد الاشتراك في باقة ' + plan + ' (' + price + ' جم/شهر) - بريدي: ' + email + ' - استخدمت: ' + used + '/' + limit;
    var link = document.getElementById('upgradeWaLink');
    if(link) link.href = 'https://wa.me/201116415272?text=' + encodeURIComponent(msg);
  }
  </script>'''

# Insert before real last </body>
real_body = content.rfind('\n</body>')
content = content[:real_body] + upgrade + content[real_body:]

open('WissamXpoHub_V3_Frontend_FIXED.html', 'w', encoding='utf-8').write(content)
print('Done - upgrade modal added correctly')
