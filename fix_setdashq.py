content = open('WissamXpoHub_V3_Frontend_FIXED.html', encoding='utf-8').read()

old = '''  function setDashQ(btn, text) {'''

new = '''  function setDashQ(btn, text) {
    // Check plan limit before activating
    var used  = parseInt(localStorage.getItem("wx_plan_used") || "0");
    var limit = parseInt(localStorage.getItem("wx_plan_limit") || "1");
    if (used >= limit) {
      showUpgradeModal("وصلت للحد الاقصى — اختر باقة للاستمرار");
      return;
    }'''

content = content.replace(old, new, 1)
open('WissamXpoHub_V3_Frontend_FIXED.html', 'w', encoding='utf-8').write(content)
print('Done - setDashQ check added')
