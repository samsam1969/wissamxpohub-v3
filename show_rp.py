f = open("WissamXpoHub_V3_Frontend_FIXED.html", encoding="utf-8")
html = f.read()
f.close()

# Show more of right panel
idx = html.find("Right panel")
print(repr(html[idx:idx+2000]))
