content = open('Blog.html', encoding='utf-8').read()

old = '''<script>
(function(){
  // Check if user is logged in
  var token = null;
  var planType = "free";
  
  try {
    var keys = Object.keys(localStorage);
    for(var i=0; i<keys.length; i++){
      var v = localStorage.getItem(keys[i]);
      if(v && v.startsWith("eyJ")){ token = v; break; }
      try{ var p = JSON.parse(v); if(p && p.access_token && p.access_token.startsWith("eyJ")){ token = p.access_token; break; }} catch(e){}
    }
    planType = localStorage.getItem("wx_plan_type") || "free";
  } catch(e){}

  var allowedPlans = ["starter","pro","agency"];
  var isAllowed = token && allowedPlans.indexOf(planType) !== -1;

  if(!isAllowed){
    var msg = !token ? 
      "<h2 style=color:#a5b4fc>سجّل دخولك أولاً</h2><p style=color:#9ca3af;margin-bottom:20px>تحتاج حساباً للوصول للمدونة</p><a href=/ style=color:#a5b4fc>← العودة للداشبورد وتسجيل الدخول</a>" :
      "<h2 style=color:#a5b4fc>المدونة للمشتركين فقط</h2><p style=color:#9ca3af;margin-bottom:20px>باقتك الحالية (Free) لا تشمل الوصول للمدونة</p>";
    
    document.body.innerHTML = 
      "<div style='display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:100vh;background:#0f0e17;font-family:Cairo,Arial,sans-serif;text-align:center;padding:24px'>" +
      "<div style=font-size:64px;margin-bottom:16px>🔒</div>" + msg +
      "<br/><br/>" +
      "<a href='https://wa.me/201116415272?text=" + encodeURIComponent("مرحباً، أريد الاشتراك في WissamXpoHub") + "' target=_blank " +
      "style='display:inline-block;background:linear-gradient(135deg,#25d366,#128c7e);color:white;padding:12px 28px;border-radius:50px;text-decoration:none;font-weight:700;margin-top:16px'>📱 اشترك عبر واتساب</a>" +
      "</div>";
  }
})();
</script>'''

new = '''<script>
(function(){
  var token = null;
  try {
    var keys = Object.keys(localStorage);
    for(var i=0; i<keys.length; i++){
      var v = localStorage.getItem(keys[i]);
      if(v && v.startsWith("eyJ")){ token = v; break; }
      try{ var p = JSON.parse(v); if(p && p.access_token && p.access_token.startsWith("eyJ")){ token = p.access_token; break; }} catch(e){}
    }
  } catch(e){}

  function showLock(isLoggedIn) {
    var msg = !isLoggedIn ?
      "<h2 style=color:#a5b4fc;margin-bottom:12px>سجّل دخولك أولاً</h2><p style=color:#9ca3af;margin-bottom:20px>تحتاج حساباً للوصول للمدونة</p><a href='/' style='color:#a5b4fc;display:block;margin-bottom:20px'>← العودة للداشبورد</a>" :
      "<h2 style=color:#a5b4fc;margin-bottom:12px>المدونة للمشتركين فقط</h2><p style=color:#9ca3af;margin-bottom:20px>باقتك الحالية (Free) لا تشمل الوصول للمدونة</p>" +
      "<div style='display:flex;gap:12px;flex-wrap:wrap;justify-content:center;margin-bottom:20px'>" +
        "<div style='background:rgba(99,102,241,.1);border:1px solid rgba(99,102,241,.3);border-radius:12px;padding:16px 20px'><div style=color:#a5b4fc;font-weight:800>Starter</div><div style=color:#6b7280;font-size:13px>5 تقارير/شهر</div><div style=color:white;font-weight:800;font-size:18px>299 ج.م</div></div>" +
        "<div style='background:rgba(139,92,246,.15);border:2px solid rgba(139,92,246,.5);border-radius:12px;padding:16px 20px'><div style=color:#c4b5fd;font-weight:800>Pro ⭐</div><div style=color:#6b7280;font-size:13px>25 تقرير/شهر</div><div style=color:white;font-weight:800;font-size:18px>599 ج.م</div></div>" +
      "</div>";
    document.body.innerHTML =
      "<div style='display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:100vh;background:#0f0e17;font-family:Cairo,Arial,sans-serif;text-align:center;padding:24px'>" +
      "<div style=font-size:64px;margin-bottom:16px>🔒</div>" + msg +
      "<a href='https://wa.me/201116415272?text=" + encodeURIComponent("مرحباً، أريد الاشتراك في WissamXpoHub") + "' target=_blank style='display:inline-block;background:linear-gradient(135deg,#25d366,#128c7e);color:white;padding:12px 28px;border-radius:50px;text-decoration:none;font-weight:700'>📱 اشترك عبر واتساب</a>" +
      "</div>";
  }

  if(!token) { showLock(false); return; }

  // Verify plan from backend
  var backendUrl = localStorage.getItem("wx_backend_url") || "http://localhost:4000";
  fetch(backendUrl + "/api/auth/my-plan", {
    headers: {"Authorization": "Bearer " + token}
  }).then(function(r){ return r.json(); }).then(function(d){
    var planType = d.plan_type || "free";
    localStorage.setItem("wx_plan_type", planType);
    var allowed = ["starter","pro","agency"];
    if(allowed.indexOf(planType) === -1) showLock(true);
  }).catch(function(){
    // Fallback to localStorage
    var planType = localStorage.getItem("wx_plan_type") || "free";
    var allowed = ["starter","pro","agency"];
    if(allowed.indexOf(planType) === -1) showLock(true);
  });
})();
</script>'''

content = content.replace(old, new, 1)
open('Blog.html', 'w', encoding='utf-8').write(content)
print('Done - Blog lock uses backend verification')
