import re

for filename, feature, plan_needed in [
    ('PotentialBuyers.html', 'buyers', 'Pro'),
    ('ExportOpportunityScanner.html', 'scanner', 'Starter')
]:
    content = open(filename, encoding='utf-8').read()
    
    # Remove old lock
    content = re.sub(r'<script>\n\(function\(\)\{.*?\}\)\(\);\n</script>\n', '', content, flags=re.DOTALL, count=1)
    
    lock = f"""<script>
(function(){{
  var token = null;
  try {{
    var keys = Object.keys(localStorage);
    for(var i=0; i<keys.length; i++){{
      var v = localStorage.getItem(keys[i]);
      if(v && v.startsWith("eyJ")){{ token = v; break; }}
      try{{ var p = JSON.parse(v); if(p && p.access_token && p.access_token.startsWith("eyJ")){{ token = p.access_token; break; }}}} catch(e){{}}
    }}
  }} catch(e){{}}

  if(!token){{ window.location.href = '/WissamXpoHub_V3_Frontend_FIXED.html'; return; }}

  // Try multiple backend URLs
  var urls = [
    localStorage.getItem("wx_backend_url"),
    "http://localhost:4000",
    "http://127.0.0.1:4000"
  ].filter(Boolean);
  
  var url = urls[0] || "http://localhost:4000";

  function showLock(){{
    document.body.innerHTML =
      "<div style='display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:100vh;background:#0f0e17;font-family:Cairo,Arial,sans-serif;text-align:center;padding:24px'>" +
      "<div style='font-size:64px;margin-bottom:16px'>🔒</div>" +
      "<h2 style='color:#a5b4fc;margin-bottom:12px'>هذه الصفحة للمشتركين فقط</h2>" +
      "<p style='color:#9ca3af;margin-bottom:24px'>تتطلب باقة {plan_needed} أو أعلى</p>" +
      "<a href='https://wa.me/201116415272?text=" + encodeURIComponent("مرحباً، أريد الاشتراك في WissamXpoHub") + "' target='_blank' style='display:inline-block;background:linear-gradient(135deg,#25d366,#128c7e);color:white;padding:12px 28px;border-radius:50px;text-decoration:none;font-weight:700;margin-bottom:12px'>📱 اشترك عبر واتساب</a><br/>" +
      "<a href='/WissamXpoHub_V3_Frontend_FIXED.html' style='color:#6b7280;font-size:13px'>← العودة للداشبورد</a>" +
      "</div>";
  }}

  fetch(url + "/api/auth/check-feature/{feature}", {{
    headers: {{"Authorization": "Bearer " + token}}
  }}).then(function(r){{
    if(r.status === 401){{ showLock(); return null; }}
    return r.json();
  }}).then(function(d){{
    if(!d || !d.allowed) showLock();
  }}).catch(function(){{
    // Backend unreachable - deny access
    showLock();
  }});
}})();
</script>
"""
    
    content = content.replace('<head>', '<head>\n' + lock, 1)
    open(filename, 'w', encoding='utf-8').write(content)
    print(f'Done - {filename} locked for {feature}')
