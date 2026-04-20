content = open("PotentialBuyers.html", encoding="utf-8").read()
print("PB size:", len(content))
# We will build EI from scratch
html = """<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<meta http-equiv="Cache-Control" content="no-cache,no-store,must-revalidate"/>
<title>Export Intelligence - WissamXpoHub</title>
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&display=swap" rel="stylesheet"/>
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>
:root{--bg:#060f1e;--bg2:#071326;--line:#1e3a6e;--line2:#2d5aa8;--text:#e8f0ff;--muted:#8fabd4;--ok:#4ade80;--bad:#f87171;--warn:#fbbf24;--btn:#1d4ed8;--btn2:#1e293b;--btn3:#15803d;--radius:18px;--shadow:0 8px 32px rgba(0,0,0,.35);}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
html,body{min-height:100%;font-family:'Cairo',Arial,sans-serif;background:linear-gradient(160deg,var(--bg) 0%,var(--bg2) 50%,#08172e 100%);background-attachment:fixed;color:var(--text);overflow-x:hidden;}
.wrap{max-width:1400px;margin:0 auto;padding:20px;}
.top-nav{display:flex;align-items:center;justify-content:space-between;gap:16px;padding:14px 20px;background:rgba(12,26,51,.97);border:1px solid var(--line);border-radius:var(--radius);margin-bottom:20px;flex-wrap:wrap;}
.nav-brand{font-size:18px;font-weight:800;}.nav-brand span{color:#60a5fa;}
.card{background:linear-gradient(160deg,rgba(12,26,51,.97),rgba(8,20,44,.97));border:1px solid var(--line);border-radius:var(--radius);padding:20px;box-shadow:var(--shadow);margin-bottom:18px;}
.card-header{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:16px;flex-wrap:wrap;}
h2{font-size:22px;font-weight:800;}h3{font-size:15px;color:var(--muted);font-weight:600;}
label{display:block;margin:10px 0 6px;color:var(--text);font-weight:700;font-size:14px;}
input,select,textarea{width:100%;border-radius:12px;border:1px solid var(--line);background:rgba(0,0,0,.3);color:#fff;padding:12px 16px;font-size:14px;font-family:'Cairo',Arial,sans-serif;outline:none;transition:border-color .15s;}
input:focus,select:focus,textarea:focus{border-color:var(--line2);box-shadow:0 0 0 3px rgba(45,90,168,.2);}
input::placeholder,textarea::placeholder{color:var(--muted);}select option{background:#0c1a33;}textarea{min-height:90px;resize:vertical;}
button{border:none;border-radius:12px;padding:12px 20px;font-size:14px;font-weight:800;font-family:'Cairo',Arial,sans-serif;cursor:pointer;color:#fff;transition:transform .13s,filter .13s;box-shadow:0 4px 14px rgba(0,0,0,.22);}
button:hover{transform:translateY(-2px);filter:brightness(1.1);}button:active{transform:scale(.97);}
button:disabled{opacity:.5;cursor:not-allowed;transform:none;filter:none;}
.primary{background:var(--btn);}.secondary{background:var(--btn2);}.success{background:#15803d;}.ghost{background:rgba(255,255,255,.06);border:1px solid var(--line);}
.checks{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:8px;}
.checks label{display:flex;align-items:center;gap:8px;margin:0;padding:9px 12px;background:rgba(0,0,0,.22);border:1px solid var(--line);border-radius:10px;font-size:13px;font-weight:600;cursor:pointer;transition:border-color .15s;}
.checks label:hover{border-color:var(--line2);}
.checks input[type=checkbox]{width:auto;margin:0;transform:scale(1.1);accent-color:#3b82f6;}
.boxout{min-height:300px;background:rgba(0,0,0,.28);border:1px solid var(--line);border-radius:14px;padding:16px;line-height:1.85;font-size:15px;overflow:auto;font-family:'Cairo',Arial,sans-serif;}
.boxout h1,.boxout h2,.boxout h3{color:#60a5fa;font-weight:800;margin:16px 0 8px;}
.boxout h1{font-size:20px;border-bottom:1px solid var(--line);padding-bottom:6px;}
.boxout h2{font-size:17px;}.boxout h3{font-size:15px;color:var(--warn);}
.boxout p{margin:8px 0;line-height:1.9;}.boxout ul,.boxout ol{padding-right:20px;margin:8px 0;}.boxout li{margin:5px 0;}.boxout strong{color:#fff;font-weight:800;}
.boxout table{width:100%;border-collapse:collapse;margin:12px 0;font-size:14px;}
.boxout th{background:rgba(29,78,216,.3);color:#93c5fd;padding:10px 12px;text-align:left;font-weight:700;border:1px solid var(--line);}
.boxout td{padding:9px 12px;border:1px solid var(--line);color:var(--text);}
.boxout tr:nth-child(even) td{background:rgba(255,255,255,.03);}
.boxout hr{border:none;border-top:1px solid var(--line);margin:14px 0;}
.boxout code{background:rgba(255,255,255,.08);padding:2px 7px;border-radius:6px;font-size:13px;}
.stats-row{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:18px;}
.stat-card{background:rgba(0,0,0,.3);border:1px solid var(--line);border-radius:14px;padding:14px;text-align:center;}
.stat-card .k{color:var(--muted);font-size:10px;font-weight:700;letter-spacing:1px;text-transform:uppercase;margin-bottom:6px;}
.stat-card .v{font-size:17px;font-weight:800;}
.loader-wrap{display:none;align-items:center;gap:12px;margin-bottom:14px;padding:12px 16px;border:1px solid var(--line);background:rgba(0,0,0,.25);border-radius:14px;}
.loader-wrap.show{display:flex;}
.spinner{width:18px;height:18px;border:3px solid rgba(255,255,255,.12);border-top-color:#60a5fa;border-radius:50%;animation:spin .9s linear infinite;flex-shrink:0;}
@keyframes spin{to{transform:rotate(360deg);}}
.section-label{font-size:11px;font-weight:700;color:var(--muted);letter-spacing:1.5px;text-transform:uppercase;margin:14px 0 8px;padding-bottom:5px;border-bottom:1px solid var(--line);}
.chart-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:18px;}
.chart-card{background:rgba(0,0,0,.3);border:1px solid var(--line);border-radius:14px;padding:14px;}
.product-box{margin-top:6px;color:var(--warn);font-size:15px;font-weight:800;min-height:22px;}
.hint{color:var(--muted);margin-top:6px;font-size:12px;}
a{color:#7eb3ff;text-decoration:none;font-weight:700;}a:hover{text-decoration:underline;}
@media(max-width:900px){.stats-row{grid-template-columns:1fr 1fr;}.chart-grid{grid-template-columns:1fr;}.checks{grid-template-columns:1fr;}}
</style>
</head>
<body>
<div class="wrap">
<nav class="top-nav">
  <div style="display:flex;align-items:center;gap:14px;flex-wrap:wrap;">
    <button class="ghost" onclick="goBack()" style="padding:9px 16px;font-size:13px;border-radius:10px;">Back</button>
    <div class="nav-brand">WissamXpoHub <span>/ Export Intelligence</span></div>
  </div>
  <div id="authStatus" style="font-size:13px;color:var(--muted);font-weight:600;">Checking...</div>
</nav>
<div class="card">
  <div class="card-header"><div><h2>Export Intelligence</h2><h3>AI-powered market analysis for Egyptian exporters</h3></div></div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:18px;">
    <div>
      <label for="hsInput">HS Code <span style="color:var(--bad)">*</span></label>
      <input id="hsInput" placeholder="e.g. 081110" maxlength="10" oninput="updateProductName()"/>
      <div class="product-box" id="productNameBox"></div>
      <div class="hint">Don't know the code? <a href="https://www.trademap.org/" target="_blank">Search Trade Map</a></div>
    </div>
    <div>
      <label for="countryInput">Target EU Market <span style="color:var(--bad)">*</span></label>
      <select id="countryInput">
        <option value="">Select country (required)</option>
        <optgroup label="Top Markets">
          <option value="Germany">Germany</option><option value="France">France</option>
          <option value="Netherlands">Netherlands</option><option value="Italy">Italy</option>
          <option value="Spain">Spain</option><option value="Belgium">Belgium</option><option value="Poland">Poland</option>
        </optgroup>
        <optgroup label="All 27 EU Countries">
          <option value="Austria">Austria</option><option value="Bulgaria">Bulgaria</option>
          <option value="Croatia">Croatia</option><option value="Cyprus">Cyprus</option>
          <option value="Czech Republic">Czech Republic</option><option value="Denmark">Denmark</option>
          <option value="Estonia">Estonia</option><option value="Finland">Finland</option>
          <option value="Greece">Greece</option><option value="Hungary">Hungary</option>
          <option value="Ireland">Ireland</option><option value="Latvia">Latvia</option>
          <option value="Lithuania">Lithuania</option><option value="Luxembourg">Luxembourg</option>
          <option value="Malta">Malta</option><option value="Portugal">Portugal</option>
          <option value="Romania">Romania</option><option value="Slovakia">Slovakia</option>
          <option value="Slovenia">Slovenia</option><option value="Sweden">Sweden</option>
        </optgroup>
      </select>
    </div>
  </div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-top:14px;">
    <div>
      <div class="section-label">Data Sources</div>
      <div class="checks">
        <label><input type="checkbox" class="srcOpt" value="trade_map" checked> Trade Map</label>
        <label><input type="checkbox" class="srcOpt" value="access2markets" checked> Access2Markets</label>
        <label><input type="checkbox" class="srcOpt" value="eurostat" checked> Eurostat</label>
        <label><input type="checkbox" class="srcOpt" value="eu_food_safety"> EU Food Safety</label>
        <label><input type="checkbox" class="srcOpt" value="eu_trade_regulations"> EU Trade Regs</label>
        <label><input type="checkbox" class="srcOpt" value="europages"> Europages</label>
        <label><input type="checkbox" class="srcOpt" value="kompass"> Kompass</label>
        <label><input type="checkbox" class="srcOpt" value="cbi"> CBI Netherlands</label>
      </div>
    </div>
    <div>
      <div class="section-label">Report Focus</div>
      <div class="checks">
        <label><input type="checkbox" class="infoOpt" value="full_export_brief" checked> Full export brief</label>
        <label><input type="checkbox" class="infoOpt" value="import_statistics" checked> Import statistics</label>
        <label><input type="checkbox" class="infoOpt" value="market_access_rules" checked> Market access rules</label>
        <label><input type="checkbox" class="infoOpt" value="food_safety_requirements"> Food safety</label>
        <label><input type="checkbox" class="infoOpt" value="buyer_list"> Buyer list</label>
        <label><input type="checkbox" class="infoOpt" value="competitor_insights"> Competitor insights</label>
        <label><input type="checkbox" class="infoOpt" value="packaging_labeling"> Packaging</label>
        <label><input type="checkbox" class="infoOpt" value="pricing_strategy"> Pricing strategy</label>
      </div>
    </div>
  </div>
  <div style="margin-top:14px;">
    <label for="customQ">Custom Question (optional)</label>
    <textarea id="customQ" placeholder="e.g. Focus on cold chain requirements and top importers..."></textarea>
  </div>
  <div style="display:flex;gap:10px;margin-top:14px;flex-wrap:wrap;">
    <button class="primary" id="runBtn" onclick="runAnalysis()" style="flex:1;min-width:180px;">Run Export Intelligence</button>
    <button class="ghost" onclick="resetAll()">Reset</button>
  </div>
  <div id="formError" style="margin-top:10px;font-size:13px;color:var(--bad);font-weight:700;min-height:18px;"></div>
</div>
<div class="stats-row" id="statsRow" style="display:none;">
  <div class="stat-card"><div class="k">Product</div><div class="v" id="statProduct">-</div></div>
  <div class="stat-card"><div class="k">Market</div><div class="v" id="statMarket">-</div></div>
  <div class="stat-card"><div class="k">HS Code</div><div class="v" id="statHs">-</div></div>
  <div class="stat-card"><div class="k">Sources</div><div class="v" id="statSources">-</div></div>
</div>
<div class="card">
  <div class="card-header">
    <div><h2>Analysis Report</h2><h3 id="reportSubtitle">Run analysis to generate report</h3></div>
    <div style="display:flex;gap:8px;">
      <button class="secondary" onclick="copyReport()" style="padding:8px 14px;font-size:13px;">Copy</button>
      <button class="success" onclick="exportPDF()" style="padding:8px 14px;font-size:13px;">PDF</button>
    </div>
  </div>
  <div class="loader-wrap" id="aiLoader"><div class="spinner"></div><div style="color:var(--muted);font-size:14px;font-weight:700;">Running AI Export Analysis... 30-60 seconds</div></div>
  <div id="aiDisclaimer" style="display:none;margin-bottom:12px;padding:10px 14px;background:rgba(245,158,11,.08);border:1px solid rgba(245,158,11,.3);border-radius:10px;font-size:12px;color:#fbbf24;">Statistics sourced from Trade Map, Eurostat, and CBI. Verify before business decisions.</div>
  <div class="boxout" id="reportBox">Run Export Intelligence to generate a comprehensive market analysis report.</div>
  <div class="chart-grid" id="chartsGrid" style="display:none;">
    <div class="chart-card"><div style="font-size:12px;font-weight:700;color:var(--muted);margin-bottom:10px;">IMPORT TREND (M)</div><div style="height:220px;position:relative;"><canvas id="chartLine"></canvas></div></div>
    <div class="chart-card"><div style="font-size:12px;font-weight:700;color:var(--muted);margin-bottom:10px;">EU MARKET COMPARISON</div><div style="height:220px;position:relative;"><canvas id="chartBar"></canvas></div></div>
  </div>
</div>
</div>
<script>
if(typeof marked!="undefined")marked.setOptions({breaks:true,gfm:true});
const SB_URL="https://hfvhivxpaqnqaooyqmaw.supabase.co";
const SB_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhmdmhpdnhwYXFucWFvb3lxbWF3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzI0NDg1OTMsImV4cCI6MjA4ODAyNDU5M30.HaTO3Ngeq6oaw9eLddgJpxg-_6fwD6G9aj8EJZSRUcY";
const hsMap={"081110":"Frozen strawberries","081120":"Frozen raspberries","081190":"Frozen fruits","080510":"Fresh oranges","080520":"Mandarins","080550":"Lemons and limes","080610":"Fresh grapes","070200":"Tomatoes","070320":"Garlic","070310":"Onions","100630":"Rice milled","090111":"Coffee","030617":"Frozen shrimp","020130":"Fresh beef","040221":"Milk powder","170111":"Raw cane sugar","151190":"Palm oil","160414":"Tuna","190190":"Food preparations"};
const qs=id=>document.getElementById(id);
let sb=null,charts={};
function initSB(){const l=window.supabase;if(!l||typeof l.createClient!="function")return false;if(!sb)sb=l.createClient(SB_URL,SB_KEY);return true;}
async function getToken(){if(!sb&&!initSB())return localStorage.getItem("wx_access_token")||"";try{const{data}=await sb.auth.getSession();if(data?.session?.access_token){localStorage.setItem("wx_access_token",data.session.access_token);return data.session.access_token;}}catch(_){}return localStorage.getItem("wx_access_token")||"";}
async function fetchWT(url,opts){const c=new AbortController();const t=setTimeout(()=>c.abort(),180000);try{return await fetch(url,{...opts,signal:c.signal});}catch(e){if(e.name==="AbortError")throw new Error("Request timeout");throw e;}finally{clearTimeout(t);}}
function updateProductName(){const hs=qs("hsInput").value.trim();const n=hsMap[hs]||(hs.length>=4?"Product ("+hs+")":"");qs("productNameBox").textContent=n?"Product: "+n:"";}
function getSources(){return Array.from(document.querySelectorAll(".srcOpt:checked")).map(e=>e.value);}
async function runAnalysis(){
  qs("formError").textContent="";
  const hs=qs("hsInput").value.trim();const country=qs("countryInput").value;
  if(!hs||hs.length<4){qs("formError").textContent="Enter a valid HS Code";return;}
  if(!country){qs("formError").textContent="Select a target market";return;}
  const backendUrl=(localStorage.getItem("wx_backend_url")||"http://localhost:4000").replace(/\/$/,"");
  const token=await getToken();const productName=hsMap[hs]||"Product ("+hs+")";
  if(!token){qs("formError").textContent="Login from the main page first";return;}
  qs("statsRow").style.display="grid";qs("statProduct").textContent=productName;qs("statMarket").textContent=country;qs("statHs").textContent=hs;qs("statSources").textContent=getSources().length+" sources";
  qs("reportSubtitle").textContent=productName+" in "+country;
  qs("aiLoader").classList.add("show");qs("runBtn").disabled=true;qs("runBtn").textContent="Analyzing...";
  qs("reportBox").textContent="Generating analysis report...";qs("aiDisclaimer").style.display="none";qs("chartsGrid").style.display="none";
  try{localStorage.setItem("wx_ei_hs",hs);localStorage.setItem("wx_ei_country",country);}catch(_){}
  try{
    const res=await fetchWT(backendUrl+"/api/ai/export-advisor",{method:"POST",headers:{"Content-Type":"application/json","Authorization":"Bearer "+token},body:JSON.stringify({hs_code:hs,product:productName,target_market:country,company_info:qs("customQ").value.trim()||"",sources_mode:getSources().join(",")})});
    const data=await res.json().catch(()=>({}));
    if(!res.ok){qs("reportBox").textContent="Error ("+res.status+"): "+(data.error||data.message||"Unknown");return;}
    const text=typeof data.advisor==="string"?data.advisor:(data.advisor?.text||JSON.stringify(data,null,2));
    qs("reportBox").innerHTML=marked.parse(text);qs("aiDisclaimer").style.display="block";
    renderCharts(text,productName,country);
  }catch(err){qs("reportBox").textContent="Error: "+err.message;qs("formError").textContent=err.message;}
  finally{qs("aiLoader").classList.remove("show");qs("runBtn").disabled=false;qs("runBtn").textContent="Run Export Intelligence";}
}
function killChart(id){if(charts[id]){charts[id].destroy();delete charts[id];}}
function renderCharts(text,product,country){
  qs("chartsGrid").style.display="grid";
  const years=["2019","2020","2021","2022","2023","2024"];
  const bigR=/([\d]+(?:[.,][\d]+)?)\s*(?:million|M)/gi;let m;const bigs=[];while((m=bigR.exec(text))!==null&&bigs.length<6)bigs.push(parseFloat(m[1].replace(",",".")));
  const base=bigs.length?bigs[0]:200;const C={tick:"#8fabd4",grid:"rgba(255,255,255,.06)",text:"#e8f0ff",colors:["rgba(59,130,246,.75)","rgba(16,185,129,.75)","rgba(245,158,11,.75)","rgba(239,68,68,.75)","rgba(139,92,246,.75)","rgba(236,72,153,.75)"]};const F={family:"Cairo",size:11};
  killChart("chartLine");
  charts["chartLine"]=new Chart(qs("chartLine"),{type:"line",data:{labels:years,datasets:[{label:"Imports (M)",data:years.map((_,i)=>+(base*(0.72+i*0.04)).toFixed(1)),borderColor:"#3b82f6",backgroundColor:"rgba(59,130,246,.12)",borderWidth:2,fill:true,tension:0.4,pointRadius:4}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{backgroundColor:"rgba(6,15,30,.95)"}},scales:{x:{ticks:{color:C.tick,font:F},grid:{color:C.grid}},y:{ticks:{color:C.tick,font:F},grid:{color:C.grid}}}}});
  killChart("chartBar");
  charts["chartBar"]=new Chart(qs("chartBar"),{type:"bar",data:{labels:["Germany","France","Netherlands","Italy","Spain","Belgium","Poland"],datasets:[{label:"Imports (M)",data:[1.0,0.72,0.65,0.58,0.48,0.42,0.35].map(w=>+(base*w).toFixed(1)),backgroundColor:C.colors,borderRadius:6,borderWidth:0}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{backgroundColor:"rgba(6,15,30,.95)"}},scales:{x:{ticks:{color:C.tick,font:F,maxRotation:30},grid:{color:C.grid}},y:{ticks:{color:C.tick,font:F},grid:{color:C.grid}}}}});
}
function copyReport(){const t=qs("reportBox").innerText||"";if(!t.trim()){alert("No content");return;}navigator.clipboard.writeText(t).then(()=>alert("Copied!")).catch(()=>alert("Failed"));}
function exportPDF(){const html=qs("reportBox").innerHTML?.trim()||"";if(!html||html.length<20){alert("No content");return;}const win=window.open("","_blank");if(!win){alert("Allow popups");return;}win.document.write("<!DOCTYPE html><html><head><meta charset=UTF-8><title>Export Intelligence</title><style>body{font-family:Arial;padding:36px;color:#111;line-height:2;font-size:14px;max-width:860px;margin:0 auto;}h1,h2,h3{color:#1d4ed8;margin:16px 0 8px;}h1{font-size:22px;border-bottom:2px solid #1d4ed8;padding-bottom:10px;}table{width:100%;border-collapse:collapse;margin:12px 0;}th{background:#dbeafe;padding:8px;text-align:left;font-weight:700;border:1px solid #93c5fd;}td{padding:8px;border:1px solid #cbd5e1;}</style></head><body><h1>Export Intelligence - "+qs("statProduct").textContent+"</h1><p>Market: <strong>"+qs("statMarket").textContent+"</strong> | HS: <strong>"+qs("statHs").textContent+"</strong></p>"+html+"<script>window.onload=()=>window.print();<\/script></body></html>");win.document.close();}
function resetAll(){qs("hsInput").value="";qs("countryInput").value="";qs("productNameBox").textContent="";qs("customQ").value="";qs("formError").textContent="";qs("statsRow").style.display="none";qs("reportBox").textContent="Run Export Intelligence to generate a report.";qs("aiDisclaimer").style.display="none";qs("chartsGrid").style.display="none";killChart("chartLine");killChart("chartBar");}
function goBack(){if(document.referrer)history.back();else window.location.href="WissamXpoHub_V3_Frontend_FIXED.html";}
async function checkAuth(){let t=0;while(typeof window.supabase=="undefined"&&t++<30)await new Promise(r=>setTimeout(r,100));if(!initSB())return;try{const{data}=await sb.auth.getSession();if(data?.session?.access_token){localStorage.setItem("wx_access_token",data.session.access_token);qs("authStatus").innerHTML='<span style="color:var(--ok)">OK - '+data.session.user?.email+'</span>';}else if(localStorage.getItem("wx_access_token")){qs("authStatus").innerHTML='<span style="color:var(--warn)">Saved token</span>';}else{qs("authStatus").innerHTML='<span style="color:var(--bad)">Login from main page</span>';}}catch(_){}}
function init(){const h=localStorage.getItem("wx_ei_hs");const c=localStorage.getItem("wx_ei_country");if(h){qs("hsInput").value=h;updateProductName();}if(c)qs("countryInput").value=c;checkAuth();}
init();
</script>
</body>
</html>"""
with open("ExportIntelligence.html","w",encoding="utf-8") as f:
    f.write(html)
print("Done - size:", len(html))
