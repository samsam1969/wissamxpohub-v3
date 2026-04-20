content = open('WissamXpoHub_V3_Frontend_FIXED.html', encoding='utf-8').read()

old = '  function setDashQ(btn, text) {\n    // Check plan limit before activating\n    var used  = parseInt(localStorage.getItem("wx_plan_used") || "0");\n    var limit = parseInt(localStorage.getItem("wx_plan_limit") || "1");\n    if (used >= limit) {\n      showUpgradeModal("وصلت للحد الاقصى — اختر باقة للاستمرار");\n      return;\n    }'

new = '''  function showFreeTrialEndedBanner() {
    var used  = parseInt(localStorage.getItem("wx_plan_used") || "0");
    var limit = parseInt(localStorage.getItem("wx_plan_limit") || "1");
    var type  = localStorage.getItem("wx_plan_type") || "free";
    if (type !== "free") return;
    
    var existing = document.getElementById("freeTrialBanner");
    if (existing) return;
    
    var banner = document.createElement("div");
    banner.id = "freeTrialBanner";
    banner.style.cssText = "position:fixed;top:0;left:0;right:0;z-index:9998;background:linear-gradient(135deg,#1e1b4b,#312e81);border-bottom:2px solid rgba(99,102,241,.5);padding:14px 20px;font-family:Cairo,Arial,sans-serif;direction:rtl;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:10px;";
    
    if (used >= limit) {
      banner.innerHTML = 
        "<div style='display:flex;align-items:center;gap:10px'>" +
          "<span style='font-size:22px'>⏰</span>" +
          "<div>" +
            "<div style='color:white;font-weight:800;font-size:14px'>انتهت تجربتك المجانية!</div>" +
            "<div style='color:#9ca3af;font-size:12px'>استخدمت تقريرك المجاني (1/1) هذا الشهر — اشترك للحصول على المزيد</div>" +
          "</div>" +
        "</div>" +
        "<div style='display:flex;gap:8px;flex-wrap:wrap'>" +
          "<button onclick='showUpgradeModal()' style='background:linear-gradient(135deg,#6366f1,#8b5cf6);color:white;border:none;padding:8px 18px;border-radius:50px;font-family:Cairo,Arial,sans-serif;font-weight:700;font-size:13px;cursor:pointer'>🚀 اختر باقة</button>" +
          "<a href='https://wa.me/201116415272?text=" + encodeURIComponent("مرحباً، أريد الاشتراك في WissamXpoHub") + "' target='_blank' style='background:linear-gradient(135deg,#25d366,#128c7e);color:white;padding:8px 18px;border-radius:50px;text-decoration:none;font-weight:700;font-size:13px'>📱 واتساب</a>" +
          "<button onclick='document.getElementById(\"freeTrialBanner\").remove()' style='background:rgba(255,255,255,.1);color:#9ca3af;border:none;padding:8px 14px;border-radius:50px;cursor:pointer;font-size:12px'>×</button>" +
        "</div>";
    } else {
      banner.innerHTML =
        "<div style='display:flex;align-items:center;gap:10px'>" +
          "<span style='font-size:20px'>🎁</span>" +
          "<div style='color:#a5b4fc;font-size:13px'>أنت على الباقة المجانية — تقرير واحد مجاناً هذا الشهر (" + used + "/" + limit + " مستخدم)</div>" +
        "</div>" +
        "<div style='display:flex;gap:8px'>" +
          "<button onclick='showUpgradeModal()' style='background:linear-gradient(135deg,#6366f1,#8b5cf6);color:white;border:none;padding:7px 16px;border-radius:50px;font-family:Cairo,Arial,sans-serif;font-weight:700;font-size:12px;cursor:pointer'>ترقية الباقة</button>" +
          "<button onclick='document.getElementById(\"freeTrialBanner\").remove()' style='background:rgba(255,255,255,.1);color:#9ca3af;border:none;padding:7px 12px;border-radius:50px;cursor:pointer;font-size:12px'>×</button>" +
        "</div>";
    }
    
    document.body.prepend(banner);
  }

  // Show banner after login
  setTimeout(function() {
    var type = localStorage.getItem("wx_plan_type") || "free";
    if (type === "free") showFreeTrialEndedBanner();
  }, 2500);

  function setDashQ(btn, text) {
    // Check plan limit before activating
    var used  = parseInt(localStorage.getItem("wx_plan_used") || "0");
    var limit = parseInt(localStorage.getItem("wx_plan_limit") || "1");
    if (used >= limit) {
      showUpgradeModal("انتهت تجربتك المجانية — اختر باقة للاستمرار");
      return;
    }'''

content = content.replace(old, new, 1)
open('WissamXpoHub_V3_Frontend_FIXED.html', 'w', encoding='utf-8').write(content)
print('Done - free trial banner added')
