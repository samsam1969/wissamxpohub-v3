lines = open('WissamXpoHub_V3_Frontend_FIXED.html', encoding='utf-8').readlines()

# Fix line 1498 - corrupted error message
lines[1497] = '        if(qs("aiBox"))qs("aiBox").textContent = Backend error ():\\n;\n'

open('WissamXpoHub_V3_Frontend_FIXED.html', 'w', encoding='utf-8').writelines(lines)
print('Done - line 1498 fixed')
