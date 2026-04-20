import shutil
from datetime import datetime

f = open("services/trade_data_service.py", encoding="utf-8")
c = f.read()
f.close()
shutil.copy2("services/trade_data_service.py", f"services/trade_data_service_BACKUP_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py")

# Remove invalid params - partnerCode=ALL, customsCode, motCode cause 400 errors
old_params = '''    full_params = {
        **params,
        "partnerCode":    "ALL",
        "breakdownMode":  "classic",
        "customsCode":    "C00",
        "motCode":        "0",
        "includeDesc":    "true",
    }'''

new_params = '''    # Note: partnerCode=ALL invalid in Preview API
    # breakdownMode=classic + includeDesc work fine
    full_params = {
        **params,
        "breakdownMode": "classic",
        "includeDesc":   "true",
    }'''

if old_params in c:
    c = c.replace(old_params, new_params, 1)
    print("OK1: invalid params removed")
else:
    print("FAIL1 - searching...")
    idx = c.find("partnerCode")
    print(repr(c[idx-30:idx+80]))

# Also fix filter: remove C00 filter since it works now
old_filter = '''        # Filter: only C00 (total customs) to prevent double counting
        records = [r for r in records if r.get("customsCode","C00") in ("C00","")]'''
new_filter = '''        # Filter: keep C00 (TOTAL CPC) and aggregates only
        records = [r for r in records if r.get("customsCode","C00") in ("C00","") 
                   and r.get("isAggregate", False) == False or r.get("customsCode") == "C00"]'''

if old_filter in c:
    c = c.replace(old_filter, new_filter, 1)
    print("OK2: filter updated")

open("services/trade_data_service.py", "w", encoding="utf-8").write(c)
print("Done")
