with open('WissamXpoHub_V3_Frontend_FIXED.html', encoding='utf-8') as f:
    content = f.read()

# Remove scannerSection references
content = content.replace(
    'if (!e.target.closest("#scannerSection")) closeAcDropdown();',
    'closeAcDropdown();'
)

# Remove populateScannerEuFilter function
s1 = content.find('  function populateScannerEuFilter()')
e1 = content.find('\n  let scanFilterMode')
if s1 != -1 and e1 != -1:
    content = content[:s1] + content[e1:]

# Remove setScanFilter function  
s2 = content.find('  function setScanFilter(')
e2 = content.find('\n\n  /* --- INIT')
if s2 == -1:
    s2 = content.find('  function setScanFilter(')
if e2 == -1:
    e2 = content.find('\n\n  loadSettings()')
if s2 != -1 and e2 != -1:
    content = content[:s2] + content[e2:]

# Remove leftover variables
content = content.replace('  let scanFilterMode = "top10";\n', '')
content = content.replace('  let scanFilterCountry = "";\n', '')

with open('WissamXpoHub_V3_Frontend_FIXED.html', 'w', encoding='utf-8') as f:
    f.write(content)

remaining = content.count('scannerSection')
print('scannerSection remaining:', remaining)
print('DONE!' if remaining == 0 else 'Still has: ' + str(remaining))