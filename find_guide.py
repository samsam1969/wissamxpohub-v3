lines = open('WissamXpoHub_V3_Frontend_FIXED.html', encoding='utf-8').readlines()
for i, line in enumerate(lines):
    if 'دليل الاستخدام' in line or 'خطوات الاستخدام' in line or 'ما هذه المنصة' in line:
        print(f'{i+1}: {line.rstrip()[:80]}')
