f = open("PotentialBuyers.html", encoding="utf-8")
html = f.read()
f.close()

# Replace the fetch call to use new endpoint
old = """    const prompt='You are a B2B trade research specialist. Find REAL companies that import or distribute "'+productName+'" (HS Code: '+hs+') in '+country+'. CRITICAL RULES: Only list REAL companies with actual business names. Each row needs Company Name + at least Source or Website. Never use country names, regions, or vague descriptions as company names. Skip any row where the company name is generic or unverifiable. Search: Europages, Kompass, WLW, LinkedIn, Google B2B Return ONLY this markdown table: | Company Name | Country | Source | Source Link | Website | Email | Phone | |---|---|---|---|---|---|---| Find 10-15 real companies in '+country+' only. Skip unverified entries.';
    const res=await fetchWT(backendUrl+"/api/ai/export-advisor",{method:"POST",headers:{"Content-Type":"application/json","Authorization":"Bearer "+token},body:JSON.stringify({hs_code:hs,product:productName,target_market:country,company_info:prompt,sources_mode:"europages,kompass,wlw,linkedin_companies,google_b2b,trade_map"})});
    const data=await res.json().catch(()=>({}));
    if(!res.ok){qs("formError").textContent="Error ("+res.status+"): "+(data.error||"Unknown");qs("buyersTableBody").innerHTML='<tr><td colspan="8" style="text-align:center;padding:20px;color:var(--bad);">Server error: '+(data.error||res.status)+'</td></tr>';return;}
    const text=typeof data.advisor==="string"?data.advisor:(data.advisor?.text||JSON.stringify(data));
    const buyers=parseBuyers(text,country);"""

new = """    const res=await fetchWT(backendUrl+"/api/buyers/search",{method:"POST",headers:{"Content-Type":"application/json","Authorization":"Bearer "+token},body:JSON.stringify({hs_code:hs,country:country})});
    const data=await res.json().catch(()=>({}));
    if(!res.ok){qs("formError").textContent="Error ("+res.status+"): "+(data.error||"Unknown");qs("buyersTableBody").innerHTML='<tr><td colspan="8" style="text-align:center;padding:20px;color:var(--bad);">Server error: '+(data.error||res.status)+'</td></tr>';return;}
    const buyers=data.buyers||[];"""

if old in html:
    html = html.replace(old, new, 1)
    open("PotentialBuyers.html", "w", encoding="utf-8").write(html)
    print("Patch OK - now using /api/buyers/search")
else:
    print("Pattern not found - searching...")
    idx = html.find("/api/ai/export-advisor")
    print("export-advisor at:", idx)
    if idx > 0:
        print(repr(html[idx-200:idx+100]))
