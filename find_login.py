lines = open('WissamXpoHub_V3_Frontend_FIXED.html', encoding='utf-8').readlines()
for i, line in enumerate(lines):
    if 'login' in line.lower() and ('onclick' in line.lower() or 'function' in line.lower()):
        print(f'{i+1}: {line.rstrip()}')
