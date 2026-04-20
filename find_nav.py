import shutil, os
from datetime import datetime

f = open("WissamXpoHub_V3_Frontend_FIXED.html", encoding="utf-8")
html = f.read()
f.close()
shutil.copy2("WissamXpoHub_V3_Frontend_FIXED.html", f"WissamXpoHub_V3_Frontend_FIXED_BACKUP_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html")

# Find nav/tools section to add Blog button
import re

# Find Potential Buyers button to add Blog near it
patterns = [
    'PotentialBuyers.html',
    'potential-buyers',
    'potentialbuyers',
    'Potential Buyers',
    'المشترين المحتملين',
]
for p in patterns:
    idx = html.find(p)
    if idx != -1:
        print(f"Found '{p}' at {idx}")
        print(repr(html[idx-100:idx+100]))
        print()
