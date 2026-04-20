f = open("WissamXpoHub_V3_Frontend_FIXED.html", encoding="utf-8")
html = f.read()
f.close()

# Find the question textarea area
idx = html.find('id="userQuestion"')
print("userQuestion at:", idx)
print(repr(html[idx-50:idx+200]))
print("---")
# Find what comes after textarea
idx2 = html.find('</textarea>', idx)
print("After textarea:")
print(repr(html[idx2:idx2+300]))
