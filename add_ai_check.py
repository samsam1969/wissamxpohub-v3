content = open('WissamXpoHub_V3_Frontend_FIXED.html', encoding='utf-8').read()

# Find the function that calls the AI API and add permission check
old = '''    const res   = await fetchWithTimeout(${s.backendUrl}/api/ai/export-advisor, {'''

new = '''    // Check plan before calling API
    const planType = localStorage.getItem('wx_plan_type') || 'free';
    const planUsed = parseInt(localStorage.getItem('wx_plan_used') || '0');
    const planLimit = parseInt(localStorage.getItem('wx_plan_limit') || '1');
    if (planUsed >= planLimit) {
      if(box) box.innerHTML = '<div style="text-align:center;padding:40px;font-family:Cairo,Arial,sans-serif">' +
        '<div style="font-size:48px;margin-bottom:12px">⚠️</div>' +
        '<div style="color:#f87171;font-size:18px;font-weight:800;margin-bottom:8px">وصلت للحد الأقصى</div>' +
        '<div style="color:#9ca3af;margin-bottom:20px">استخدمت كل تقاريرك (' + planLimit + '/' + planLimit + ') هذا الشهر</div>' +
        '<button onclick="showUpgradeModal(\'وصلت للحد الأقصى — اختر باقة للاستمرار\')" style="background:linear-gradient(135deg,#6366f1,#8b5cf6);color:white;border:none;padding:12px 28px;border-radius:50px;font-family:Cairo,Arial,sans-serif;font-weight:700;font-size:15px;cursor:pointer">🚀 ترقية الباقة</button>' +
        '</div>';
      return;
    }

    const res   = await fetchWithTimeout(${s.backendUrl}/api/ai/export-advisor, {'''

content = content.replace(old, new, 1)
open('WissamXpoHub_V3_Frontend_FIXED.html', 'w', encoding='utf-8').write(content)
print('Done - AI check added')
