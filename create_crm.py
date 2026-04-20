html = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8"/>
<title>Admin CRM - WissamXpoHub</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:Cairo,Arial,sans-serif;background:#0f0e17;color:#e2e8f0;min-height:100vh}
.header{background:linear-gradient(135deg,#1e1b4b,#312e81);padding:16px 28px;display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid rgba(99,102,241,.3)}
.header h1{font-size:20px;color:#a5b4fc}
.nav{display:flex;gap:10px}
.nav a{color:#6b7280;text-decoration:none;font-size:13px;padding:6px 12px;border-radius:8px;background:rgba(255,255,255,.05)}
.nav a:hover{color:#a5b4fc;background:rgba(99,102,241,.15)}
.container{max-width:1400px;margin:0 auto;padding:20px}
.stats{display:grid;grid-template-columns:repeat(5,1fr);gap:14px;margin-bottom:20px}
.stat{background:rgba(99,102,241,.08);border:1px solid rgba(99,102,241,.2);border-radius:12px;padding:14px;text-align:center}
.stat-num{font-size:26px;font-weight:800;color:#a5b4fc}
.stat-label{font-size:11px;color:#6b7280;margin-top:3px}
.toolbar{display:flex;gap:10px;margin-bottom:14px;flex-wrap:wrap;align-items:center}
.btn{padding:8px 16px;border-radius:8px;border:none;cursor:pointer;font-family:Cairo,Arial,sans-serif;font-weight:700;font-size:12px}
.btn-primary{background:linear-gradient(135deg,#6366f1,#8b5cf6);color:white}
.btn-success{background:rgba(34,197,94,.2);color:#4ade80;border:1px solid rgba(34,197,94,.3)}
.btn-danger{background:rgba(239,68,68,.2);color:#f87171;border:1px solid rgba(239,68,68,.3)}
.btn-warning{background:rgba(245,158,11,.2);color:#fbbf24;border:1px solid rgba(245,158,11,.3)}
.btn-sm{padding:5px 10px;font-size:11px}
select,input{background:rgba(255,255,255,.05);border:1px solid rgba(99,102,241,.3);border-radius:8px;color:#e2e8f0;padding:7px 11px;font-family:Cairo,Arial,sans-serif;font-size:13px}
table{width:100%;border-collapse:collapse;background:rgba(255,255,255,.02);border-radius:12px;overflow:hidden}
thead{background:rgba(99,102,241,.15)}
th{padding:11px 14px;text-align:right;font-size:11px;color:#a5b4fc;font-weight:700;letter-spacing:.5px}
td{padding:11px 14px;font-size:12px;border-bottom:1px solid rgba(255,255,255,.04);vertical-align:middle}
tr:hover td{background:rgba(99,102,241,.04)}
.plan-badge{display:inline-block;padding:3px 9px;border-radius:99px;font-size:11px;font-weight:700}
.plan-free{background:rgba(107,114,128,.2);color:#9ca3af}
.plan-starter{background:rgba(99,102,241,.2);color:#a5b4fc}
.plan-pro{background:rgba(139,92,246,.2);color:#c4b5fd}
.plan-agency{background:rgba(245,158,11,.2);color:#fcd34d}
.status-active{color:#4ade80}
.status-expired{color:#f87171}
.modal{display:none;position:fixed;inset:0;background:rgba(0,0,0,.8);z-index:999;justify-content:center;align-items:center}
.modal.open{display:flex}
.mbox{background:#1e1b4b;border:1px solid rgba(99,102,241,.4);border-radius:16px;padding:24px;width:90%;max-width:500px}
.mbox h3{color:#a5b4fc;margin-bottom:16px;font-size:16px}
.fg{margin-bottom:12px}
.fg label{display:block;font-size:11px;color:#9ca3af;margin-bottom:4px;font-weight:700}
.fg input,.fg select,.fg textarea{width:100%}
.fg textarea{min-height:80px;resize:vertical}
.mfoot{display:flex;gap:8px;justify-content:flex-end;margin-top:16px}
#toast{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);padding:10px 22px;border-radius:8px;font-weight:700;display:none;z-index:9999;font-size:13px}
</style>
</head>
<body>
<div class="header">
  <h1>👥 Admin CRM — المشتركون</h1>
  <div class="nav">
    <a href="/admin/knowledge">🧠 Knowledge Base</a>
    <a href="/WissamXpoHub_V3_Frontend_FIXED.html">🏠 الداشبورد</a>
  </div>
</div>

<div class="container">
  <div class="stats">
    <div class="stat"><div class="stat-num" id="totalUsers">-</div><div class="stat-label">إجمالي المستخدمين</div></div>
    <div class="stat"><div class="stat-num" id="freeUsers">-</div><div class="stat-label">Free</div></div>
    <div class="stat"><div class="stat-num" id="paidUsers">-</div><div class="stat-label">مشتركون مدفوعون</div></div>
    <div class="stat"><div class="stat-num" id="totalRevenue">-</div><div class="stat-label">إيراد شهري (ج.م)</div></div>
    <div class="stat"><div class="stat-num" id="totalReports">-</div><div class="stat-label">تقارير منشأة</div></div>
  </div>

  <div class="toolbar">
    <input id="searchInput" placeholder="بحث بالإيميل أو الاسم..." style="min-width:220px" oninput="renderTable()"/>
    <select id="filterPlan" onchange="renderTable()">
      <option value="">كل الباقات</option>
      <option value="free">Free</option>
      <option value="starter">Starter</option>
      <option value="pro">Pro</option>
      <option value="agency">Agency</option>
    </select>
    <button class="btn btn-success btn-sm" onclick="loadData()">🔄 تحديث</button>
    <button class="btn btn-primary btn-sm" onclick="exportCSV()">📥 تصدير CSV</button>
  </div>

  <table>
    <thead>
      <tr>
        <th>الإيميل</th>
        <th>الاسم</th>
        <th>الشركة</th>
        <th>الباقة</th>
        <th>التقارير</th>
        <th>الحالة</th>
        <th>تاريخ الانتهاء</th>
        <th>آخر دخول</th>
        <th>إجراءات</th>
      </tr>
    </thead>
    <tbody id="tableBody"></tbody>
  </table>
</div>

<!-- Edit Modal -->
<div class="modal" id="modal">
  <div class="mbox">
    <h3>✏️ تعديل بيانات المستخدم</h3>
    <input type="hidden" id="editUserId"/>
    <div class="fg">
      <label>الباقة</label>
      <select id="editPlan">
        <option value="free">🆓 Free</option>
        <option value="starter">🥉 Starter (299 ج.م)</option>
        <option value="pro">🥈 Pro (599 ج.م)</option>
        <option value="agency">🥇 Agency (1490 ج.م)</option>
      </select>
    </div>
    <div class="fg">
      <label>تاريخ انتهاء الاشتراك</label>
      <input type="date" id="editSubEnd"/>
    </div>
    <div class="fg">
      <label>ملاحظات</label>
      <textarea id="editNotes" placeholder="ملاحظات خاصة عن المستخدم..."></textarea>
    </div>
    <div class="mfoot">
      <button class="btn btn-primary" onclick="saveUser()">💾 حفظ</button>
      <button class="btn" onclick="closeModal()" style="background:rgba(255,255,255,.08);color:#9ca3af;border:none">إلغاء</button>
    </div>
  </div>
</div>

<div id="toast"></div>

<script>
var BACKEND = 'http://localhost:4000';
var allData = [];

function getToken(){
  var keys = Object.keys(localStorage);
  for(var i=0;i<keys.length;i++){
    var v = localStorage.getItem(keys[i]);
    if(v && v.startsWith('eyJ')) return v;
    try{ var p=JSON.parse(v); if(p&&p.access_token&&p.access_token.startsWith('eyJ')) return p.access_token; }catch(e){}
  }
  return null;
}

function apiFetch(url, opts){
  opts = opts||{};
  var token = getToken();
  var headers = {'Content-Type':'application/json'};
  if(token) headers['Authorization'] = 'Bearer '+token;
  opts.headers = headers;
  return fetch(BACKEND+url, opts);
}

function loadData(){
  apiFetch('/api/admin/crm/users').then(function(r){
    if(r.status===401){ document.getElementById('tableBody').innerHTML='<tr><td colspan="9" style="text-align:center;padding:30px;color:#f87171">⛔ غير مصرح — سجل دخولك من الداشبورد أولاً</td></tr>'; return null; }
    return r.json();
  }).then(function(data){
    if(!data) return;
    allData = data;
    updateStats();
    renderTable();
  }).catch(function(e){ showToast('خطأ في الاتصال'); });
}

function updateStats(){
  document.getElementById('totalUsers').textContent = allData.length;
  document.getElementById('freeUsers').textContent = allData.filter(function(u){ return u.plan_type==='free'; }).length;
  var paid = allData.filter(function(u){ return u.plan_type!=='free'; });
  document.getElementById('paidUsers').textContent = paid.length;
  var prices = {starter:299,pro:599,agency:1490};
  var rev = paid.reduce(function(s,u){ return s+(prices[u.plan_type]||0); },0);
  document.getElementById('totalRevenue').textContent = rev.toLocaleString();
  var reports = allData.reduce(function(s,u){ return s+(u.total_reports||0); },0);
  document.getElementById('totalReports').textContent = reports;
}

function renderTable(){
  var search = document.getElementById('searchInput').value.toLowerCase();
  var plan   = document.getElementById('filterPlan').value;
  var data   = allData.filter(function(u){
    if(plan && u.plan_type !== plan) return false;
    if(search && !(u.email||'').toLowerCase().includes(search) && !(u.full_name||'').toLowerCase().includes(search)) return false;
    return true;
  });

  var rows = data.map(function(u){
    var planClass = 'plan-'+u.plan_type;
    var planIcons = {free:'🆓',starter:'🥉',pro:'🥈',agency:'🥇'};
    var icon = planIcons[u.plan_type]||'';
    var used  = u.reports_used||0;
    var limit = u.reports_limit||1;
    var pct   = limit>0 ? Math.round(used/limit*100) : 0;
    var barColor = pct>=90?'#ef4444':pct>=70?'#f59e0b':'#6366f1';
    var subEnd  = u.sub_end ? new Date(u.sub_end).toLocaleDateString('ar-EG') : '—';
    var lastLog = u.last_login ? new Date(u.last_login).toLocaleDateString('ar-EG') : '—';
    var isExpired = u.sub_end && new Date(u.sub_end) < new Date();
    var statusTxt = u.plan_type==='free' ? '<span style="color:#6b7280">مجاني</span>' :
                    isExpired ? '<span class="status-expired">منتهي</span>' :
                    '<span class="status-active">نشط ✅</span>';

    return '<tr>' +
      '<td style="font-size:12px">'+( u.email||'—')+'</td>'+
      '<td>'+(u.full_name||'—')+'</td>'+
      '<td style="color:#6b7280">'+(u.company||'—')+'</td>'+
      '<td><span class="plan-badge '+planClass+'">'+icon+' '+u.plan_type+'</span></td>'+
      '<td>'+
        '<div style="font-size:11px;margin-bottom:3px">'+used+'/'+limit+'</div>'+
        '<div style="height:4px;background:rgba(255,255,255,.1);border-radius:99px;width:60px">'+
          '<div style="height:100%;width:'+Math.min(pct,100)+'%;background:'+barColor+';border-radius:99px"></div>'+
        '</div>'+
      '</td>'+
      '<td>'+statusTxt+'</td>'+
      '<td style="color:#6b7280;font-size:11px">'+subEnd+'</td>'+
      '<td style="color:#6b7280;font-size:11px">'+lastLog+'</td>'+
      '<td>'+
        '<button class="btn btn-warning btn-sm" onclick="openEdit(\''+u.user_id+'\')">✏️</button> '+
        '<a href="https://wa.me/'+( u.phone||'').replace(/[^0-9]/g,'')+'?text='+encodeURIComponent('مرحباً '+( u.full_name||'')+' — بخصوص اشتراكك في WissamXpoHub')+'" target="_blank" class="btn btn-success btn-sm" style="text-decoration:none">📱</a>'+
      '</td>'+
    '</tr>';
  });

  document.getElementById('tableBody').innerHTML = rows.join('') || '<tr><td colspan="9" style="text-align:center;padding:20px;color:#6b7280">لا يوجد مستخدمون</td></tr>';
}

function openEdit(userId){
  var u = allData.find(function(x){ return x.user_id===userId; });
  if(!u) return;
  document.getElementById('editUserId').value  = userId;
  document.getElementById('editPlan').value    = u.plan_type||'free';
  document.getElementById('editNotes').value   = u.notes||'';
  if(u.sub_end) document.getElementById('editSubEnd').value = u.sub_end.substring(0,10);
  document.getElementById('modal').classList.add('open');
}

function closeModal(){ document.getElementById('modal').classList.remove('open'); }

function saveUser(){
  var userId  = document.getElementById('editUserId').value;
  var plan    = document.getElementById('editPlan').value;
  var subEnd  = document.getElementById('editSubEnd').value;
  var notes   = document.getElementById('editNotes').value;
  var prices  = {free:0,starter:299,pro:599,agency:1490};
  var limits  = {free:1,starter:5,pro:25,agency:100};

  apiFetch('/api/admin/crm/update-user', {
    method:'POST',
    body: JSON.stringify({
      user_id: userId, plan_type: plan,
      price_egp: prices[plan]||0,
      reports_limit: limits[plan]||1,
      sub_end: subEnd||null, notes: notes
    })
  }).then(function(r){ return r.json(); }).then(function(d){
    closeModal();
    showToast('تم الحفظ ✅');
    loadData();
  }).catch(function(){ showToast('خطأ في الحفظ'); });
}

function exportCSV(){
  var rows = [['Email','Name','Company','Plan','Reports Used','Reports Limit','Sub End','Last Login']];
  allData.forEach(function(u){
    rows.push([u.email,u.full_name||'',u.company||'',u.plan_type,u.reports_used||0,u.reports_limit||1,u.sub_end||'',u.last_login||'']);
  });
  var csv = rows.map(function(r){ return r.join(','); }).join('\\n');
  var blob = new Blob(['\\uFEFF'+csv],{type:'text/csv;charset=utf-8'});
  var a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'wissamxpohub_users_'+new Date().toISOString().substring(0,10)+'.csv';
  a.click();
}

function showToast(msg){
  var t = document.getElementById('toast');
  t.textContent = msg;
  t.style.background = '#4ade80';
  t.style.color = '#000';
  t.style.display = 'block';
  setTimeout(function(){ t.style.display='none'; },3000);
}

loadData();
</script>
</body>
</html>"""

open('admin_crm.html', 'w', encoding='utf-8').write(html)
print('Done - admin_crm.html created')
