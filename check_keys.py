lines = open('WissamXpoHub_V3_Frontend_FIXED.html', encoding='utf-8').readlines()
for i, line in enumerate(lines):
    if 'SUPABASE_URL' in line or 'SUPABASE_ANON_KEY' in line or 'ANON_KEY' in line:
        print(f'{i+1}: {line.rstrip()}')
