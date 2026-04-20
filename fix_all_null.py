import shutil
from datetime import datetime

f = open("WissamXpoHub_V3_Frontend_FIXED.html", encoding="utf-8")
html = f.read()
f.close()

shutil.copy2("WissamXpoHub_V3_Frontend_FIXED.html", f"WissamXpoHub_V3_Frontend_FIXED_BACKUP_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html")

import re

# Make ALL qs().textContent null-safe
def make_safe(m):
    el = m.group(1)
    val = m.group(2)
    return f'if(qs("{el}"))qs("{el}").textContent{val}'

# Pattern: qs("xxx").textContent = something
html = re.sub(
    r'qs\("([^"]+)"\)\.textContent(\s*=\s*[^;]+;)',
    make_safe,
    html
)

# Also fix .innerHTML assignments
def make_safe_html(m):
    el = m.group(1)
    val = m.group(2)
    return f'if(qs("{el}"))qs("{el}").innerHTML{val}'

html = re.sub(
    r'qs\("([^"]+)"\)\.innerHTML(\s*=\s*[^;]+;)',
    make_safe_html,
    html
)

# Fix .classList operations
html = re.sub(
    r'qs\("([^"]+)"\)\.classList\.',
    lambda m: f'qs("{m.group(1)}")&&qs("{m.group(1)}").classList.',
    html
)

# Fix .style operations  
html = re.sub(
    r'qs\("([^"]+)"\)\.style\.(\w+)\s*=',
    lambda m: f'if(qs("{m.group(1)}"))qs("{m.group(1)}").style.{m.group(2)}=',
    html
)

open("WissamXpoHub_V3_Frontend_FIXED.html", "w", encoding="utf-8").write(html)
print("Done - all null checks added, size:", len(html))
