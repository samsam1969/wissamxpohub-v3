f = open("services/claude_service.py", encoding="utf-8")
c = f.read()
f.close()

# Fix FOB for dates 080410
old = '            "080410": 480,  # Dates'
new = '            "080410": 420,  # Dates (Egyptian dates avg FOB)'
if old in c:
    c = c.replace(old, new, 1)
    print("OK1: dates FOB fixed to 420")
else:
    print("FAIL1 - checking...")
    idx = c.find("080410")
    print(repr(c[idx-10:idx+50]))

# Also check the base_fob default override logic
idx2 = c.find("base_fob = FOB_DEFAULTS.get")
print("FOB logic at:", idx2)
print(repr(c[idx2:idx2+200]))

open("services/claude_service.py", "w", encoding="utf-8").write(c)
print("Done")
