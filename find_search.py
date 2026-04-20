f = open("PotentialBuyers.html", encoding="utf-8")
html = f.read()
f.close()

idx = html.find("searchBuyers")
while idx != -1:
    print(repr(html[idx-30:idx+80]))
    print("---")
    idx = html.find("searchBuyers", idx+1)
