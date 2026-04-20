f = open("ExportIntelligence.html", encoding="utf-8")
html = f.read()
f.close()

old_sb = '<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>'
if "auth_guard.js" not in html:
    html = html.replace(old_sb, old_sb + '\n<script src="auth_guard.js"></script>', 1)

old_init_call = "init();"
new_init_call = "WX_AUTH.guard().then(ok => { if (ok) init(); });"
html = html.replace(old_init_call, new_init_call, 1)

open("ExportIntelligence.html", "w", encoding="utf-8").write(html)
print("OK: ExportIntelligence.html protected")
