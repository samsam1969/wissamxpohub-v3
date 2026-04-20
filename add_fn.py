f = open("WissamXpoHub_V3_Frontend_FIXED.html", encoding="utf-8")
html = f.read()
f.close()

old = "  function goBack() {"
new = """  function goToPotentialBuyers() {
    const hs = (document.getElementById("hs")||{}).value || "";
    const country = (document.getElementById("country")||{}).value || "";
    if (hs) localStorage.setItem("wx_pb_hs", hs);
    if (country && country !== "__ALL__") localStorage.setItem("wx_pb_country", country);
    window.location.href = "PotentialBuyers.html";
  }

  function goBack() {"""

if old in html:
    html = html.replace(old, new, 1)
    open("WissamXpoHub_V3_Frontend_FIXED.html", "w", encoding="utf-8").write(html)
    print("OK - goToPotentialBuyers added")
else:
    print("Not found - searching for script area...")
    idx = html.find("function saveSettings")
    print("saveSettings at:", idx)
