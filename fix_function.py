lines = open('WissamXpoHub_V3_Frontend_FIXED.html', encoding='utf-8').readlines()

# Insert missing function declaration before line 2688 (index 2687)
lines.insert(2687, '  function toggleSourcesPanel() {\n')

open('WissamXpoHub_V3_Frontend_FIXED.html', 'w', encoding='utf-8').writelines(lines)
print('Done - function toggleSourcesPanel() restored at line 2688')
