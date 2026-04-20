# Read corrupted file as latin-1, re-encode bytes, decode as utf-8
with open('WissamXpoHub_V3_Frontend_FIXED.html', 'r', encoding='latin-1') as f:
    corrupted = f.read()

try:
    fixed = corrupted.encode('latin-1').decode('utf-8')
    with open('WissamXpoHub_V3_Frontend_FIXED.html', 'w', encoding='utf-8') as f:
        f.write(fixed)
    print('SUCCESS - Arabic restored')
except Exception as e:
    print('ERROR:', e)
