for fname in ["PotentialBuyers.html", "ExportIntelligence.html"]:
    f = open(fname, encoding="utf-8")
    html = f.read()
    f.close()

    # Add instant auth check right after <body> tag
    guard_script = """<script>
// Instant auth check — runs before page renders
(function(){
  var token = localStorage.getItem("wx_access_token");
  var email = localStorage.getItem("wx_user_email");
  if (!token || !email) {
    document.documentElement.style.display = "none";
    window.location.replace("WissamXpoHub_V3_Frontend_FIXED.html");
  }
})();
</script>"""

    if "Instant auth check" not in html:
        html = html.replace("<body>", "<body>\n" + guard_script, 1)
        open(fname, "w", encoding="utf-8").write(html)
        print(f"OK: {fname} - instant guard added")
    else:
        print(f"Already protected: {fname}")
