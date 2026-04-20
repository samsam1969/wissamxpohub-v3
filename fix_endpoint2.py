f = open("PotentialBuyers.html", encoding="utf-8")
html = f.read()
f.close()

# Find try{ block and replace the fetch inside it
start_marker = "  try{\n    const res=await fetchWT(backendUrl+\"/api/ai/export-advisor\""
end_marker = "    const buyers=parseBuyers(text,country);"

si = html.find(start_marker)
ei = html.find(end_marker)

if si != -1 and ei != -1:
    new_block = """  try{
    const res=await fetchWT(backendUrl+"/api/buyers/search",{method:"POST",headers:{"Content-Type":"application/json","Authorization":"Bearer "+token},body:JSON.stringify({hs_code:hs,country:country})});
    const data=await res.json().catch(()=>({}));
    if(!res.ok){qs("formError").textContent="Error ("+res.status+"): "+(data.error||"Unknown");qs("buyersTableBody").innerHTML='<tr><td colspan="8" style="text-align:center;padding:20px;color:var(--bad);">Server error: '+(data.error||res.status)+'</td></tr>';return;}
    const buyers=data.buyers||[];"""
    
    end_pos = ei + len(end_marker)
    html = html[:si] + new_block + "\n" + html[end_pos:]
    open("PotentialBuyers.html", "w", encoding="utf-8").write(html)
    print("OK - endpoint updated to /api/buyers/search")
else:
    print("si:", si, "ei:", ei)
    # Show context around export-advisor
    idx = html.find("/api/ai/export-advisor")
    print(repr(html[idx-300:idx+50]))
