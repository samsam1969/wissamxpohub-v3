lines = open('WissamXpoHub_V3_Frontend_FIXED.html', encoding='utf-8').readlines()
for i, line in enumerate(lines):
    if 'initSupabase' in line or 'supabase' in line.lower() and 'init' in line.lower():
        print(f'{i+1}: {line.rstrip()}')
