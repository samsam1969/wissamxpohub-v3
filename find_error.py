lines = open('WissamXpoHub_V3_Frontend_FIXED.html', encoding='utf-8').readlines()
for i, line in enumerate(lines):
    if 'Backend error' in line or 'backendError' in line or '402' in line:
        print(f'{i+1}: {line.rstrip()}')
