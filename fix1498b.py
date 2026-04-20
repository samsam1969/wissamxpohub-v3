lines = open('WissamXpoHub_V3_Frontend_FIXED.html', encoding='utf-8').readlines()
lines[1497] = '        if(qs("aiBox"))qs("aiBox").textContent = "Backend error: " + (data.error || data.message || "Unknown error");\n'
open('WissamXpoHub_V3_Frontend_FIXED.html', 'w', encoding='utf-8').writelines(lines)
print('Done')
