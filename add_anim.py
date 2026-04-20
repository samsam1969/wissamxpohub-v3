f = open("WissamXpoHub_V3_Frontend_FIXED.html", encoding="utf-8")
html = f.read()
f.close()

anim_css = """
    @keyframes flagFloat {
      0%,100% { transform: translateY(0); }
      50%      { transform: translateY(-5px); }
    }
    @keyframes arrowPulse {
      0%,100% { opacity:.3; }
      50%      { opacity:1; }
    }"""

if "flagFloat" not in html:
    html = html.replace("    @keyframes spin {", anim_css + "\n    @keyframes spin {", 1)
    open("WissamXpoHub_V3_Frontend_FIXED.html", "w", encoding="utf-8").write(html)
    print("OK - animations added")
else:
    print("Already present")
