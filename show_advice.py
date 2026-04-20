import shutil, re
from datetime import datetime

f = open("services/claude_service.py", encoding="utf-8")
c = f.read()
f.close()
shutil.copy2("services/claude_service.py", f"services/claude_service_BACKUP_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py")

# ── 1. Show current get_export_advice structure
idx = c.find("async def get_export_advice(")
print("get_export_advice at:", idx)
print(repr(c[idx:idx+3000]))
