f = open("PotentialBuyers.html", encoding="utf-8")
html = f.read()
f.close()

old = """    const res=await fetchWT(backendUrl+"/api/buyers/search",{method:"POST",headers:{"Content-Type":"application/json","Authorization":"Bearer "+token},body:JSON.stringify({hs_code:hs,country:country})});"""

new = """    const searchMode = document.getElementById("searchMode")?.value || "ai";
    const res=await fetchWT(backendUrl+"/api/buyers/search",{method:"POST",headers:{"Content-Type":"application/json","Authorization":"Bearer "+token},body:JSON.stringify({hs_code:hs,country:country,mode:searchMode})});"""

if old in html:
    html = html.replace(old, new, 1)
    print("OK1: mode param added")
else:
    print("FAIL1")

# Add mode selector next to search button
old_btn = """<button id="searchBtn" onclick="searchBuyers()">Search Buyers</button>"""
new_btn = """<div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;">
  <select id="searchMode" style="width:auto;padding:12px 16px;border-radius:12px;font-size:13px;font-weight:700;border:1px solid var(--line);background:rgba(0,0,0,.3);color:#fff;">
    <option value="ai">🤖 AI Search</option>
    <option value="live">🌐 Live Search (Lightpanda)</option>
  </select>
  <button id="searchBtn" onclick="searchBuyers()" style="flex:1;">Search Buyers</button>
</div>"""

if old_btn in html:
    html = html.replace(old_btn, new_btn, 1)
    print("OK2: mode selector added")
else:
    print("FAIL2 - trying alt...")
    idx = html.find("searchBuyers()")
    print(repr(html[idx-50:idx+60]))

open("PotentialBuyers.html", "w", encoding="utf-8").write(html)
print("Done")
