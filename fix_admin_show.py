content = open('WissamXpoHub_V3_Frontend_FIXED.html', encoding='utf-8').read()

old = '        if(userEmail === "wissamxpo@outlook.com"){'
new = '        if(userEmail === "wissamxpo@outlook.com" || userEmail === "wissamxpo@outlook.com".toLowerCase()){'

content = content.replace(old, new, 1)

# Also try immediate check on page load
old2 = '  // Apply on load\n  document.addEventListener("DOMContentLoaded", function() {\n    setTimeout(function() { applyLanguage(LANG); }, 500);\n  });'

new2 = '''  // Apply on load
  document.addEventListener("DOMContentLoaded", function() {
    setTimeout(function() { applyLanguage(LANG); }, 500);
    // Check admin immediately
    setTimeout(function() {
      try {
        var tok2 = null;
        var ks2 = Object.keys(localStorage);
        for(var ki2=0; ki2<ks2.length; ki2++){
          var kv2 = localStorage.getItem(ks2[ki2]);
          if(kv2 && kv2.startsWith("eyJ")){ tok2 = kv2; break; }
          try{ var kp2=JSON.parse(kv2); if(kp2&&kp2.access_token){ tok2=kp2.access_token; break; }}catch(e){}
        }
        if(tok2){
          var pay2 = JSON.parse(atob(tok2.split(".")[1]));
          if(pay2.email === "wissamxpo@outlook.com"){
            var al2 = document.getElementById("adminLinks");
            if(al2) al2.style.display = "inline-flex";
          }
        }
      } catch(e){ console.log("admin check error:", e); }
    }, 1000);
  });'''

content = content.replace(old2, new2, 1)
open('WissamXpoHub_V3_Frontend_FIXED.html', 'w', encoding='utf-8').write(content)
print('Done')
