f = open("PotentialBuyers.html", encoding="utf-8")
html = f.read()
f.close()

# Find and replace renderTable function
old = "  tbody.innerHTML=buyers.map((b,i)=>{"
idx = html.find(old)
print("renderTable found at:", idx)

if idx != -1:
    # Find end of function
    end_marker = "}).join(\"\");"
    ei = html.find(end_marker, idx)
    print("end at:", ei)
    
    new_render = """  tbody.innerHTML=buyers.map((b,i)=>{
    const web=b.website?'<a href="https://'+b.website+'" target="_blank" rel="noopener" class="ext-link">'+b.website.split("/")[0]+'</a>':'<span class="tag-none">-</span>';
    const email=b.email?'<a href="mailto:'+b.email+'" class="ext-link">'+b.email+'</a>':'<span class="tag-none">-</span>';
    const phone=b.phone?b.phone:'<span class="tag-none">-</span>';
    const nm=encodeURIComponent(b.name);
    const ct=encodeURIComponent(b.country);
    const findBtns='<div style="display:flex;gap:3px;flex-wrap:wrap;">'
      +'<a href="https://www.europages.com/companies/'+ct+'/'+nm+'.html" target="_blank" style="font-size:10px;padding:2px 6px;border-radius:5px;background:rgba(29,78,216,.2);color:#93c5fd;border:1px solid rgba(29,78,216,.4);text-decoration:none;">EP</a>'
      +'<a href="https://www.kompass.com/a/search/?search='+nm+'&lang=en" target="_blank" style="font-size:10px;padding:2px 6px;border-radius:5px;background:rgba(139,92,246,.2);color:#c4b5fd;border:1px solid rgba(139,92,246,.4);text-decoration:none;">KP</a>'
      +'<a href="https://www.linkedin.com/search/results/companies/?keywords='+nm+'" target="_blank" style="font-size:10px;padding:2px 6px;border-radius:5px;background:rgba(59,130,246,.2);color:#93c5fd;border:1px solid rgba(59,130,246,.4);text-decoration:none;">LI</a>'
      +'<a href="https://www.google.com/search?q='+nm+'+importer+'+ct+'+email+contact" target="_blank" style="font-size:10px;padding:2px 6px;border-radius:5px;background:rgba(16,185,129,.15);color:#6ee7b7;border:1px solid rgba(16,185,129,.3);text-decoration:none;">G</a>'
      +'</div>';
    return'<tr><td style="color:var(--muted);font-size:11px;">'+(i+1)+'</td><td><div class="company-name">'+b.name+'</div></td><td style="font-size:12px;color:var(--muted);">'+b.country+'</td><td><span class="badge-src">'+b.source+'</span></td><td>'+web+'</td><td style="font-size:12px;">'+email+'</td><td style="font-size:12px;">'+phone+'</td><td>'+findBtns+'</td></tr>';
  }).join("");"""
    
    end_pos = ei + len(end_marker)
    html = html[:idx] + new_render + html[end_pos:]
    
    # Also fix table header
    old_th = "<thead><tr><th>#</th><th>Company Name</th><th>Country</th><th>Source</th><th>Source Link</th><th>Website</th><th>Email</th><th>Phone</th></tr></thead>"
    new_th = "<thead><tr><th>#</th><th>Company Name</th><th>Country</th><th>Source</th><th>Website</th><th>Email</th><th>Phone</th><th>Find & Verify</th></tr></thead>"
    html = html.replace(old_th, new_th, 1)
    
    old_th2 = "<thead><tr><th>#</th><th>Company Name</th><th>Country</th><th>Source</th><th>Website</th><th>Email</th><th>Phone</th></tr></thead>"
    new_th2 = "<thead><tr><th>#</th><th>Company Name</th><th>Country</th><th>Source</th><th>Website</th><th>Email</th><th>Phone</th><th>Find & Verify</th></tr></thead>"
    html = html.replace(old_th2, new_th2, 1)
    
    open("PotentialBuyers.html", "w", encoding="utf-8").write(html)
    print("Done - renderTable updated with Find & Verify buttons")
