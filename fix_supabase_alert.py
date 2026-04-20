lines = open('WissamXpoHub_V3_Frontend_FIXED.html', encoding='utf-8').readlines()

# Fix initSupabase - remove alert, just return false silently
lines[1904] = '      return false;\n'

open('WissamXpoHub_V3_Frontend_FIXED.html', 'w', encoding='utf-8').writelines(lines)
print('Done - removed Supabase alert')
