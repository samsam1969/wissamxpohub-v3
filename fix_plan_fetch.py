content = open('WissamXpoHub_V3_Frontend_FIXED.html', encoding='utf-8').read()

# Fix 1: Clear plan data on logout
old = 'localStorage.removeItem("wx_user_remaining")'
new = '''localStorage.removeItem("wx_user_remaining");
    localStorage.removeItem("wx_plan_type");
    localStorage.removeItem("wx_plan_used");
    localStorage.removeItem("wx_plan_limit");
    localStorage.removeItem("wx_user_email");
    localStorage.removeItem("wx_user_plan");'''
content = content.replace(old, new, 1)

# Fix 2: After login, fetch real plan from backend
old2 = '      localStorage.setItem("wx_user_remaining", rem);'
new2 = '''      localStorage.setItem("wx_user_remaining", rem);
      // Always fetch real plan after login
      fetch(getSettings().backendUrl + "/api/auth/my-plan", {
        headers: {"Authorization": "Bearer " + localStorage.getItem("sb-access-token") || ""}
      }).then(r => r.json()).then(d => {
        if(d.plan_type) {
          localStorage.setItem("wx_plan_type", d.plan_type);
          localStorage.setItem("wx_plan_limit", d.reports_limit);
          localStorage.setItem("wx_plan_used", d.reports_used);
          updatePlanBar(d.reports_used, d.reports_limit, d.plan_type);
        }
      }).catch(e => {});'''
content = content.replace(old2, new2, 1)

open('WissamXpoHub_V3_Frontend_FIXED.html', 'w', encoding='utf-8').write(content)
print('Done - logout and plan fetch fixed')
