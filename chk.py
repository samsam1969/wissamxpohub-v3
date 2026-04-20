f = open("PotentialBuyers.html", encoding="utf-8")
html = f.read()
f.close()

# Check if search_links rendering is there
idx = html.find("search_links")
print("search_links in HTML:", idx)
idx2 = html.find("findBtns")
print("findBtns in HTML:", idx2)
