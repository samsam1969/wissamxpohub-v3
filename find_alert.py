lines = open('WissamXpoHub_V3_Frontend_FIXED.html', encoding='utf-8').readlines()
for i, line in enumerate(lines):
    if 'Supabase library not loaded' in line:
        print(f'{i+1}: {line.rstrip()}')
