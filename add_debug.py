f = open("PotentialBuyers.html", encoding="utf-8")
html = f.read()
f.close()

old = "const buyers=parseBuyers(text,country);"
new = "console.log('RAW TEXT:', text.substring(0,800)); const buyers=parseBuyers(text,country); console.log('BUYERS PARSED:', buyers.length, buyers.slice(0,2));"

if old in html:
    html = html.replace(old, new, 1)
    open("PotentialBuyers.html", "w", encoding="utf-8").write(html)
    print("Debug added OK")
else:
    print("Pattern not found - checking...")
    idx = html.find("parseBuyers")
    print("parseBuyers at:", idx)
    print(repr(html[idx-30:idx+60]))
