content = open('WissamXpoHub_V3_Frontend_FIXED.html', encoding='utf-8').read()

old = '          <div class="badge" id="adminLinks" style="display:none">\n            <a href="/admin/crm" style="color:#a5b4fc;text-decoration:none;margin-left:8px">👥 CRM</a>\n            <a href="/admin/knowledge" style="color:#fcd34d;text-decoration:none">🧠 KB</a>\n          </div>'

new = '''          <div id="adminLinks" style="display:none;gap:6px;align-items:center">
            <a href="/admin/crm" style="background:rgba(99,102,241,.2);border:1px solid rgba(99,102,241,.4);color:#a5b4fc;text-decoration:none;padding:4px 10px;border-radius:8px;font-size:12px;font-weight:700">👥 CRM</a>
            <a href="/admin/knowledge" style="background:rgba(245,158,11,.15);border:1px solid rgba(245,158,11,.3);color:#fcd34d;text-decoration:none;padding:4px 10px;border-radius:8px;font-size:12px;font-weight:700">🧠 KB</a>
          </div>'''

content = content.replace(old, new, 1)

# Fix the show logic - check token email directly
old2 = '''    // Show admin links
    var email = localStorage.getItem("wx_user_email") || "";
    if (email === "wissamxpo@outlook.com") {
      var al = document.getElementById("adminLinks");
      if(al) al.style.display = "inline-flex";
    }'''

new2 = '''    // Show admin links - check from token
    try {
      var tok = null;
      var ks = Object.keys(localStorage);
      for(var ki=0; ki<ks.length; ki++){
        var kv = localStorage.getItem(ks[ki]);
        if(kv && kv.startsWith("eyJ")){ tok = kv; break; }
        try{ var kp=JSON.parse(kv); if(kp&&kp.access_token){ tok=kp.access_token; break; }}catch(e){}
      }
      if(tok){
        var payload = JSON.parse(atob(tok.split(".")[1]));
        var userEmail = payload.email || "";
        if(userEmail === "wissamxpo@outlook.com"){
          var al = document.getElementById("adminLinks");
          if(al) al.style.display = "inline-flex";
        }
      }
    } catch(e){}'''

content = content.replace(old2, new2, 1)
open('WissamXpoHub_V3_Frontend_FIXED.html', 'w', encoding='utf-8').write(content)
print('Done')
