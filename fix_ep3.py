f = open("PotentialBuyers.html", encoding="utf-8")
html = f.read()
f.close()

si = html.find('  try{\n    const res=await fetchWT(backendUrl+"/api/ai/export-advisor"')
ei = html.find("  }catch(err){")

print("si:", si, "ei:", ei)

if si != -1 and ei != -1:
    new_block = """  try{
    const res=await fetchWT(backendUrl+"/api/buyers/search",{method:"POST",headers:{"Content-Type":"application/json","Authorization":"Bearer "+token},body:JSON.stringify({hs_code:hs,country:country})});
    const data=await res.json().catch(()=>({}));
    if(!res.ok){qs("formError").textContent="Error ("+res.status+"): "+(data.error||"Unknown");qs("buyersTableBody").innerHTML='<tr><td colspan="8" style="text-align:center;padding:20px;color:var(--bad);">Server error: '+(data.error||res.status)+'</td></tr>';return;}
    const buyers=data.buyers||[];
    try{localStorage.setItem("wx_buyers_data",JSON.stringify(buyers));localStorage.setItem("wx_buyers_product",productName);localStorage.setItem("wx_buyers_market",country);localStorage.setItem("wx_buyers_hs",hs);}catch(_){}
    renderTable(buyers);qs("statCount").textContent=buyers.length?buyers.length+" companies":"0";
"""
    html = html[:si] + new_block + html[ei:]
    open("PotentialBuyers.html", "w", encoding="utf-8").write(html)
    print("OK - endpoint updated")
else:
    print("FAILED - checking...")
    idx = html.find("fetchWT")
    while idx != -1:
        print(idx, repr(html[idx:idx+60]))
        idx = html.find("fetchWT", idx+1)
