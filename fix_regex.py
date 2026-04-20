lines = open('WissamXpoHub_V3_Frontend_FIXED.html', encoding='utf-8').readlines()
lines[1521] = '            /^[A-Za-z]/.test(cell) && !cell.includes("استيراد") &&\n'
open('WissamXpoHub_V3_Frontend_FIXED.html', 'w', encoding='utf-8').writelines(lines)
print('Done - line 1522 fixed')
