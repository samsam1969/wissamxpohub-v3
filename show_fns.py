f = open("WissamXpoHub_V3_Frontend_FIXED.html", encoding="utf-8")
html = f.read()
f.close()

for fn in ["requireSavedSettings", "buildPayload"]:
    idx = html.find(f"function {fn}")
    if idx == -1:
        idx = html.find(fn)
    print(f"\n{fn} at {idx}:")
    print(repr(html[idx:idx+400]))
