content = open('Blog.html', encoding='utf-8').read()

lock_script = '''
<script>
(function() {
  var token = null;
  var keys = Object.keys(localStorage);
  for (var i = 0; i < keys.length; i++) {
    var v = localStorage.getItem(keys[i]);
    if (v && v.startsWith('eyJ')) { token = v; break; }
    try { var p = JSON.parse(v); if (p && p.access_token) { token = p.access_token; break; } } catch(e) {}
  }

  if (!token) {
    document.body.innerHTML = '<div style="display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:100vh;background:#0f0e17;font-family:Cairo,Arial,sans-serif;text-align:center;padding:24px">' +
      '<div style="font-size:48px;margin-bottom:16px">🔒</div>' +
      '<h2 style="color:#a5b4fc;font-size:24px;margin-bottom:12px">المدونة للمشتركين فقط</h2>' +
      '<p style="color:#6b7280;margin-bottom:24px;max-width:400px">اشترك في إحدى الباقات للوصول لكل المقالات والأخبار التصديرية</p>' +
      '<div style="display:flex;gap:12px;flex-wrap:wrap;justify-content:center;margin-bottom:24px">' +
        '<div style="background:rgba(99,102,241,.1);border:1px solid rgba(99,102,241,.3);border-radius:12px;padding:16px 24px;color:white">' +
          '<div style="font-weight:800;color:#a5b4fc">🥉 Starter</div>' +
          '<div style="color:#6b7280;font-size:13px">5 تقارير/شهر</div>' +
          '<div style="font-size:20px;font-weight:800;margin-top:4px">299 ج.م</div>' +
        '</div>' +
        '<div style="background:rgba(139,92,246,.15);border:2px solid rgba(139,92,246,.5);border-radius:12px;padding:16px 24px;color:white">' +
          '<div style="font-weight:800;color:#c4b5fd">🥈 Pro</div>' +
          '<div style="color:#6b7280;font-size:13px">25 تقرير/شهر</div>' +
          '<div style="font-size:20px;font-weight:800;margin-top:4px">599 ج.م</div>' +
        '</div>' +
      '</div>' +
      '<a href="https://wa.me/201116415272?text=' + encodeURIComponent('مرحباً، أريد الاشتراك في WissamXpoHub') + '" target="_blank" ' +
        'style="background:linear-gradient(135deg,#25d366,#128c7e);color:white;padding:14px 32px;border-radius:50px;text-decoration:none;font-weight:700;font-size:16px;margin-bottom:16px">📱 اشترك عبر واتساب</a>' +
      '<a href="/" style="color:#6b7280;font-size:13px">← العودة للداشبورد</a>' +
    '</div>';
    return;
  }

  try {
    var payload = JSON.parse(atob(token.split(".")[1]));
    var planType = localStorage.getItem("wx_plan_type") || "free";
    var allowedPlans = ["starter", "pro", "agency"];
    if (allowedPlans.indexOf(planType) === -1) {
      document.body.innerHTML = document.body.innerHTML;
      var overlay = document.createElement("div");
      overlay.style.cssText = "position:fixed;inset:0;background:rgba(15,14,23,.95);z-index:9999;display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:Cairo,Arial,sans-serif;text-align:center;padding:24px";
      overlay.innerHTML = '<div style="font-size:48px;margin-bottom:16px">🔒</div>' +
        '<h2 style="color:#a5b4fc;font-size:24px;margin-bottom:12px">المدونة للمشتركين فقط</h2>' +
        '<p style="color:#9ca3af;margin-bottom:24px">باقتك الحالية (Free) لا تشمل الوصول للمدونة</p>' +
        '<a href="https://wa.me/201116415272?text=' + encodeURIComponent('مرحباً، أريد ترقية باقتي للوصول للمدونة') + '" target="_blank" ' +
          'style="background:linear-gradient(135deg,#25d366,#128c7e);color:white;padding:12px 28px;border-radius:50px;text-decoration:none;font-weight:700;margin-bottom:12px;display:inline-block">📱 ترقية للوصول</a><br/>' +
        '<a href="/" style="color:#6b7280;font-size:13px">← العودة</a>';
      document.body.appendChild(overlay);
    }
  } catch(e) {}
})();
</script>
'''

content = content.replace('<head>', '<head>\n' + lock_script, 1)
open('Blog.html', 'w', encoding='utf-8').write(content)
print('Done - Blog locked for free users')
