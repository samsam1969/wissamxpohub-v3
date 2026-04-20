f = open("WissamXpoHub_V3_Frontend_FIXED.html", encoding="utf-8")
html = f.read()
f.close()

# Fix runIntelligence function - null-safe stat updates
old = """    qs("statsRow").style.display="grid";qs("statProduct").textContent=productName;qs("statMarket").textContent=country;qs("statHs").textContent=hs;qs("statSources").textContent=getSources().length+" sources";"""

new = """    if(qs("statsRow"))qs("statsRow").style.display="grid";
    if(qs("statProduct"))qs("statProduct").textContent=productName;
    if(qs("statMarket"))qs("statMarket").textContent=country;
    if(qs("statHs"))qs("statHs").textContent=hs;
    if(qs("statSources"))qs("statSources").textContent=getSources().length+" sources";"""

if old in html:
    html = html.replace(old, new, 1)
    print("OK1")
else:
    print("FAIL1 - searching...")
    idx = html.find("statProduct")
    while idx != -1:
        ctx = html[idx-30:idx+60]
        if "textContent" in ctx:
            print(repr(ctx))
        idx = html.find("statProduct", idx+1)

# Fix reportSubtitle null error
old2 = 'qs("reportSubtitle").textContent'
new2 = 'if(qs("reportSubtitle"))qs("reportSubtitle").textContent'
count = html.count(old2)
if count:
    html = html.replace(old2, new2)
    print(f"OK2: fixed {count} reportSubtitle refs")

# Fix aiLoader null error  
old3 = 'qs("aiLoader").classList.add("show")'
new3 = 'if(qs("aiLoader"))qs("aiLoader").classList.add("show")'
if old3 in html:
    html = html.replace(old3, new3)
    print("OK3: aiLoader fixed")

old4 = 'qs("aiLoader").classList.remove("show")'
new4 = 'if(qs("aiLoader"))qs("aiLoader").classList.remove("show")'
if old4 in html:
    html = html.replace(old4, new4)
    print("OK4: aiLoader remove fixed")

open("WissamXpoHub_V3_Frontend_FIXED.html", "w", encoding="utf-8").write(html)
print("Done")
