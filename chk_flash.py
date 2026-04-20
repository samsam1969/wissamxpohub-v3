f = open("WissamXpoHub_V3_Frontend_FIXED.html", encoding="utf-8")
html = f.read()
f.close()

# Check first 500 chars after <body>
body_idx = html.find("<body>")
print("BODY START:")
print(repr(html[body_idx:body_idx+600]))
