# Language system for WissamXpoHub Dashboard
# Reports stay in Arabic - only UI changes

import re

content = open('WissamXpoHub_V3_Frontend_FIXED.html', encoding='utf-8').read()

# 1. Add language toggle button near the top badges
old_badges = '''        <div class="badge-row">
          <div class="badge" id="dashBadge">Dashboard Mode</div>
          <div class="badge">Supabase Auth</div>
          <div class="badge">AI + Sources</div>
        </div>'''

new_badges = '''        <div class="badge-row">
          <div class="badge" id="dashBadge">Dashboard Mode</div>
          <div class="badge">Supabase Auth</div>
          <div class="badge">AI + Sources</div>
          <div class="badge" id="langToggle" onclick="toggleLanguage()" style="cursor:pointer;background:rgba(99,102,241,.2);border:1px solid rgba(99,102,241,.4);color:#a5b4fc;">🌐 EN</div>
        </div>'''

content = content.replace(old_badges, new_badges, 1)

# 2. Add language JS system before </body>
lang_script = '''
  <!-- Language System -->
  <script>
  var LANG = localStorage.getItem("wx_lang") || "ar";

  var TRANSLATIONS = {
    ar: {
      login: "Login", logout: "Logout", signup: "تسجيل جديد",
      notLoggedIn: "غير مسجّل الدخول", loggedIn: "مسجّل الدخول",
      settings: "الإعدادات", saveSettings: "حفظ الإعدادات",
      testHealth: "اختبار الاتصال", productSetup: "إعداد المنتج",
      hsCode: "كود HS *", targetMarket: "السوق المستهدف *",
      productName: "اسم المنتج", question: "ما الذي تريد معرفته؟",
      runBtn: "تشغيل Export Intelligence ▶",
      quickShipping: "🚢 الشحن", quickCustoms: "⚖️ الجمارك",
      quickPricing: "💰 التسعير", quickCerts: "📋 الشهادات",
      quickBuyers: "🏭 المستوردين", quickMarket: "🚀 دخول السوق",
      quickFull: "📊 تقرير شامل",
      aiAdvisor: "AI Export Advisor", potentialBuyers: "Potential Buyers",
      scanner: "Export Opportunity Scanner",
      backBtn: "BACK ←", copy: "نسخ", pdf: "PDF",
      sources: "مصادر البيانات", upgrade: "ترقية الباقة",
      langBtn: "AR عربي",
      guideTitle: "🧭 دليل الاستخدام",
      guideSub: "منصة الذكاء التصديري المصري نحو أوروبا",
    },
    en: {
      login: "Login", logout: "Logout", signup: "Sign Up",
      notLoggedIn: "Not logged in", loggedIn: "Logged in",
      settings: "Settings", saveSettings: "Save Settings",
      testHealth: "Test Backend Health", productSetup: "Product Setup",
      hsCode: "HS Code *", targetMarket: "Target Market *",
      productName: "Product Name", question: "What do you want to know?",
      runBtn: "Run Export Intelligence ▶",
      quickShipping: "🚢 Shipping", quickCustoms: "⚖️ Customs",
      quickPricing: "💰 Pricing", quickCerts: "📋 Certificates",
      quickBuyers: "🏭 Importers", quickMarket: "🚀 Market Entry",
      quickFull: "📊 Full Report",
      aiAdvisor: "AI Export Advisor", potentialBuyers: "Potential Buyers",
      scanner: "Export Opportunity Scanner",
      backBtn: "BACK ←", copy: "Copy", pdf: "PDF",
      sources: "Data Sources", upgrade: "Upgrade Plan",
      langBtn: "🌐 EN",
      guideTitle: "🧭 User Guide",
      guideSub: "Egyptian Export Intelligence Platform for Europe",
    }
  };

  var UI_MAP = {
    "loginBtn":         {key: "login"},
    "signupBtn":        {key: "signup"},
    "langToggle":       {key: "langBtn"},
  };

  function applyLanguage(lang) {
    LANG = lang;
    localStorage.setItem("wx_lang", lang);
    var isAr = lang === "ar";
    var t = TRANSLATIONS[lang];

    // Direction
    document.documentElement.setAttribute("lang", lang);
    document.documentElement.setAttribute("dir", isAr ? "rtl" : "ltr");

    // Toggle button text
    var toggle = document.getElementById("langToggle");
    if (toggle) toggle.textContent = isAr ? "🌐 EN" : "🌐 عربي";

    // Apply all mapped elements
    for (var id in UI_MAP) {
      var el = document.getElementById(id);
      if (el) {
        var key = UI_MAP[id].key;
        if (t[key]) el.textContent = t[key];
      }
    }

    // Quick buttons
    var qBtns = document.querySelectorAll(".dash-q-btn");
    var qKeys = ["quickShipping","quickCustoms","quickPricing","quickCerts","quickBuyers","quickMarket","quickFull"];
    qBtns.forEach(function(btn, i) {
      if (qKeys[i] && t[qKeys[i]]) btn.textContent = t[qKeys[i]];
    });

    // Placeholders
    var hsInput = document.getElementById("hsCodeInput") || document.querySelector("input[placeholder*='080']");
    if (hsInput) hsInput.placeholder = isAr ? "مثال: 081110" : "e.g. 081110";

    var qInput = document.getElementById("userQuestion");
    if (qInput) qInput.placeholder = isAr ? "مثال: ما تكلفة الشحن للألمانيا؟ أو من هم أكبر المستوردين؟" : "e.g. What are the shipping costs to Germany?";

    // Run button
    var runBtn = document.getElementById("runBtn");
    if (runBtn && !runBtn.disabled) runBtn.textContent = t.runBtn;

    // Not logged in text
    var emailEl = document.getElementById("userEmail");
    if (emailEl && emailEl.textContent === TRANSLATIONS[isAr ? "en" : "ar"].notLoggedIn) {
      emailEl.textContent = t.notLoggedIn;
    }

    // Logout button
    var logoutBtns = document.querySelectorAll("button");
    logoutBtns.forEach(function(btn) {
      if (btn.textContent === "Logout" || btn.textContent === "Logout") {
        btn.textContent = t.logout;
      }
    });
  }

  function toggleLanguage() {
    applyLanguage(LANG === "ar" ? "en" : "ar");
  }

  // Apply on load
  document.addEventListener("DOMContentLoaded", function() {
    setTimeout(function() { applyLanguage(LANG); }, 500);
  });
  </script>
'''

real_body = content.rfind('\n</body>')
content = content[:real_body] + lang_script + content[real_body:]

open('WissamXpoHub_V3_Frontend_FIXED.html', 'w', encoding='utf-8').write(content)
print('Done - language system added')
