lines = open('WissamXpoHub_V3_Frontend_FIXED.html', encoding='utf-8').readlines()
lines[1413] = '      qs("userPlan").innerHTML = \'<span style="padding:3px 10px;border-radius:99px;font-size:12px;font-weight:700;" id="planBadge">\' + pIcon + " " + planLabel + \'</span>\';\n'
open('WissamXpoHub_V3_Frontend_FIXED.html', 'w', encoding='utf-8').writelines(lines)
print('Done')
