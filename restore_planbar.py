content = open('WissamXpoHub_V3_Frontend_FIXED.html', encoding='utf-8').read()

old = '  function showUpgradeModal() {'

new = '''  // Restore plan bar on page load
  (function restorePlanBar() {
    const used  = parseInt(localStorage.getItem("wx_plan_used")  || "0");
    const limit = parseInt(localStorage.getItem("wx_plan_limit") || "5");
    const type  = localStorage.getItem("wx_plan_type") || "starter";
    if (localStorage.getItem("wx_plan_type")) {
      updatePlanBar(used, limit, type);
    }
  })();

  function showUpgradeModal() {'''

content = content.replace(old, new, 1)
open('WissamXpoHub_V3_Frontend_FIXED.html', 'w', encoding='utf-8').write(content)
print('Done - plan bar restores on load')
