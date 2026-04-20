lines = open('WissamXpoHub_V3_Frontend_FIXED.html', encoding='utf-8').readlines()
for i, line in enumerate(lines):
    if 'supabase' in line.lower() and ('cdn' in line.lower() or 'script src' in line.lower()):
        print(f'{i+1}: {line.rstrip()}')
