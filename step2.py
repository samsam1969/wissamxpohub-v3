f = open("PotentialBuyers.html", encoding="utf-8")
html = f.read()
f.close()

# 1. Add script tag
old_sb = '<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>'
if "auth_guard.js" not in html:
    html = html.replace(old_sb, old_sb + '\n<script src="auth_guard.js"></script>', 1)

# 2. Add guard call - replace init() call at bottom
old_init_call = "init();"
new_init_call = "WX_AUTH.guard().then(ok => { if (ok) init(); });"
html = html.replace(old_init_call, new_init_call, 1)

open("PotentialBuyers.html", "w", encoding="utf-8").write(html)
print("OK: PotentialBuyers.html protected")
