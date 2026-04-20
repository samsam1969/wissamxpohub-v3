content = open('Blog.html', encoding='utf-8').read()

# Remove old lock script
import re
content = re.sub(r'<script>\s*\(function\(\) \{[\s\S]*?\}\)\(\);\s*</script>', '', content, count=1)

# Add new clean lock
lock = '''<script>
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

content = content.replace('<head>', '<head>\n' + lock, 1)
open('Blog.html', 'w', encoding='utf-8').write(content)
print('Done - Blog lock fixed')
