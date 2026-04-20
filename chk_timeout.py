f = open("WissamXpoHub_V3_Frontend_FIXED.html", encoding="utf-8")
html = f.read()
f.close()

# Check the init/setTimeout area
idx = html.find("setTimeout")
while idx != -1:
    print(repr(html[idx:idx+150]))
    print("---")
    idx = html.find("setTimeout", idx+1)
