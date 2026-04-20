lines = open('WissamXpoHub_V3_Frontend_FIXED.html', encoding='utf-8').readlines()

# Fix line 2766
lines[2765] = "          \"<button onclick='document.getElementById(\\\"freeTrialBanner\\\").remove()' style='background:rgba(255,255,255,.1);color:#9ca3af;border:none;padding:8px 14px;border-radius:50px;cursor:pointer;font-size:12px'>×</button>\" +\n"

# Fix line 2776  
lines[2775] = "          \"<button onclick='document.getElementById(\\\"freeTrialBanner\\\").remove()' style='background:rgba(255,255,255,.1);color:#9ca3af;border:none;padding:7px 12px;border-radius:50px;cursor:pointer;font-size:12px'>×</button>\" +\n"

open('WissamXpoHub_V3_Frontend_FIXED.html', 'w', encoding='utf-8').writelines(lines)
print('Done - quotes fixed')
