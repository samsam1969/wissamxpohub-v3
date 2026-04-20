content = open('Blog.html', encoding='utf-8').read()

old = '''  // Verify plan from backend
  var backendUrl = localStorage.getItem("wx_backend_url") || "http://localhost:4000";
  fetch(backendUrl + "/api/auth/my-plan", {
    headers: {"Authorization": "Bearer " + token}
  }).then(function(r){ return r.json(); }).then(function(d){
    var planType = d.plan_type || "free";
    localStorage.setItem("wx_plan_type", planType);
    var allowed = ["starter","pro","agency"];
    if(allowed.indexOf(planType) === -1) showLock(true);'''

new = '''  // Verify from backend ONLY - no localStorage fallback
  var backendUrl = localStorage.getItem("wx_backend_url") || "http://localhost:4000";
  fetch(backendUrl + "/api/auth/check-feature/blog", {
    headers: {"Authorization": "Bearer " + token}
  }).then(function(r){ return r.json(); }).then(function(d){
    localStorage.setItem("wx_plan_type", d.plan_type || "free");
    if(!d.allowed) showLock(true);'''

content = content.replace(old, new, 1)
open('Blog.html', 'w', encoding='utf-8').write(content)
print('Done - Blog uses check-feature')
