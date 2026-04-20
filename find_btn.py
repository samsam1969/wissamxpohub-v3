f = open("PotentialBuyers.html", encoding="utf-8")
html = f.read()
f.close()

# Find search button and add mode selector before it
old = '<button id="searchBtn"'
idx = html.find(old)
print("searchBtn at:", idx)
print(repr(html[idx-100:idx+100]))
