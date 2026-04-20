lines = open('WissamXpoHub_V3_Frontend_FIXED.html', encoding='utf-8').readlines()

# Improve userPlan display style
lines[1401] = '''    const planColors = {
      "free": "background:rgba(107,114,128,.2);color:#9ca3af",
      "starter": "background:rgba(99,102,241,.2);color:#a5b4fc", 
      "pro": "background:rgba(139,92,246,.2);color:#c4b5fd",
      "agency": "background:rgba(245,158,11,.2);color:#fcd34d"
    };
    const planIcons = {"free":"🆓","starter":"🥉","pro":"🥈","agency":"🥇"};
    const planKey = planLabel.toLowerCase().replace(/[^a-z]/g,"") || "free";
    const pColor = planColors[planKey] || planColors.free;
    const pIcon = planIcons[planKey] || "";
    if (qs("statPlan")) qs("statPlan").textContent = planLabel;
    if (qs("userPlan")) {
      qs("userPlan").innerHTML = <span style="padding:3px 10px;border-radius:99px;font-size:12px;font-weight:700;"> </span>;
    }
'''

open('WissamXpoHub_V3_Frontend_FIXED.html', 'w', encoding='utf-8').writelines(lines)
print('Done - plan badge added')
