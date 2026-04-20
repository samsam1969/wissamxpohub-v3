f = open("WissamXpoHub_V3_Frontend_FIXED.html", encoding="utf-8")
html = f.read()
f.close()

idx = html.find("updateConnectionIndicators")
while idx != -1:
    print(repr(html[idx:idx+150]))
    print("---")
    idx = html.find("updateConnectionIndicators", idx+1)
