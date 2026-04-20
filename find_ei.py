import shutil, re
from datetime import datetime

f = open("WissamXpoHub_V3_Frontend_FIXED.html", encoding="utf-8")
html = f.read()
f.close()

# Find ExportIntelligence button context
ei = html.find("ExportIntelligence.html")
print("EI at:", ei)
print(repr(html[ei-300:ei+100]))
