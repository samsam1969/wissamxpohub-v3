import shutil, re
from datetime import datetime

f = open("WissamXpoHub_V3_Frontend_FIXED.html", encoding="utf-8")
html = f.read()
f.close()

shutil.copy2("WissamXpoHub_V3_Frontend_FIXED.html", f"WissamXpoHub_V3_Frontend_FIXED_BACKUP_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html")

# Find section boundaries
s = html.find("    <!-- PRODUCT SETUP + AI ADVISOR -->")
e = html.find("  </div><!-- end .wrap -->")

if s == -1 or e == -1:
    print("FAIL - s:", s, "e:", e)
    exit()

print("Replacing section:", s, "->", e, "(", e-s, "chars)")

NEW_SECTION = """    <!-- AI ADVISOR — New UX -->

    <!-- Step 1: Question -->
    <section class="card" style="margin-top:18px;">
      <div style="display:flex;align-items:center;gap:12px;margin-bottom:16px;">
        <div style="width:26px;height:26px;border-radius:50%;background:linear-gradient(135deg,#3b82f6,#6366f1);display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:800;color:#fff;flex-shrink:0;">1</div>
        <div>
          <div style="font-size:17px;font-weight:800;">ما الذي تريد معرفته؟</div>
          <div style="font-size:12px;color:var(--muted);margin-top:2px;">اكتب سؤالك أو اختر من الخيارات السريعة</div>
        </div>
      </div>

      <div style="position:relative;">
        <span style="position:absolute;right:16px;top:50%;transform:translateY(-50%);font-size:20px;pointer-events:none;">🔍</span>
        <textarea id="userQuestion"
          style="width:100%;background:rgba(0,0,0,.3);border:1.5px solid var(--line);border-radius:12px;color:#fff;font-size:15px;font-family:'Cairo',Arial,sans-serif;font-weight:600;padding:16px 46px 16px 16px;outline:none;resize:none;min-height:60px;line-height:1.6;transition:border-color .15s;"
          placeholder="مثال: ما تكلفة شحن الفراولة لألمانيا؟ أو من هم أكبر المستوردين؟"
          oninput="onDashQuestion()" rows="2"></textarea>
      </div>

      <div style="display:flex;flex-wrap:wrap;gap:7px;margin-top:12px;">
        <button type="button" onclick="setDashQ(this,'شحن وتكاليف لوجستية')" class="dash-q-btn">🚢 الشحن</button>
        <button type="button" onclick="setDashQ(this,'الرسوم الجمركية ومتطلبات دخول السوق')" class="dash-q-btn">⚖️ الجمارك</button>
        <button type="button" onclick="setDashQ(this,'أهم المستوردين والموزعين في السوق')" class="dash-q-btn">🏢 المستوردين</button>
        <button type="button" onclick="setDashQ(this,'الشهادات والمتطلبات الصحية المطلوبة')" class="dash-q-btn">📋 الشهادات</button>
        <button type="button" onclick="setDashQ(this,'استراتيجية التسعير والربحية')" class="dash-q-btn">💰 التسعير</button>
        <button type="button" onclick="setDashQ(this,'استراتيجية دخول السوق وخطة التصدير')" class="dash-q-btn">🚀 دخول السوق</button>
        <button type="button" onclick="setDashQ(this,'')" class="dash-q-btn">📊 تقرير شامل</button>
      </div>
    </section>

    <!-- Step 2: Depth -->
    <section class="card" style="margin-top:14px;">
      <div style="display:flex;align-items:center;gap:12px;margin-bottom:14px;">
        <div style="width:26px;height:26px;border-radius:50%;background:linear-gradient(135deg,#3b82f6,#6366f1);display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:800;color:#fff;flex-shrink:0;">2</div>
        <div style="font-size:17px;font-weight:800;">مستوى التحليل</div>
      </div>
      <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;">
        <div id="dd-quick" onclick="setDashDepth('quick')" style="padding:14px;background:rgba(0,0,0,.25);border:1.5px solid var(--line);border-radius:12px;cursor:pointer;text-align:center;transition:all .15s;">
          <div style="font-size:20px;margin-bottom:5px;">⚡</div>
          <div style="font-size:12px;font-weight:800;">إجابة سريعة</div>
          <div style="font-size:10px;color:var(--muted);margin-top:3px;">~30 ثانية</div>
        </div>
        <div id="dd-pro" onclick="setDashDepth('pro')" style="padding:14px;background:rgba(59,130,246,.1);border:1.5px solid var(--btn);border-radius:12px;cursor:pointer;text-align:center;transition:all .15s;">
          <div style="font-size:20px;margin-bottom:5px;">📊</div>
          <div style="font-size:12px;font-weight:800;">تحليل احترافي</div>
          <div style="font-size:10px;color:var(--muted);margin-top:3px;">~90 ثانية</div>
        </div>
        <div id="dd-full" onclick="setDashDepth('full')" style="padding:14px;background:rgba(0,0,0,.25);border:1.5px solid var(--line);border-radius:12px;cursor:pointer;text-align:center;transition:all .15s;">
          <div style="font-size:20px;margin-bottom:5px;">📚</div>
          <div style="font-size:12px;font-weight:800;">تقرير شامل</div>
          <div style="font-size:10px;color:var(--muted);margin-top:3px;">~5 دقائق</div>
        </div>
      </div>
    </section>

    <!-- Step 3: Product + Market -->
    <section class="card" style="margin-top:14px;">
      <div style="display:flex;align-items:center;gap:12px;margin-bottom:14px;">
        <div style="width:26px;height:26px;border-radius:50%;background:linear-gradient(135deg,#3b82f6,#6366f1);display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:800;color:#fff;flex-shrink:0;">3</div>
        <div style="font-size:17px;font-weight:800;">المنتج والسوق</div>
      </div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;">
        <div>
          <label style="display:block;font-size:11px;font-weight:700;color:var(--muted);letter-spacing:.8px;margin-bottom:6px;">كود HS *</label>
          <input id="hs" placeholder="مثال: 081110" maxlength="10"
            style="width:100%;background:rgba(0,0,0,.3);border:1px solid var(--line);color:#fff;padding:11px 14px;border-radius:10px;font-size:14px;font-family:'Cairo',Arial,sans-serif;outline:none;transition:border-color .15s;"
            oninput="updateProductName()"/>
          <div class="product-box" id="productNameBox" style="margin-top:5px;font-size:12px;color:var(--warn);font-weight:700;min-height:18px;"></div>
        </div>
        <div>
          <label style="display:block;font-size:11px;font-weight:700;color:var(--muted);letter-spacing:.8px;margin-bottom:6px;">السوق المستهدف *</label>
          <select id="country" onchange="onCountryChange()"
            style="width:100%;background:rgba(0,0,0,.3);border:1px solid var(--line);color:#fff;padding:11px 14px;border-radius:10px;font-size:14px;font-family:'Cairo',Arial,sans-serif;outline:none;">
            <option value="__ALL__">🌍 جميع دول الاتحاد الأوروبي</option>
            <optgroup label="أهم الأسواق">
              <option value="Germany">Germany — ألمانيا</option>
              <option value="France">France — فرنسا</option>
              <option value="Netherlands">Netherlands — هولندا</option>
              <option value="Italy">Italy — إيطاليا</option>
              <option value="Spain">Spain — إسبانيا</option>
              <option value="Belgium">Belgium — بلجيكا</option>
              <option value="Poland">Poland — بولندا</option>
            </optgroup>
            <optgroup label="جميع دول الاتحاد الأوروبي">
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

      <!-- Smart Preview -->
      <div id="dashPreview" style="display:none;margin-top:14px;padding:14px 16px;background:rgba(59,130,246,.05);border:1px solid rgba(59,130,246,.2);border-radius:10px;">
        <div style="display:flex;align-items:flex-start;gap:10px;margin-bottom:8px;">
          <span style="font-size:14px;flex-shrink:0;">🎯</span>
          <div>
            <div style="font-size:10px;font-weight:700;color:var(--muted);letter-spacing:.8px;margin-bottom:5px;">سيتم تحليل طلبك باستخدام</div>
            <div id="dashModules" style="display:flex;flex-wrap:wrap;gap:4px;"></div>
          </div>
        </div>
        <div style="display:flex;align-items:flex-start;gap:10px;">
          <span style="font-size:14px;flex-shrink:0;">📚</span>
          <div>
            <div style="font-size:10px;font-weight:700;color:var(--muted);letter-spacing:.8px;margin-bottom:5px;">المصادر المستخدمة</div>
            <div id="dashSources" style="display:flex;flex-wrap:wrap;gap:4px;"></div>
          </div>
        </div>
      </div>

      <!-- Run Button -->
      <div style="display:flex;gap:10px;margin-top:14px;flex-wrap:wrap;">
        <button type="button" id="runBtn" onclick="runIntelligence()"
          style="flex:1;padding:15px;background:linear-gradient(135deg,#1d4ed8,#6366f1);border:none;border-radius:12px;color:#fff;font-size:15px;font-weight:800;font-family:'Cairo',Arial,sans-serif;cursor:pointer;box-shadow:0 6px 20px rgba(59,130,246,.35);transition:transform .13s,opacity .13s;display:flex;align-items:center;justify-content:center;gap:8px;">
          ▶ تشغيل Export Intelligence
        </button>
        <button type="button" onclick="resetAll()" class="ghost" style="padding:15px 18px;">إعادة</button>
      </div>
    </section>

    <!-- AI OUTPUT -->
    <section class="dashboard-stack">
      <div class="card">
        <div class="card-header">
          <h2>AI Export Advisor</h2>
          <h3 id="reportSubtitle" style="color:var(--muted);font-size:13px;"></h3>
        </div>
        <div style="display:flex;gap:8px;margin-bottom:12px;flex-wrap:wrap;">
          <button type="button" class="secondary" onclick="copyBoxText('aiBox')" style="padding:8px 14px;font-size:13px;border-radius:10px;">📋 نسخ</button>
          <button type="button" class="success" onclick="exportBoxToPdf('AI Export Advisor','aiBox')" style="padding:8px 14px;font-size:13px;border-radius:10px;">📄 PDF</button>
        </div>
        <div class="loader-wrap" id="aiLoader">
          <div class="spinner"></div>
          <div>
            <div class="loader-text">جارٍ تشغيل AI Export Advisor...</div>
            <div style="display:flex;flex-direction:column;gap:3px;margin-top:5px;">
              <div class="loader-step" id="als1" style="font-size:11px;color:var(--muted);">⏳ تحليل السؤال واختيار المصادر</div>
              <div class="loader-step" id="als2" style="font-size:11px;color:var(--muted);">⏳ جمع البيانات</div>
              <div class="loader-step" id="als3" style="font-size:11px;color:var(--muted);">⏳ كتابة التقرير</div>
            </div>
          </div>
        </div>
        <div id="aiDisclaimer" style="display:none;margin-bottom:10px;padding:10px 14px;background:rgba(245,158,11,.08);border:1px solid rgba(245,158,11,.3);border-radius:10px;font-size:12px;color:#fbbf24;">
          ⚠️ الإحصاءات مستقاة من Trade Map وEurostat وCBI. راجع الأرقام الحرجة قبل القرارات التجارية.
        </div>
        <div class="boxout" id="aiBox">شغّل Export Intelligence لإنشاء تقرير مخصص بناءً على سؤالك.</div>
      </div>
    </section>

"""

