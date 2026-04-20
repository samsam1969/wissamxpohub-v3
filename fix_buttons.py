lines = open('WissamXpoHub_V3_Frontend_FIXED.html', encoding='utf-8').readlines()

# Fix 1: Remove duplicate showSourcesBtn (line 923, index 922)
lines.pop(922)

# Fix 2: Fix تقرير شامل button (now check new line number after pop)
for i, line in enumerate(lines):
    if 'تقرير شامل' in line and "setDashQ(this,'')" in line:
        lines[i] = lines[i].replace("setDashQ(this,'')", "setDashQ(this,'اعطني تقرير شامل ومفصل عن فرص التصدير لهذا المنتج')")
        print(f'Fixed تقرير شامل at line {i+1}')
        break

open('WissamXpoHub_V3_Frontend_FIXED.html', 'w', encoding='utf-8').writelines(lines)
print('Done')
