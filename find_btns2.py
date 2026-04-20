f = open("WissamXpoHub_V3_Frontend_FIXED.html", encoding="utf-8")
html = f.read()
f.close()

idx = html.find('<div class="btns hero-auth-btns">')
print(repr(html[idx:idx+600]))
