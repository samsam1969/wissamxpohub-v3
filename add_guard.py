import shutil
from datetime import datetime

# ── Add auth guard to PotentialBuyers.html
for fname in ["PotentialBuyers.html", "ExportIntelligence.html"]:
    f = open(fname, encoding="utf-8")
    html = f.read()
    f.close()

    # Add auth_guard.js include after supabase script
    old = '<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>'
    new = '<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>\n<script src="auth_guard.js"></script>'

    if "auth_guard.js" not in html:
        html = html.replace(old, new, 1)

        # Add guard call at start of init()
        old_init = "function init(){"
        new_init = """function init(){
  // Auth Guard — redirect to dashboard if not logged in
  WX_AUTH.guard(true).then(ok => { if (!ok) return; _initPage(); });
}
async function _initPage(){"""

        if old_init in html and "_initPage" not in html:
            # Find closing brace of init
            start = html.find(old_init)
            # Find the matching closing brace
            depth = 0
            pos = start
            while pos < len(html):
                if html[pos] == "{": depth += 1
                elif html[pos] == "}":
                    depth -= 1
                    if depth == 0:
                        end = pos
                        break
                pos += 1

            init_body = html[start+len(old_init):end]
            html = html[:start] + new_init + init_body + "\n}" + html[end+1:]

        open(fname, "w", encoding="utf-8").write(html)
        print(f"OK: {fname} protected")
    else:
        print(f"Already protected: {fname}")
