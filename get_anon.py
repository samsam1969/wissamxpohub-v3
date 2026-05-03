filepath = r"C:\Users\DELL\Desktop\wissamxpohub-backend\WissamXpoHub_V3_Frontend_FIXED.html"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()
import re
# نبحث عن SUPABASE_ANON_KEY أو anon key
patterns = [
    r'SUPABASE_ANON_KEY["\s:=]+(["\'])(eyJ[^"\']+)\1',
    r'anon["\s:=]+(["\'])(eyJ[^"\']+)\1',
    r'supabaseKey\s*=\s*["\']+(eyJ[^"\']+)["\']',
    r'createClient\([^,]+,\s*["\']+(eyJ[^"\']+)["\']',
]
found = set()
for pat in patterns:
    matches = re.findall(pat, content)
    for m in matches:
        key = m[-1] if isinstance(m, tuple) else m
        if key not in found:
            found.add(key)
            print(f"Found key: {key[:80]}...")
            print(f"Full key:\n{key}\n")
