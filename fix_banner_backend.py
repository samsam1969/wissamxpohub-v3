lines = open('WissamXpoHub_V3_Frontend_FIXED.html', encoding='utf-8').readlines()

for i, line in enumerate(lines):
    if 'if (type === "free" && isLoggedIn) showFreeTrialEndedBanner();' in line:
        lines[i] = '''    // Check real plan from backend before showing banner
    if (isLoggedIn) {
      var bkUrl = localStorage.getItem("wx_backend_url") || "http://localhost:4000";
      var tok = null;
      try {
        var ks = Object.keys(localStorage);
        for(var ki=0; ki<ks.length; ki++){
          var kv = localStorage.getItem(ks[ki]);
          if(kv && kv.startsWith("eyJ")){ tok = kv; break; }
          try{ var kp = JSON.parse(kv); if(kp && kp.access_token){ tok = kp.access_token; break; }}catch(e){}
        }
      } catch(e){}
      if (tok) {
        fetch(bkUrl + "/api/auth/my-plan", {
          headers: {"Authorization": "Bearer " + tok}
        }).then(function(r){ return r.json(); }).then(function(d){
          var realPlan = d.plan_type || "free";
          localStorage.setItem("wx_plan_type", realPlan);
          localStorage.setItem("wx_plan_used", d.reports_used || 0);
          localStorage.setItem("wx_plan_limit", d.reports_limit || 1);
          if (realPlan === "free") showFreeTrialEndedBanner();
        }).catch(function(){});
      }
    }
'''
        print(f'Fixed at line {i+1}')
        break

open('WissamXpoHub_V3_Frontend_FIXED.html', 'w', encoding='utf-8').writelines(lines)
print('Done - banner checks backend')
