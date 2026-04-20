# Lock ExportOpportunityScanner.html - Starter+ only
lock_starter = """<script>
(function(){
  var token = null;
  try {
    var keys = Object.keys(localStorage);
    for(var i=0; i<keys.length; i++){
      var v = localStorage.getItem(keys[i]);
      if(v && v.startsWith("eyJ")){ token = v; break; }
      try{ var p = JSON.parse(v); if(p && p.access_token){ token = p.access_token; break; }} catch(e){}
    }
  } catch(e){}

  if(!token){ window.location.href = '/'; return; }

  var backendUrl = localStorage.getItem("wx_backend_url") || "http://localhost:4000";
  fetch(backendUrl + "/api/auth/check-feature/scanner", {
    headers: {"Authorization": "Bearer " + token}
  }).then(function(r){ return r.json(); }).then(function(d){
    if(!d.allowed){
      document.body.innerHTML =
        "<div style='display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:100vh;background:#0f0e17;font-family:Cairo,Arial,sans-serif;text-align:center;padding:24px'>" +
        "<div style='font-size:64px;margin-bottom:16px'>🔒</div>" +
        "<h2 style='color:#a5b4fc;margin-bottom:12px'>Scanner للمشتركين فقط</h2>" +
        "<p style='color:#9ca3af;margin-bottom:8px'>باقتك الحالية: <strong style=color:#fbbf24>" + (d.plan_type||'free') + "</strong></p>" +
        "<p style='color:#9ca3af;margin-bottom:24px'>يتطلب باقة Starter أو أعلى</p>" +
        "<div style='display:flex;gap:12px;flex-wrap:wrap;justify-content:center;margin-bottom:24px'>" +
          "<div style='background:rgba(99,102,241,.1);border:1px solid rgba(99,102,241,.3);border-radius:12px;padding:16px 20px'><div style=color:#a5b4fc;font-weight:800>Starter</div><div style=color:#6b7280;font-size:12px>5 تقارير + Scanner</div><div style=color:white;font-weight:800>299 ج.م</div></div>" +
          "<div style='background:rgba(139,92,246,.15);border:2px solid rgba(139,92,246,.5);border-radius:12px;padding:16px 20px'><div style=color:#c4b5fd;font-weight:800>Pro</div><div style=color:#6b7280;font-size:12px>25 تقرير + كل الميزات</div><div style=color:white;font-weight:800>599 ج.م</div></div>" +
        "</div>" +
        "<a href='https://wa.me/201116415272?text=" + encodeURIComponent("مرحباً، أريد الاشتراك في WissamXpoHub للوصول للـ Scanner") + "' target=_blank style='display:inline-block;background:linear-gradient(135deg,#25d366,#128c7e);color:white;padding:12px 28px;border-radius:50px;text-decoration:none;font-weight:700;margin-bottom:12px'>📱 اشترك عبر واتساب</a><br/>" +
        "<a href='/' style='color:#6b7280;font-size:13px'>← العودة للداشبورد</a>" +
        "</div>";
    }
  }).catch(function(){ window.location.href = '/'; });
})();
</script>"""

# Lock PotentialBuyers.html - Pro+ only
lock_pro = """<script>
(function(){
  var token = null;
  try {
    var keys = Object.keys(localStorage);
    for(var i=0; i<keys.length; i++){
      var v = localStorage.getItem(keys[i]);
      if(v && v.startsWith("eyJ")){ token = v; break; }
      try{ var p = JSON.parse(v); if(p && p.access_token){ token = p.access_token; break; }} catch(e){}
    }
  } catch(e){}

  if(!token){ window.location.href = '/'; return; }

  var backendUrl = localStorage.getItem("wx_backend_url") || "http://localhost:4000";
  fetch(backendUrl + "/api/auth/check-feature/buyers", {
    headers: {"Authorization": "Bearer " + token}
  }).then(function(r){ return r.json(); }).then(function(d){
    if(!d.allowed){
      document.body.innerHTML =
        "<div style='display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:100vh;background:#0f0e17;font-family:Cairo,Arial,sans-serif;text-align:center;padding:24px'>" +
        "<div style='font-size:64px;margin-bottom:16px'>🔒</div>" +
        "<h2 style='color:#a5b4fc;margin-bottom:12px'>Potential Buyers للـ Pro فأعلى</h2>" +
        "<p style='color:#9ca3af;margin-bottom:8px'>باقتك الحالية: <strong style=color:#fbbf24>" + (d.plan_type||'free') + "</strong></p>" +
        "<p style='color:#9ca3af;margin-bottom:24px'>يتطلب باقة Pro أو Agency</p>" +
        "<div style='display:flex;gap:12px;flex-wrap:wrap;justify-content:center;margin-bottom:24px'>" +
          "<div style='background:rgba(139,92,246,.15);border:2px solid rgba(139,92,246,.5);border-radius:12px;padding:16px 20px'><div style=color:#c4b5fd;font-weight:800>Pro</div><div style=color:#6b7280;font-size:12px>25 تقرير + Buyers</div><div style=color:white;font-weight:800>599 ج.م</div></div>" +
          "<div style='background:rgba(245,158,11,.1);border:1px solid rgba(245,158,11,.3);border-radius:12px;padding:16px 20px'><div style=color:#fcd34d;font-weight:800>Agency</div><div style=color:#6b7280;font-size:12px>100 تقرير + كل الميزات</div><div style=color:white;font-weight:800>1,490 ج.م</div></div>" +
        "</div>" +
        "<a href='https://wa.me/201116415272?text=" + encodeURIComponent("مرحباً، أريد الاشتراك في باقة Pro للوصول لـ Potential Buyers") + "' target=_blank style='display:inline-block;background:linear-gradient(135deg,#25d366,#128c7e);color:white;padding:12px 28px;border-radius:50px;text-decoration:none;font-weight:700;margin-bottom:12px'>📱 اشترك عبر واتساب</a><br/>" +
        "<a href='/' style='color:#6b7280;font-size:13px'>← العودة للداشبورد</a>" +
        "</div>";
    }
  }).catch(function(){ window.location.href = '/'; });
})();
</script>"""

# Apply to Scanner
scanner = open('ExportOpportunityScanner.html', encoding='utf-8').read()
if 'check-feature' not in scanner:
    scanner = scanner.replace('<head>', '<head>\n' + lock_starter, 1)
    open('ExportOpportunityScanner.html', 'w', encoding='utf-8').write(scanner)
    print('Scanner locked')
else:
    print('Scanner already locked')

# Apply to Buyers
buyers = open('PotentialBuyers.html', encoding='utf-8').read()
if 'check-feature' not in buyers:
    buyers = buyers.replace('<head>', '<head>\n' + lock_pro, 1)
    open('PotentialBuyers.html', 'w', encoding='utf-8').write(buyers)
    print('Buyers locked')
else:
    print('Buyers already locked')
