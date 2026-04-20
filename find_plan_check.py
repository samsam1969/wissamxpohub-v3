lines = open('WissamXpoHub_V3_Frontend_FIXED.html', encoding='utf-8').readlines()
for i, line in enumerate(lines):
    if 'planUsed' in line or 'planLimit' in line or 'wx_plan' in line:
        print(f'{i+1}: {line.rstrip()}')
