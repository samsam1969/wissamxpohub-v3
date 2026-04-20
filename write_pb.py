html = r"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<meta http-equiv="Cache-Control" content="no-cache,no-store,must-revalidate"/>
<title>Potential Buyers — WissamXpoHub</title>
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&display=swap" rel="stylesheet"/>
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
<style>
:root{--bg:#060f1e;--bg2:#071326;--line:#1e3a6e;--line2:#2d5aa8;--text:#e8f0ff;--muted:#8fabd4;--ok:#4ade80;--bad:#f87171;--warn:#fbbf24;--btn:#1d4ed8;--btn2:#1e293b;--radius:18px;--shadow:0 8px 32px rgba(0,0,0,.35);}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
html,body{min-height:100%;font-family:'Cairo',Arial,sans-serif;background:linear-gradient(160deg,var(--bg) 0%,var(--bg2) 50%,#08172e 100%);background-attachment:fixed;color:var(--text);overflow-x:hidden;}
.wrap{max-width:1400px;margin:0 auto;padding:20px;}
.top-nav{display:flex;align-items:center;justify-content:space-between;gap:16px;padding:14px 20px;background:rgba(12,26,51,.97);border:1px solid var(--line);border-radius:var(--radius);margin-bottom:20px;flex-wrap:wrap;}
.nav-brand{font-size:18px;font-weight:800;}.nav-brand span{color:#60a5fa;}
.card{background:linear-gradient(160deg,rgba(12,26,51,.97),rgba(8,20,44,.97));border:1px solid var(--line);border-radius:var(--radius);padding:20px;box-shadow:var(--shadow);}
.card-header{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:16px;flex-wrap:wrap;}
h2{font-size:22px;font-weight:800;}h3{font-size:15px;color:var(--muted);font-weight:600;}
label{display:block;margin:12px 0 7px;color:var(--text);font-weight:700;font-size:15px;}
input,select{width:100%;border-radius:14px;border:1px solid var(--line);background:rgba(0,0,0,.3);color:#fff;padding:14px 16px;font-size:15px;font-family:'Cairo',Arial,sans-serif;outline:none;transition:border-color .15s;}
input:focus,select:focus{border-color:var(--line2);box-shadow:0 0 0 3px rgba(45,90,168,.25);}
input::placeholder{color:var(--muted);}select option{background:#0c1a33;}
button{border:none;border-radius:14px;padding:13px 20px;font-size:15px;font-weight:800;font-family:'Cairo',Arial,sans-serif;cursor:pointer;color:#fff;transition:transform .13s,filter .13s;box-shadow:0 6px 16px rgba(0,0,0,.22);}
button:hover{transform:translateY(-2px);filter:brightness(1.1);}button:active{transform:scale(.97);}
button:disabled{opacity:.55;cursor:not-allowed;transform:none;filter:none;}
.primary{background:var(--btn);}.secondary{background:var(--btn2);}.ghost{background:rgba(255,255,255,.06);border:1px solid var(--line);}
.product-box{margin-top:8px;color:var(--warn);font-size:17px;font-weight:800;}
.hint{color:var(--muted);margin-top:8px;font-size:13px;line-height:1.8;}
.stats-row{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:18px;}
.stat-card{background:rgba(0,0,0,.3);border:1px solid var(--line);border-radius:14px;padding:14px;text-align:center;}
.stat-card .k{color:var(--muted);font-size:10px;font-weight:700;letter-spacing:1px;text-transform:uppercase;margin-bottom:6px;}
.stat-card .v{font-size:17px;font-weight:800;}
.loader-wrap{display:none;align-items:center;gap:12px;margin-bottom:14px;padding:12px 16px;border:1px solid var(--line);background:rgba(0,0,0,.25);border-radius:14px;}
.loader-wrap.show{display:flex;}
.spinner{width:18px;height:18px;border:3px solid rgba(255,255,255,.12);border-top-color:#60a5fa;border-radius:50%;animation:spin .9s linear infinite;flex-shrink:0;}
@keyframes spin{to{transform:rotate(360deg);}}
.opp-table{width:100%;border-collapse:collapse;font-size:13px;}
.opp-table th{background:rgba(0,0,0,.35);color:var(--muted);font-size:11px;letter-spacing:.8px;text-transform:uppercase;padding:10px 12px;text-align:right;border-bottom:1px solid var(--line);}
.opp-table td{padding:11px 12px;border-bottom:1px solid rgba(255,255,255,.05);vertical-align:middle;}
.opp-table tr:hover td{background:rgba(255,255,255,.03);}
.rank-badge{width:24px;height:24px;border-radius:50%;display:inline-flex;align-items:center;justify-content:center;font-size:11px;font-weight:800;background:rgba(59,130,246,.2);color:#93c5fd;border:1px solid rgba(59,130,246,.4);}
.rank-badge.gold{background:rgba(245,158,11,.2);color:#fbbf24;border-color:rgba(245,158,11,.4);}
.rank-badge.silver{background:rgba(156,163,175,.2);color:#d1d5db;border-color:rgba(156,163,175,.4);}
.rank-badge.bronze{background:rgba(180,83,9,.2);color:#fdba74;border-color:rgba(180,83,9,.4);}
.buyer-action{font-size:11px;font-weight:700;padding:4px 10px;border-radius:6px;background:rgba(16,185,129,.15);color:#6ee7b7;border:1px solid rgba(16,185,129,.3);cursor:pointer;white-space:nowrap;box-shadow:none;}
.buyer-action:hover{background:rgba(16,185,129,.28);transform:none;}
.website-link{color:#7eb3ff;font-size:12px;font-weight:700;}
.empty-state{text-align:center;padding:50px 20px;color:var(--muted);font-size:14px;line-height:2.2;}
.empty-state .icon{font-size:44px;margin-bottom:12px;}
.section-label{font-size:12px;font-weight:700;color:var(--muted);letter-spacing:1.5px;text-transform:uppercase;margin:16px 0 10px;padding-bottom:6px;border-bottom:1px solid var(--line);}
.src-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;}
.src-card{background:rgba(0,0,0,.25);border:1px solid var(--line);border-radius:14px;padding:14px;transition:border-color .15s;}
.src-card:hover{border-color:var(--line2);}
.src-header{display:flex;align-items:center;gap:10px;margin-bottom:8px;font-size:14px;font-weight:700;}
.src-badge{font-size:10px;font-weight:800;padding:3px 8px;border-radius:999px;letter-spacing:.5px;flex-shrink:0;}
.src-badge.eu{background:rgba(29,78,216,.3);color:#93c5fd;border:1px solid #1d4ed8;}
.src-badge.b2b{background:rgba(139,92,246,.2);color:#c4b5fd;border:1px solid #8b5cf6;}
.src-desc{font-size:13px;color:var(--muted);line-height:1.6;margin-bottom:8px;}
.src-meta{display:flex;gap:12px;font-size:11px;color:var(--muted);margin-bottom:8px;font-weight:600;}
.src-link{font-size:12px;font-weight:700;color:#7eb3ff;}
a{color:#7eb3ff;text-decoration:none;font-weight:700;}a:hover{text-decoration:underline;}
@media(max-width:900px){.stats-row{grid-template-columns:1fr 1fr;}.src-grid{grid-template-columns:1fr 1fr;}}
@media(max-width:600px){.stats-row{grid-template-columns:1fr 1fr;}.src-grid{grid-template-columns:1fr;}.opp-table{font-size:12px;}}
</style>
</head>
<body>
<div class="wrap">
<nav class="top-nav">
  <div style="display:flex;align-items:center;gap:14px;flex-wrap:wrap;">
    <button class="ghost" onclick="goBack()" style="padding:9px 16px;font-size:13px;border-radius:10px;">&#8592; العودة</button>
    <div class="nav-brand">WissamXpoHub <span>/ Potential Buyers</span></div>
  </div>
  <div id="authStatus" style="font-size:13px;color:var(--muted);font-weight:600;">جارٍ التحقق...</div>
</nav>
<div class="card" style="margin-bottom:18px;">
  <div class="card-header">
    <div><h2>&#128270; بحث عن المشترين المحتملين</h2><h3>أدخل HS Code واختر السوق المستهدف</h3></div>
  </div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:18px;">
    <div>
      <label for="hsInput">HS Code <span style="color:var(--bad)">*</span></label>
      <input id="hsInput" placeholder="مثال: 081110" maxlength="10" oninput="updateProductName()"/>
      <div class="product-box" id="productNameBox">&#8212;</div>
      <div class="hint">لا تعرف الكود؟ <a href="https://www.trademap.org/" target="_blank">ابحث في Trade Map</a></div>
    </div>
    <div>
      <label for="countryInput">EU Country <span style="color:var(--bad)">*</span></label>
      <select id="countryInput">
        <option value="">&#8212; اختر الدولة &#8212;</option>
        <optgroup label="Top Markets">
          <option value="Germany">Germany</option><option value="France">France</option>
          <option value="Netherlands">Netherlands</option><option value="Italy">Italy</option>
          <option value="Spain">Spain</option><option value="Belgium">Belgium</option>
          <option value="Poland">Poland</option>
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
  <div style="display:flex;gap:10px;margin-top:16px;flex-wrap:wrap;">
    <button class="primary" id="searchBtn" onclick="runSearch()" style="flex:1;min-width:160px;">&#128269; بحث عن المشترين</button>
    <button class="ghost" onclick="resetSearch()">Reset</button>
  </div>
  <div id="formError" style="margin-top:10px;font-size:13px;color:var(--bad);min-height:18px;font-weight:700;"></div>
</div>
<div class="stats-row" id="statsRow" style="display:none;">
  <div class="stat-card"><div class="k">المنتج</div><div class="v" id="statProduct">&#8212;</div></div>
  <div class="stat-card"><div class="k">السوق</div><div class="v" id="statMarket">&#8212;</div></div>
  <div class="stat-card"><div class="k">HS Code</div><div class="v" id="statHs">&#8212;</div></div>
  <div class="stat-card"><div class="k">المشترين</div><div class="v" id="statCount">&#8212;</div></div>
</div>
<div class="card">
  <div class="card-header">
    <div><h2>&#127970; Potential Buyers</h2><h3 id="resultsSubtitle">قائمة المشترين المحتملين</h3></div>
    <div style="display:flex;gap:8px;flex-wrap:wrap;">
      <button class="secondary" onclick="exportBuyersPDF()">&#128196; PDF</button>
      <button class="secondary" onclick="exportBuyersCSV()">&#128442; CSV</button>
    </div>
  </div>
  <div class="loader-wrap" id="searchLoader"><div class="spinner"></div><div style="color:var(--muted);font-size:14px;font-weight:700;">جارٍ البحث...</div></div>
  <div style="margin-bottom:14px;"><input type="text" id="buyerSearch" placeholder="&#128269; فلترة بالاسم أو الدولة..." oninput="filterTable(this.value)" style="padding:10px 14px;background:rgba(0,0,0,.3);border:1px solid var(--line);border-radius:12px;color:var(--text);font-size:13px;font-family:inherit;outline:none;"/></div>
  <div style="overflow-x:auto;">
    <table class="opp-table">
      <thead><tr><th>#</th><th>Company Name</th><th>Country</th><th>Importer Type</th><th>Import Volume</th><th>التواصل</th></tr></thead>
      <tbody id="buyersTableBody"><tr><td colspan="6"><div class="empty-state"><div class="icon">&#128270;</div><div>أدخل <strong>HS Code</strong> واختر <strong>الدولة</strong> ثم اضغط بحث</div></div></td></tr></tbody>
    </table>
  </div>
  <div style="margin-top:14px;font-size:12px;color:var(--muted);line-height:1.9;">&#128161; النتائج مولّدة بواسطة AI — Europages, Kompass, WLW, LinkedIn, Trade Map.</div>
</div>
<div class="card" style="margin-top:18px;">
  <div class="card-header"><h2>&#128218; مصادر البيانات</h2><h3>B2B Buyer Discovery Sources</h3></div>
  <div class="src-grid">
    <div class="src-card"><div class="src-header"><span class="src-badge b2b">B2B</span><a href="https://www.europages.com/" target="_blank">Europages</a></div><div class="src-desc">أكبر دليل أعمال أوروبي — 3M+ شركة</div><div class="src-meta"><span>Free</span></div><a href="https://www.europages.com/" target="_blank" class="src-link">europages.com</a></div>
    <div class="src-card"><div class="src-header"><span class="src-badge b2b">B2B</span><a href="https://www.kompass.com/" target="_blank">Kompass</a></div><div class="src-desc">دليل شركات دولي — 75+ دولة</div><div class="src-meta"><span>Freemium</span></div><a href="https://www.kompass.com/" target="_blank" class="src-link">kompass.com</a></div>
    <div class="src-card"><div class="src-header"><span class="src-badge b2b">B2B</span><a href="https://www.wlw.com/" target="_blank">WLW Europe</a></div><div class="src-desc">B2B أوروبي — DACH Region</div><div class="src-meta"><span>Free</span></div><a href="https://www.wlw.com/" target="_blank" class="src-link">wlw.com</a></div>
    <div class="src-card"><div class="src-header"><span class="src-badge eu">EU</span><a href="https://www.trademap.org/" target="_blank">ITC Trade Map</a></div><div class="src-desc">إحصاءات التجارة — HS Code</div><div class="src-meta"><span>2024</span></div><a href="https://www.trademap.org/" target="_blank" class="src-link">trademap.org</a></div>
    <div class="src-card"><div class="src-header"><span class="src-badge b2b">B2B</span><a href="https://www.linkedin.com/search/results/companies/" target="_blank">LinkedIn</a></div><div class="src-desc">بحث مباشر عن الشركات المستوردة</div><div class="src-meta"><span>Freemium</span></div><a href="https://www.linkedin.com/search/results/companies/" target="_blank" class="src-link">linkedin.com</a></div>
    <div class="src-card"><div class="src-header"><span class="src-badge eu">EU</span><a href="https://trade.ec.europa.eu/access-to-markets/" target="_blank">Access2Markets</a></div><div class="src-desc">متطلبات الدخول للسوق الأوروبي</div><div class="src-meta"><span>2024</span></div><a href="https://trade.ec.europa.eu/access-to-markets/" target="_blank" class="src-link">trade.ec.europa.eu</a></div>
  </div>
</div>
</div>
<script>
const SB_URL="https://hfvhivxpaqnqaooyqmaw.supabase.co";
const SB_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhmdmhpdnhwYXFucWFvb3lxbWF3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzI0NDg1OTMsImV4cCI6MjA4ODAyNDU5M30.HaTO3Ngeq6oaw9eLddgJpxg-_6fwD6G9aj8EJZSRUcY";
const hsMap={"081110":"Frozen strawberries","081120":"Frozen raspberries","081190":"Frozen fruits (other)","080510":"Fresh oranges","080520":"Mandarins","080550":"Lemons & limes","080610":"Fresh grapes","070200":"Tomatoes","070320":"Garlic","070310":"Onions","100630":"Rice (milled)","090111":"Coffee","030617":"Frozen shrimp","020130":"Fresh beef","040221":"Milk powder","170111":"Raw cane sugar","151190":"Palm oil","160414":"Tuna","190190":"Food preparations"};
const qs=id=>document.getElementById(id);
let sb=null,buyersData=[];
function initSB(){const l=window.supabase;if(!l||typeof l.createClient!=="function")return false;if(!sb)sb=l.createClient(SB_URL,SB_KEY);return true;}
async function getToken(){if(!sb&&!initSB())return localStorage.getItem("wx_access_token")||"";try{const{data}=await sb.auth.getSession();if(data?.session?.access_token){localStorage.setItem("wx_access_token",data.session.access_token);return data.session.access_token;}}catch(_){}return localStorage.getItem("wx_access_token")||"";}
async function fetchWT(url,opts){const c=new AbortController();const t=setTimeout(()=>c.abort(),180000);try{return await fetch(url,{...opts,signal:c.signal});}catch(e){if(e.name==="AbortError")throw new Error("انتهت المهلة");throw e;}finally{clearTimeout(t);}}
function updateProductName(){const hs=qs("hsInput").value.trim();const n=hsMap[hs]||(hs.length>=4?"Product ("+hs+")":"—");qs("productNameBox").textContent=hs?"اسم المنتج: "+n:"—";}
function parseBuyers(text){const buyers=[];const lines=text.split("\n");let inT=false;for(const line of lines){const l=line.trim();if(!l.startsWith("|")){inT=false;continue;}if(l.replace(/[\s|:-]/g,"")===""){inT=true;continue;}const cells=l.split("|").map(c=>c.trim()).filter(Boolean);if(!cells.length||!inT){inT=true;continue;}const o={rank:buyers.length+1,name:"",activity:"",city:"",website:"",note:""};cells.forEach((cell,i)=>{const lo=cell.toLowerCase();if(i===0&&/^\d+$/.test(cell)){o.rank=parseInt(cell);return;}if(lo.includes(".com")||lo.includes(".eu")||lo.includes(".de")||lo.includes(".fr")||lo.includes(".nl")||lo.includes("http")||lo.includes("www")){o.website=cell.replace(/^https?:\/\//,"").split("/")[0];return;}if(cell.length>10&&(lo.includes("import")||lo.includes("distribut")||lo.includes("wholesale")||cell.includes("استيراد")||cell.includes("توزيع"))){o.activity=cell;return;}if(!o.name&&cell.length>2){o.name=cell;return;}if(!o.activity&&cell.length>5){o.activity=cell;return;}if(!o.city&&cell.length<40){o.city=cell;return;}o.note+=(o.note?" | ":"")+cell;});if(o.name&&o.name.length>1)buyers.push(o);}if(!buyers.length)(text.match(/\d+\.\s+\*{0,2}([^\n*]+)\*{0,2}/g)||[]).forEach((item,i)=>{const c=item.replace(/^\d+\.\s+\**/,"").replace(/\*+$/,"").trim();if(c.length>3)buyers.push({rank:i+1,name:c,activity:"",city:"",website:"",note:""});});return buyers;}
function renderTable(buyers){buyersData=buyers;const tbody=qs("buyersTableBody");if(!buyers.length){tbody.innerHTML='<tr><td colspan="6"><div class="empty-state"><div class="icon">📭</div><div>لم يُعثر على مشترين — جرّب دولة أو HS Code مختلف.</div></div></td></tr>';return;}tbody.innerHTML=buyers.map((b,i)=>{const badge=["🥇","🥈","🥉"][i]||(i+1);const bc=i<3?["gold","silver","bronze"][i]:"";const site=b.website?'<a href="https://'+b.website+'" target="_blank" class="website-link">'+b.website+' ↗</a>':"—";return'<tr><td><span class="rank-badge '+bc+'">'+badge+'</span></td><td><strong>'+b.name+'</strong><br><small style="color:var(--muted);font-size:11px;">'+site+'</small></td><td style="font-size:12px;">'+(b.city||"—")+'</td><td style="font-size:12px;">'+(b.activity||"—")+'</td><td style="font-size:12px;color:var(--muted);">'+(b.note||"—")+'</td><td style="white-space:nowrap;"><button class="buyer-action" onclick="window.open(\'https://www.linkedin.com/search/results/companies/?keywords='+encodeURIComponent(b.name)+'\',\'_blank\')">🔗 LinkedIn</button></td></tr>';}).join("");}
function filterTable(q){const query=(q||"").toLowerCase();if(!query){renderTable(buyersData);return;}const f=buyersData.filter(b=>[b.name,b.city,b.activity,b.website].some(v=>(v||"").toLowerCase().includes(query)));const tbody=qs("buyersTableBody");if(!f.length){tbody.innerHTML='<tr><td colspan="6" style="text-align:center;padding:20px;color:var(--muted);">لا توجد نتائج</td></tr>';return;}tbody.innerHTML=f.map((b,i)=>{const site=b.website?'<a href="https://'+b.website+'" target="_blank" class="website-link">'+b.website+' ↗</a>':"—";return'<tr><td>'+(i+1)+'</td><td><strong>'+b.name+'</strong><br><small style="color:var(--muted);font-size:11px;">'+site+'</small></td><td style="font-size:12px;">'+(b.city||"—")+'</td><td style="font-size:12px;">'+(b.activity||"—")+'</td><td style="font-size:12px;color:var(--muted);">'+(b.note||"—")+'</td><td><button class="buyer-action" onclick="window.open(\'https://www.linkedin.com/search/results/companies/?keywords='+encodeURIComponent(b.name)+'\',\'_blank\')">🔗 LinkedIn</button></td></tr>';}).join("");}
async function runSearch(){qs("formError").textContent="";const hs=qs("hsInput").value.trim();const country=qs("countryInput").value;if(!hs||hs.length<4){qs("formError").textContent="⚠ أدخل HS Code صحيح (4-6 أرقام)";return;}if(!country){qs("formError").textContent="⚠ اختر الدولة المستهدفة";return;}const backendUrl=(localStorage.getItem("wx_backend_url")||"http://localhost:4000").replace(/\/$/,"");const token=await getToken();const productName=hsMap[hs]||"Product ("+hs+")";if(!token){qs("formError").textContent="⚠ سجّل الدخول من الصفحة الرئيسية أولاً";return;}qs("statsRow").style.display="grid";qs("statProduct").textContent=productName;qs("statMarket").textContent=country;qs("statHs").textContent=hs;qs("statCount").textContent="جارٍ...";qs("resultsSubtitle").textContent=productName+" → "+country;qs("searchLoader").classList.add("show");qs("searchBtn").disabled=true;qs("searchBtn").textContent="جارٍ البحث...";qs("buyersTableBody").innerHTML='<tr><td colspan="6" style="text-align:center;padding:30px;color:var(--muted);">⏳ جارٍ البحث في مصادر B2B...</td></tr>';try{const res=await fetchWT(backendUrl+"/api/ai/export-advisor",{method:"POST",headers:{"Content-Type":"application/json","Authorization":"Bearer "+token},body:JSON.stringify({hs_code:hs,product:productName,target_market:country,company_info:'Focus EXCLUSIVELY on finding potential buyers, importers, and distributors for "'+productName+'" (HS: '+hs+') in '+country+'. Provide a markdown table with 10-15 potential buyers: Company Name, Country/City, Importer Type, Import Volume estimate, Website. Sources: Europages, Kompass, WLW, LinkedIn, Trade Map.',sources_mode:"europages,kompass,wlw,linkedin_companies,google_b2b,trade_map"})});const data=await res.json().catch(()=>({}));if(!res.ok){qs("formError").textContent="خطأ ("+res.status+"): "+(data.error||"Unknown");qs("buyersTableBody").innerHTML='<tr><td colspan="6" style="text-align:center;padding:20px;color:var(--bad);">خطأ: '+(data.error||res.status)+'</td></tr>';return;}const text=typeof data.advisor==="string"?data.advisor:(data.advisor?.text||JSON.stringify(data));const buyers=parseBuyers(text);try{localStorage.setItem("wx_buyers_data",JSON.stringify(buyers));localStorage.setItem("wx_buyers_product",productName);localStorage.setItem("wx_buyers_market",country);localStorage.setItem("wx_buyers_hs",hs);}catch(_){}renderTable(buyers);qs("statCount").textContent=buyers.length?buyers.length+" مشترٍ":"0";}catch(err){qs("formError").textContent="خطأ: "+err.message;qs("buyersTableBody").innerHTML='<tr><td colspan="6" style="text-align:center;padding:20px;color:var(--bad);">خطأ: '+err.message+'</td></tr>';}finally{qs("searchLoader").classList.remove("show");qs("searchBtn").disabled=false;qs("searchBtn").textContent="🔍 بحث عن المشترين";}}
function exportBuyersPDF(){if(!buyersData.length){alert("لا توجد بيانات");return;}const rows=buyersData.map((b,i)=>"<tr><td>"+(i+1)+"</td><td><strong>"+b.name+"</strong></td><td>"+(b.city||"—")+"</td><td>"+(b.activity||"—")+"</td><td>"+(b.note||"—")+"</td><td>"+(b.website||"—")+"</td></tr>").join("");const win=window.open("","_blank");if(!win){alert("السماح بالـ popups");return;}win.document.write('<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8"><title>Buyers</title><style>body{font-family:Arial;direction:rtl;padding:30px;color:#111;}h1{font-size:20px;color:#1d4ed8;border-bottom:2px solid #1d4ed8;padding-bottom:8px;}table{width:100%;border-collapse:collapse;font-size:13px;}th{background:#dbeafe;padding:9px 12px;text-align:right;font-weight:700;border:1px solid #93c5fd;}td{padding:8px 12px;border:1px solid #e5e7eb;}</style></head><body><h1>Potential Buyers — '+qs("statProduct").textContent+'</h1><p>السوق: '+qs("statMarket").textContent+' | HS: '+qs("statHs").textContent+' | '+buyersData.length+' مشترٍ</p><table><thead><tr><th>#</th><th>الشركة</th><th>الدولة</th><th>النشاط</th><th>الحجم</th><th>الموقع</th></tr></thead><tbody>'+rows+'</tbody></table><script>window.onload=()=>window.print();<\/script></body></html>');win.document.close();}
function exportBuyersCSV(){if(!buyersData.length){alert("لا توجد بيانات");return;}const csv=[["#","الشركة","النشاط","المدينة","الموقع","ملاحظات"].join(","),...buyersData.map(b=>[b.rank,b.name,b.activity,b.city,b.website,b.note].map(c=>'"'+String(c||"").replace(/"/g,'""')+'"').join(","))].join("\n");const a=document.createElement("a");a.href=URL.createObjectURL(new Blob(["\uFEFF"+csv],{type:"text/csv;charset=utf-8;"}));a.download="buyers_"+qs("statProduct").textContent.replace(/\s+/g,"_")+".csv";a.click();}
function resetSearch(){qs("hsInput").value="";qs("countryInput").value="";qs("productNameBox").textContent="—";qs("formError").textContent="";qs("statsRow").style.display="none";qs("buyerSearch").value="";buyersData=[];qs("buyersTableBody").innerHTML='<tr><td colspan="6"><div class="empty-state"><div class="icon">🔎</div><div>أدخل HS Code واختر الدولة ثم اضغط بحث</div></div></td></tr>';}
function goBack(){if(document.referrer)history.back();else window.location.href="WissamXpoHub_V3_Frontend_FIXED.html";}
async function checkAuth(){let t=0;while(typeof window.supabase==="undefined"&&t++<30)await new Promise(r=>setTimeout(r,100));if(!initSB())return;try{const{data}=await sb.auth.getSession();if(data?.session?.access_token){localStorage.setItem("wx_access_token",data.session.access_token);qs("authStatus").innerHTML='<span style="color:var(--ok)">✓ '+data.session.user?.email+'</span>';}else if(localStorage.getItem("wx_access_token")){qs("authStatus").innerHTML='<span style="color:var(--warn)">⚠ توكن محفوظ</span>';}else{qs("authStatus").innerHTML='<span style="color:var(--bad)">✗ سجّل الدخول من الصفحة الرئيسية</span>';}}catch(_){}}
function init(){const h=localStorage.getItem("wx_pb_hs");const c=localStorage.getItem("wx_pb_country");if(h){qs("hsInput").value=h;updateProductName();}if(c)qs("countryInput").value=c;checkAuth();}
init();
</script>
</body>
</html>"""
with open("PotentialBuyers.html","w",encoding="utf-8") as f:
    f.write(html)
print("PotentialBuyers.html written OK - size:", len(html))
