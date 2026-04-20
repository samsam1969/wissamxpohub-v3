import os

html = open('admin_knowledge.html', encoding='utf-8').read()

# Check if script tag is broken
if '<script>' not in html or 'function loadData' not in html:
    print('FILE IS BROKEN - need rebuild')
else:
    print('File OK - issue elsewhere')
    
# Show last 200 chars
print('END OF FILE:', repr(html[-200:]))
