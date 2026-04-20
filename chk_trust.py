import shutil
from datetime import datetime

# First, check what we need to modify
f = open("services/claude_service.py", encoding="utf-8")
c = f.read()
f.close()
print("Size:", len(c))
print("Has sources_used:", "sources_used" in c)
print("Has sourceUrls:", "sourceUrls" in c)

# Show return statement
idx = c.rfind("return {")
print(repr(c[idx:idx+300]))
