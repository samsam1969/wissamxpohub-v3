content = open('WissamXpoHub_V3_Frontend_FIXED.html', encoding='utf-8').read()

old = '''    if (data.remaining !== undefined) {
      const rem = data.remaining;
      if (qs("statRemaining"))  if(qs("statRemaining"))qs("statRemaining").textContent  = rem;
      if (qs("userRemaining"))  if(qs("userRemaining"))qs("userRemaining").textContent  = ${rem} credits;
      // Persist credits count
      localStorage.setItem("wx_user_remaining", rem);
    }'''

new = '''    if (data.remaining !== undefined) {
      const rem = data.remaining;
      if (qs("statRemaining"))  if(qs("statRemaining"))qs("statRemaining").textContent  = rem;
      if (qs("userRemaining"))  if(qs("userRemaining"))qs("userRemaining").textContent  = ${rem} credits;
      localStorage.setItem("wx_user_remaining", rem);
      // Update plan bar
      if (data.plan) {
        const used  = data.plan.reports_used  ?? 0;
        const limit = data.plan.reports_limit ?? 5;
        const type  = data.plan.plan_type     ?? "starter";
        updatePlanBar(used, limit, type);
        localStorage.setItem("wx_plan_used",  used);
        localStorage.setItem("wx_plan_limit", limit);
        localStorage.setItem("wx_plan_type",  type);
      }
    }
    // Show limit error
    if (data.error === "limit_reached") {
      showUpgradeModal();
    }'''

content = content.replace(old, new)
open('WissamXpoHub_V3_Frontend_FIXED.html', 'w', encoding='utf-8').write(content)
print('Done - plan bar connected to API')
