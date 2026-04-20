f = open("PotentialBuyers.html", encoding="utf-8")
html = f.read()
f.close()

# Find and replace using slice
start = html.find("<script>\n// Instant auth check")
end = html.find("</script>", start) + 9

print("start:", start, "end:", end)
print(repr(html[start:end]))

new = """<script>
(function(){
  var t=localStorage.getItem("wx_access_token");
  var e=localStorage.getItem("wx_user_email");
  if(!t||!e){window.location.replace("WissamXpoHub_V3_Frontend_FIXED.html");}
})();
</script>"""

if start != -1 and end > start:
    html = html[:start] + new + html[end:]
    open("PotentialBuyers.html", "w", encoding="utf-8").write(html)
    print("OK - fixed")
