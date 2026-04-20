content = open('WissamXpoHub_V3_Frontend_FIXED.html', encoding='utf-8').read()

old = '''        <div class="badge-row">
          <div class="badge" id="dashBadge">Dashboard Mode</div>
          <div class="badge">Supabase Auth</div>
          <div class="badge">AI + Sources</div>'''

new = '''        <div class="badge-row">
          <div class="badge" id="dashBadge">Dashboard Mode</div>
          <div class="badge">Supabase Auth</div>
          <div class="badge">AI + Sources</div>
          <div class="badge" id="adminLinks" style="display:none">
            <a href="/admin/crm" style="color:#a5b4fc;text-decoration:none;margin-left:8px">👥 CRM</a>
            <a href="/admin/knowledge" style="color:#fcd34d;text-decoration:none">🧠 KB</a>
          </div>'''

content = content.replace(old, new, 1)

# Show admin links only for admin email
old2 = '  setTimeout(function() {\n    var type = localStorage.getItem("wx_plan_type") || "free";\n    if (type === "free") showFreeTrialEndedBanner();\n  }, 5000);'

new2 = '''  setTimeout(function() {
    var type = localStorage.getItem("wx_plan_type") || "free";
    if (type === "free") showFreeTrialEndedBanner();
    // Show admin links
    var email = localStorage.getItem("wx_user_email") || "";
    if (email === "wissamxpo@outlook.com") {
      var al = document.getElementById("adminLinks");
      if(al) al.style.display = "inline-flex";
    }
  }, 2500);'''

content = content.replace(old2, new2, 1)
open('WissamXpoHub_V3_Frontend_FIXED.html', 'w', encoding='utf-8').write(content)
print('Done - admin links added')
