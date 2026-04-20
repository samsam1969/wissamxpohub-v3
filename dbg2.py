f = open("WissamXpoHub_V3_Frontend_FIXED.html", encoding="utf-8")
html = f.read()
f.close()

s = html.find("<!-- SETUP + CONNECTION -->")
e = html.find("<!-- end .wrap -->")
print("s=", s, "e=", e)
print("END context:", repr(html[e-20:e+50]))

# Also find wrap closing
e2 = html.find("</div><!-- end .wrap -->")
print("e2=", e2)
