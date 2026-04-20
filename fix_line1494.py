lines = open('WissamXpoHub_V3_Frontend_FIXED.html', encoding='utf-8').readlines()

lines[1493] = '''        if (res.status === 402) {
          showUpgradeModal("وصلت للحد الاقصى — اختر باقة للاستمرار");
          return;
        }
        if(qs("aiBox"))qs("aiBox").textContent = Backend error ():\\n;
'''

open('WissamXpoHub_V3_Frontend_FIXED.html', 'w', encoding='utf-8').writelines(lines)
print('Done - line 1494 fixed')