html = html[:s] + NEW_SECTION + html[e:]
open("WissamXpoHub_V3_Frontend_FIXED.html", "w", encoding="utf-8").write(html)
print("OK - new UX injected, size:", len(html))

# Now add the new JS functions
f2 = open("WissamXpoHub_V3_Frontend_FIXED.html", encoding="utf-8")
html2 = f2.read()
f2.close()

# Add CSS for dash-q-btn
old_css_end = "    @keyframes spin { to { transform: rotate(360deg); } }"
new_css = old_css_end + """
    .dash-q-btn{
      padding:7px 13px;background:rgba(59,130,246,.08);border:1px solid rgba(59,130,246,.2);
      border-radius:999px;color:#60a5fa;font-size:12px;font-weight:700;
      font-family:'Cairo',Arial,sans-serif;cursor:pointer;transition:all .15s;white-space:nowrap;
    }
    .dash-q-btn:hover,.dash-q-btn.dq-active{
      background:rgba(59,130,246,.2);border-color:rgba(59,130,246,.5);
    }"""

if old_css_end in html2:
    html2 = html2.replace(old_css_end, new_css, 1)
    print("OK - CSS added")

# Add new JS functions before /* ─── INIT ─── */
old_init_marker = "  /* ─── INIT ─── */"
new_js = """  /* ─── DASHBOARD AI ADVISOR NEW UX ─── */
  let dashDepth = "pro";
  let dashIntent = "general";

  const DASH_INTENT_MAP = {
    shipping:     {modules:["الشحن واللوجستيات","قواعد دخول السوق"], sources:["Access2Markets","EU TARIC","الجمارك المصرية"], srcValues:["access2markets","eu_taric","egyptian_customs"]},
    tariffs:      {modules:["الرسوم الجمركية","قواعد دخول السوق"], sources:["EU TARIC","Access2Markets","Eurostat"], srcValues:["eu_taric","access2markets","eurostat"]},
    buyers:       {modules:["قائمة المشترين","إحصاءات الاستيراد"], sources:["Trade Map","Europages","CBI"], srcValues:["trade_map","europages","cbi"]},
    compliance:   {modules:["السلامة الغذائية","التغليف والتوسيم"], sources:["EU Food Safety","Access2Markets"], srcValues:["eu_food_safety","access2markets"]},
    pricing:      {modules:["استراتيجية التسعير","تحليل المنافسين"], sources:["Trade Map","Eurostat"], srcValues:["trade_map","eurostat"]},
    market_entry: {modules:["دخول السوق","الجمارك","المشترين"], sources:["Trade Map","Access2Markets","CBI"], srcValues:["trade_map","access2markets","cbi"]},
    general:      {modules:["تقرير شامل","تحليل السوق","التوقعات"], sources:["Trade Map","Eurostat","Access2Markets","CBI"], srcValues:["trade_map","eurostat","access2markets","cbi"]}
  };

  function setDashQ(btn, text) {
    document.querySelectorAll(".dash-q-btn").forEach(b=>b.classList.remove("dq-active"));
    btn.classList.add("dq-active");
    const q = qs("userQuestion");
    if(q) q.value = text;
    onDashQuestion();
  }

  function setDashDepth(d) {
    dashDepth = d;
    ["quick","pro","full"].forEach(x => {
      const el = qs("dd-"+x);
      if(!el) return;
      el.style.borderColor = x===d ? "var(--btn)" : "var(--line)";
      el.style.background  = x===d ? "rgba(59,130,246,.1)" : "rgba(0,0,0,.25)";
    });
  }

  function detectDashIntent() {
    const q = (qs("userQuestion")?.value||"").toLowerCase();
    if(!q.trim()){ dashIntent="general"; return; }
    const checks = {
      shipping:["شحن","freight","shipping","حاوية","ميناء","لوجستي","نقل","تكلفة الشحن"],
      tariffs:["جمارك","tariff","رسوم","duty","ضريبة","دخول السوق"],
      buyers:["مشتري","buyer","importer","مستورد","موزع","شركات"],
      compliance:["شهادة","سلامة","صحي","مواصفات","تعبئة","تغليف"],
      pricing:["سعر","تسعير","pricing","ربح","هامش","تكلفة"],
      market_entry:["دخول","entry","استراتيجية","خطة","كيف أبدأ"]
    };
    for(const [intent, keywords] of Object.entries(checks)){
      if(keywords.some(k=>q.includes(k))){ dashIntent=intent; return; }
    }
    dashIntent = "general";
  }

  function onDashQuestion() {
    detectDashIntent();
    updateDashPreview();
  }

  function updateDashPreview() {
    const q = qs("userQuestion")?.value?.trim();
    const hs = qs("hs")?.value?.trim();
    const country = qs("country")?.value;
    const preview = qs("dashPreview");
    if(!preview) return;
    if(!q && !hs){ preview.style.display="none"; return; }
    const cfg = DASH_INTENT_MAP[dashIntent] || DASH_INTENT_MAP.general;
    const modEl = qs("dashModules");
    const srcEl = qs("dashSources");
    if(modEl) modEl.innerHTML = cfg.modules.map(m=>`<span style="font-size:11px;padding:2px 8px;border-radius:999px;background:rgba(59,130,246,.15);color:#93c5fd;border:1px solid rgba(59,130,246,.3);font-weight:700;">${m}</span>`).join("");
    if(srcEl)  srcEl.innerHTML = cfg.sources.map(s=>`<span style="font-size:11px;padding:2px 8px;border-radius:999px;background:rgba(16,185,129,.1);color:#6ee7b7;border:1px solid rgba(16,185,129,.25);font-weight:700;">${s}</span>`).join("");
    preview.style.display = "block";
  }

  /* ─── INIT ─── */"""

if old_init_marker in html2:
    html2 = html2.replace(old_init_marker, new_js, 1)
    print("OK - new JS functions added")
else:
    print("FAIL - init marker not found")

open("WissamXpoHub_V3_Frontend_FIXED.html", "w", encoding="utf-8").write(html2)
print("Final size:", len(html2))
