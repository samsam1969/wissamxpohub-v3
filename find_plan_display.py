lines = open('WissamXpoHub_V3_Frontend_FIXED.html', encoding='utf-8').readlines()
for i, line in enumerate(lines):
    if 'userPlan' in line or 'statPlan' in line:
        print(f'{i+1}: {line.rstrip()[:100]}')
