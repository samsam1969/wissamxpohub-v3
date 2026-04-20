import shutil
from datetime import datetime

f = open('WissamXpoHub_V3_Frontend_FIXED.html', encoding='utf-8')
html = f.read()
f.close()

changed = 0

# Patch 1
old1 = "  function renderBuyersTable(buyers) {\n    buyersData = buyers;\n    const tbody = qs(\"buyersTableBody\");\n    const count = qs(\"buyersCount\");"
new1 = "  function renderBuyersTable(buyers) {\n    buyersData = buyers;\n    try {\n      localStorage.setItem('wx_buyers_data', JSON.stringify(buyers));\n      localStorage.setItem('wx_buyers_product', qs('statProduct')?.textContent || '');\n      localStorage.setItem('wx_buyers_market',  qs('statMarket')?.textContent  || '');\n      localStorage.setItem('wx_buyers_hs',      qs('statHs')?.textContent      || '');\n    } catch(e) {}\n    const tbody = qs(\"buyersTableBody\");\n    const count = qs(\"buyersCount\");"

if old1 in html:
    html = html.replace(old1, new1, 1)
    changed += 1
    print('Patch 1 OK')
elif 'wx_buyers_data' in html:
    print('Patch 1 already applied')
    changed += 1
else:
    print('Patch 1 FAILED')

# Patch 2
btn = '\n        <div style="margin-bottom:12px;"><a href="PotentialBuyers.html" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;gap:7px;padding:9px 16px;border-radius:10px;font-size:13px;font-weight:800;border:1px solid #3b82f6;color:#93c5fd;text-decoration:none;background:rgba(29,78,216,.2);">🏢 فتح Potential Buyers في صفحة مستقلة ↗</a></div>'

if 'فتح Potential Buyers' in html:
    print('Patch 2 already applied')
    changed += 1
elif 'id="buyersCount"' in html:
    html = html.replace('id="buyersCount"', 'id="buyersCount_placeholder"', 1)
    html = html.replace('<div class="toolbar" style="margin-bottom:14px;">\n          <span id="buyersCount_placeholder"', btn + '\n        <div class="toolbar" style="margin-bottom:14px;">\n          <span id="buyersCount"', 1)
    changed += 1
    print('Patch 2 OK')
else:
    print('Patch 2 FAILED')

if changed > 0:
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    shutil.copy2('WissamXpoHub_V3_Frontend_FIXED.html', f'WissamXpoHub_V3_Frontend_FIXED_BACKUP_{ts}.html')
    open('WissamXpoHub_V3_Frontend_FIXED.html', 'w', encoding='utf-8').write(html)
    print(f'DONE {changed}/2 patches')
else:
    print('Nothing saved')
