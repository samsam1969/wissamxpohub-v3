content = open('admin_knowledge.html', encoding='utf-8').read()

old = 'loadData();'

new = '''// Debug token
getToken().then(t => {
  console.log('Token found:', t ? t.substring(0,30)+'...' : 'NONE');
  console.log('LocalStorage keys:', Object.keys(localStorage));
  if (!t) {
    document.getElementById('tableBody').innerHTML = 
      '<tr><td colspan="9" style="text-align:center;padding:40px;color:#f87171">⛔ لا يوجد token — سجّل دخولك من <a href="/" style="color:#a5b4fc">الداشبورد</a> أولاً</td></tr>';
  }
});
loadData();'''

content = content.replace(old, new, 1)
open('admin_knowledge.html', 'w', encoding='utf-8').write(content)
print('Done - debug added')
