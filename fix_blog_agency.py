content = open('Blog.html', encoding='utf-8').read()

old = '"<div style=\'background:rgba(139,92,246,.15);border:2px solid rgba(139,92,246,.5);border-radius:12px;padding:16px 20px\'><div style=color:#c4b5fd;font-weight:800>Pro ⭐</div><div style=color:#6b7280;font-size:13px>25 تقرير/شهر</div><div style=color:white;font-weight:800;font-size:18px>599 ج.م</div></div>" +'

new = '"<div style=\'background:rgba(139,92,246,.15);border:2px solid rgba(139,92,246,.5);border-radius:12px;padding:16px 20px\'><div style=color:#c4b5fd;font-weight:800>Pro ⭐</div><div style=color:#6b7280;font-size:13px>25 تقرير/شهر</div><div style=color:white;font-weight:800;font-size:18px>599 ج.م</div></div>" +' + \
'"<div style=\'background:rgba(245,158,11,.1);border:1px solid rgba(245,158,11,.3);border-radius:12px;padding:16px 20px\'><div style=color:#fcd34d;font-weight:800>Agency</div><div style=color:#6b7280;font-size:13px>100 تقرير/شهر</div><div style=color:white;font-weight:800;font-size:18px>1490 ج.م</div></div>" +'

content = content.replace(old, new, 1)
open('Blog.html', 'w', encoding='utf-8').write(content)
print('Done - Agency added to Blog lock')
