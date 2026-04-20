f = open("PotentialBuyers.html", encoding="utf-8")
html = f.read()
f.close()

# Update table headers
old_th = "<thead><tr><th>#</th><th>Company Name</th><th>Country</th><th>Source</th><th>Source Link</th><th>Website</th><th>Email</th><th>Phone</th></tr></thead>"
new_th = "<thead><tr><th>#</th><th>Company Name</th><th>Country</th><th>Source</th><th>Website</th><th>Email</th><th>Phone</th><th>Find & Verify</th></tr></thead>"

# Update renderTable function
old_render = """  tbody.innerHTML=buyers.map((b,i)=>{
    const sl=b.sourceLink?'<a href="https://'+b.sourceLink+'" target="_blank" rel="noopener" class="ext-link">'+b.sourceLink.split("/")[0]+'</a>':'<span class="tag-none">-</span>';
    const web=b.website?'<a href="https://'+b.website+'" target="_blank" rel="noopener" class="ext-link">'+b.website.split("/")[0]+'</a>':'<span class="tag-none">-</span>';
    const email=b.email?'<a href="mailto:'+b.email+'" class="ext-link">'+b.email+'</a>':'<span class="tag-none">-</span>';
    const phone=b.phone||'<span class="tag-none">-</span>';
    return'<tr><td style="color:var(--muted);font-size:11px;">'+(i+1)+'</td><td><div class="company-name">'+b.name+'</div></td><td style="font-size:12px;color:var(--muted);">'+b.country+'</td><td><span class="badge-src">'+b.source+'</span></td><td>'+sl+'</td><td>'+web+'</td><td style="font-size:12px;">'+email+'</td><td style="font-size:12px;">'+phone+'</td></tr>';
  }).join("");}"""

new_render = """  tbody.innerHTML=buyers.map((b,i)=>{
    const web=b.website?'<a href="https://'+b.website+'" target="_blank" rel="noopener" class="ext-link">'+b.website.split("/")[0]+'</a>':'<span class="tag-none">-</span>';
    const email=b.email?'<a href="mailto:'+b.email+'" class="ext-link">'+b.email+'</a>':'<span class="tag-none">-</span>';
    const phone=b.phone||'<span class="tag-none">-</span>';
    const sl=b.search_links||{};
    const findBtns='<div style="display:flex;gap:4px;flex-wrap:wrap;">'
      +(sl.europages?'<a href="'+sl.europages+'" target="_blank" style="font-size:10px;padding:2px 7px;border-radius:6px;background:rgba(29,78,216,.2);color:#93c5fd;border:1px solid rgba(29,78,216,.4);text-decoration:none;white-space:nowrap;">Europages</a>':'')
      +(sl.kompass?'<a href="'+sl.kompass+'" target="_blank" style="font-size:10px;padding:2px 7px;border-radius:6px;background:rgba(139,92,246,.2);color:#c4b5fd;border:1px solid rgba(139,92,246,.4);text-decoration:none;white-space:nowrap;">Kompass</a>':'')
      +(sl.linkedin?'<a href="'+sl.linkedin+'" target="_blank" style="font-size:10px;padding:2px 7px;border-radius:6px;background:rgba(59,130,246,.2);color:#93c5fd;border:1px solid rgba(59,130,246,.4);text-decoration:none;white-space:nowrap;">LinkedIn</a>':'')
      +(sl.google?'<a href="'+sl.google+'" target="_blank" style="font-size:10px;padding:2px 7px;border-radius:6px;background:rgba(16,185,129,.15);color:#6ee7b7;border:1px solid rgba(16,185,129,.3);text-decoration:none;white-space:nowrap;">Google</a>':'')
      +'</div>';
    return'<tr><td style="color:var(--muted);font-size:11px;">'+(i+1)+'</td><td><div class="company-name">'+b.name+'</div></td><td style="font-size:12px;color:var(--muted);">'+b.country+'</td><td><span class="badge-src">'+b.source+'</span></td><td>'+web+'</td><td style="font-size:12px;">'+email+'</td><td style="font-size:12px;">'+phone+'</td><td>'+findBtns+'</td></tr>';
  }).join("");}"""

if old_th in html:
    html = html.replace(old_th, new_th, 1)
    print("Header updated")
else:
    print("Header not found")

if old_render in html:
    html = html.replace(old_render, new_render, 1)
    print("Render updated")
else:
    print("Render not found - will patch footer note instead")
    old_note = "Only rows with a real company name AND verified source are displayed. Sources: Europages, Kompass, WLW, Trade Map, LinkedIn."
    new_note = "Only real company names with verified sources are displayed. Use Find & Verify buttons to check contact info directly on source platforms."
    html = html.replace(old_note, new_note, 1)

open("PotentialBuyers.html", "w", encoding="utf-8").write(html)
print("HTML saved")
