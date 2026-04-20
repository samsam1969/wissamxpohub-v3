f = open("WissamXpoHub_V3_Frontend_FIXED.html", encoding="utf-8")
html = f.read()
f.close()

# Check if function exists
print("goToPotentialBuyers exists:", "goToPotentialBuyers" in html)
idx = html.find("goToPotentialBuyers")
while idx != -1:
    print(repr(html[idx:idx+80]))
    idx = html.find("goToPotentialBuyers", idx+1)
