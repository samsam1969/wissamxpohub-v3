f = open("PotentialBuyers.html", encoding="utf-8")
html = f.read()
f.close()

# Add mode selector before search button
old = '<button type="button" class="primary" id="searchBtn" onclick="runSearch()"'
new = '''<select id="searchMode" style="padding:12px 16px;border-radius:12px;font-size:13px;font-weight:700;border:1px solid var(--line);background:rgba(0,0,0,.3);color:#fff;cursor:pointer;">
    <option value="ai">AI Search</option>
    <option value="live">Live Search (Lightpanda)</option>
  </select>
  <button type="button" class="primary" id="searchBtn" onclick="runSearch()"'''

if old in html:
    html = html.replace(old, new, 1)
    open("PotentialBuyers.html", "w", encoding="utf-8").write(html)
    print("OK - mode selector added")
else:
    print("Not found")

# Also fix the JS to use runSearch and pass mode
f2 = open("PotentialBuyers.html", encoding="utf-8")
html2 = f2.read()
f2.close()

old_js = "const searchMode = document.getElementById(\"searchMode\")?.value || \"ai\";"
if old_js in html2:
    print("OK - JS already has searchMode")
else:
    # Find runSearch function and add mode
    idx = html2.find("async function runSearch()")
    if idx == -1:
        idx = html2.find("function runSearch()")
    print("runSearch at:", idx)
    print(repr(html2[idx:idx+200]))
