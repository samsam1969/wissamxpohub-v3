f = open("WissamXpoHub_V3_Frontend_FIXED.html", encoding="utf-8")
html = f.read()
f.close()

idx = html.find("async function runIntelligence")
if idx == -1:
    idx = html.find("function runIntelligence")
print("Found at:", idx)
print(repr(html[idx:idx+2000]))
