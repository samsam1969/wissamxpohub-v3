"""
create_ei_v2.py — Writes new ExportIntelligence.html with smart UX flow
Run: python create_ei_v2.py
"""

HTML = r"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<meta http-equiv="Cache-Control" content="no-cache,no-store,must-revalidate"/>
<title>Export Intelligence — WissamXpoHub</title>
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;800;900&display=swap" rel="stylesheet"/>
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<script src="auth_guard.js"></script>
<style>
:root{
  --bg:#050d1a;--bg2:#07111f;--card:rgba(10,22,45,.95);
  --line:#1a3560;--line2:#2d5aa8;--line3:#3b82f6;
  --text:#e8f0ff;--muted:#7a9cc4;--dim:#4a6a94;
  --ok:#22c55e;--bad:#ef4444;--warn:#f59e0b;
  --blue:#3b82f6;--indigo:#6366f1;--purple:#8b5cf6;
  --teal:#14b8a6;--green:#10b981;
  --r:16px;--r2:12px;--r3:8px;
  --sh:0 8px 32px rgba(0,0,0,.4);
}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
html{scroll-behavior:smooth;}
body{
  font-family:'Cairo',Arial,sans-serif;
  background:var(--bg);
  color:var(--text);
  min-height:100vh;
  overflow-x:hidden;
}

/* Background particles */
body::before{
  content:'';
  position:fixed;inset:0;
  background:
    radial-gradient(ellipse 80% 50% at 20% 20%, rgba(59,130,246,.06) 0%, transparent 60%),
    radial-gradient(ellipse 60% 40% at 80% 80%, rgba(99,102,241,.05) 0%, transparent 60%);
  pointer-events:none;z-index:0;
}

.wrap{max-width:1100px;margin:0 auto;padding:20px;position:relative;z-index:1;}

/* NAV */
.nav{
  display:flex;align-items:center;justify-content:space-between;
  padding:14px 20px;
  background:rgba(10,22,45,.95);
  border:1px solid var(--line);
  border-radius:var(--r);
  margin-bottom:28px;
  backdrop-filter:blur(12px);
}
.nav-brand{font-size:17px;font-weight:800;letter-spacing:-.3px;}
.nav-brand span{color:var(--blue);}
#authBadge{font-size:12px;font-weight:700;color:var(--muted);}

/* CARD */
.card{
  background:var(--card);
  border:1px solid var(--line);
  border-radius:var(--r);
  padding:24px;
  box-shadow:var(--sh);
  margin-bottom:20px;
  transition:border-color .2s;
}

/* STEP HEADER */
.step-header{
  display:flex;align-items:center;gap:12px;
  margin-bottom:18px;
}
.step-num{
  width:28px;height:28px;border-radius:50%;
  background:linear-gradient(135deg,var(--blue),var(--indigo));
  display:flex;align-items:center;justify-content:center;
  font-size:12px;font-weight:800;color:#fff;flex-shrink:0;
}
.step-title{font-size:18px;font-weight:800;}
.step-sub{font-size:13px;color:var(--muted);margin-top:2px;}

/* MAIN QUESTION INPUT */
.question-wrap{position:relative;}
.question-input{
  width:100%;
  background:rgba(0,0,0,.3);
  border:1.5px solid var(--line);
  border-radius:var(--r2);
  color:var(--text);
  font-size:16px;
  font-family:'Cairo',Arial,sans-serif;
  font-weight:600;
  padding:18px 20px 18px 56px;
  outline:none;
  transition:border-color .2s,box-shadow .2s;
  resize:none;
  min-height:64px;
  line-height:1.6;
}
.question-input:focus{
  border-color:var(--blue);
  box-shadow:0 0 0 3px rgba(59,130,246,.15);
}
.question-input::placeholder{color:var(--dim);}
.q-icon{
  position:absolute;right:18px;top:50%;transform:translateY(-50%);
  font-size:22px;pointer-events:none;
}

/* QUICK BUTTONS */
.quick-grid{
  display:flex;flex-wrap:wrap;gap:8px;
  margin-top:14px;
}
.quick-btn{
  padding:7px 14px;
  background:rgba(59,130,246,.08);
  border:1px solid rgba(59,130,246,.2);
  border-radius:999px;
  color:var(--blue);
  font-size:13px;font-weight:700;
  font-family:'Cairo',Arial,sans-serif;
  cursor:pointer;
  transition:all .15s;
  white-space:nowrap;
}
.quick-btn:hover,.quick-btn.active{
  background:rgba(59,130,246,.2);
  border-color:rgba(59,130,246,.5);
  transform:translateY(-1px);
}
.quick-btn.active{background:rgba(59,130,246,.25);border-color:var(--blue);}

/* DEPTH SELECTOR */
.depth-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:4px;}
.depth-card{
  padding:16px;
  background:rgba(0,0,0,.25);
  border:1.5px solid var(--line);
  border-radius:var(--r2);
  cursor:pointer;
  transition:all .15s;
  text-align:center;
}
.depth-card:hover{border-color:var(--line2);}
.depth-card.active{
  border-color:var(--blue);
  background:rgba(59,130,246,.1);
}
.depth-icon{font-size:22px;margin-bottom:6px;}
.depth-name{font-size:13px;font-weight:800;margin-bottom:3px;}
.depth-desc{font-size:11px;color:var(--muted);}
.depth-time{font-size:10px;color:var(--dim);margin-top:4px;}

/* PRODUCT ROW */
.product-row{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:4px;}
label.fl{display:block;font-size:12px;font-weight:700;color:var(--muted);letter-spacing:.8px;margin-bottom:6px;}
input.fi,select.fi{
  width:100%;background:rgba(0,0,0,.3);border:1px solid var(--line);
  color:var(--text);padding:11px 14px;border-radius:var(--r3);
  font-size:14px;font-family:'Cairo',Arial,sans-serif;outline:none;
  transition:border-color .15s;
}
input.fi:focus,select.fi:focus{border-color:var(--blue);}
input.fi::placeholder{color:var(--dim);}
select.fi option{background:#0a1628;}
.product-name-hint{font-size:12px;color:var(--warn);font-weight:700;margin-top:5px;min-height:18px;}

/* RUN BUTTON */
.run-btn{
  width:100%;padding:16px;
  background:linear-gradient(135deg,var(--blue),var(--indigo));
  border:none;border-radius:var(--r2);
  color:#fff;font-size:16px;font-weight:800;
  font-family:'Cairo',Arial,sans-serif;cursor:pointer;
  transition:transform .13s,opacity .13s,box-shadow .13s;
  box-shadow:0 6px 20px rgba(59,130,246,.35);
  display:flex;align-items:center;justify-content:center;gap:10px;
  margin-top:4px;
}
.run-btn:hover{transform:translateY(-2px);box-shadow:0 10px 28px rgba(59,130,246,.45);}
.run-btn:active{transform:scale(.98);}
.run-btn:disabled{opacity:.5;cursor:not-allowed;transform:none;box-shadow:none;}

/* PREVIEW CARD */
.preview-card{
  background:rgba(59,130,246,.05);
  border:1px solid rgba(59,130,246,.2);
  border-radius:var(--r2);
  padding:16px 18px;
  margin-top:16px;
  display:none;
}
.preview-row{display:flex;align-items:flex-start;gap:10px;margin-bottom:10px;}
.preview-row:last-child{margin-bottom:0;}
.preview-icon{font-size:16px;flex-shrink:0;margin-top:1px;}
.preview-label{font-size:11px;color:var(--muted);font-weight:700;letter-spacing:.8px;margin-bottom:4px;}
.preview-tags{display:flex;flex-wrap:wrap;gap:5px;}
.preview-tag{
  font-size:11px;padding:2px 9px;border-radius:999px;font-weight:700;
  background:rgba(59,130,246,.15);color:#93c5fd;border:1px solid rgba(59,130,246,.3);
}
.preview-tag.green{background:rgba(16,185,129,.12);color:#6ee7b7;border-color:rgba(16,185,129,.3);}

/* ADVANCED TOGGLE */
.adv-toggle{
  display:flex;align-items:center;gap:6px;
  font-size:12px;color:var(--muted);font-weight:700;cursor:pointer;
  margin-top:12px;padding:0;background:none;border:none;
  font-family:'Cairo',Arial,sans-serif;
  transition:color .15s;
}
.adv-toggle:hover{color:var(--text);}
.adv-wrap{display:none;margin-top:14px;}
.adv-wrap.show{display:block;}
.adv-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px;}
.adv-section-title{font-size:11px;font-weight:700;color:var(--muted);letter-spacing:1.2px;text-transform:uppercase;margin-bottom:8px;}
.check-grid{display:flex;flex-direction:column;gap:6px;}
.check-item{
  display:flex;align-items:center;gap:8px;
  padding:7px 10px;
  background:rgba(0,0,0,.2);
  border:1px solid var(--line);
  border-radius:var(--r3);
  font-size:12px;font-weight:700;cursor:pointer;
  transition:border-color .15s;
}
.check-item:hover{border-color:var(--line2);}
.check-item input{width:auto;margin:0;transform:scale(1.1);accent-color:var(--blue);}

/* LOADER */
.loader{
  display:none;align-items:center;gap:12px;
  padding:14px 18px;
  background:rgba(0,0,0,.2);border:1px solid var(--line);
  border-radius:var(--r2);margin-bottom:14px;
}
.loader.show{display:flex;}
.spin{
  width:20px;height:20px;border-radius:50%;flex-shrink:0;
  border:2.5px solid rgba(255,255,255,.1);
  border-top-color:var(--blue);
  animation:spin .8s linear infinite;
}
@keyframes spin{to{transform:rotate(360deg);}}
.loader-text{font-size:13px;font-weight:700;color:var(--muted);}
.loader-steps{display:flex;flex-direction:column;gap:3px;margin-top:4px;}
.loader-step{font-size:11px;color:var(--dim);transition:color .3s;}
.loader-step.active{color:var(--blue);}
.loader-step.done{color:var(--ok);}

/* REPORT */
.report-box{
  min-height:200px;
  background:rgba(0,0,0,.2);
  border:1px solid var(--line);
  border-radius:var(--r2);
  padding:20px;
  line-height:1.85;font-size:15px;
  overflow:auto;
  font-family:'Cairo',Arial,sans-serif;
}
.report-box h1{color:#60a5fa;font-size:21px;font-weight:800;margin:20px 0 10px;border-bottom:1px solid var(--line);padding-bottom:8px;}
.report-box h2{color:#60a5fa;font-size:17px;font-weight:800;margin:16px 0 8px;}
.report-box h3{color:var(--warn);font-size:15px;font-weight:700;margin:14px 0 6px;}
.report-box h4{color:var(--text);font-size:14px;font-weight:700;margin:10px 0 5px;}
.report-box p{margin:8px 0;line-height:1.9;}
.report-box ul,report-box ol{padding-right:22px;margin:8px 0;}
.report-box li{margin:5px 0;line-height:1.8;}
.report-box strong{color:#fff;font-weight:800;}
.report-box table{width:100%;border-collapse:collapse;margin:14px 0;font-size:13px;}
.report-box th{background:rgba(29,78,216,.25);color:#93c5fd;padding:10px 12px;text-align:right;font-weight:700;border:1px solid var(--line);}
.report-box td{padding:9px 12px;border:1px solid var(--line);}
.report-box tr:nth-child(even) td{background:rgba(255,255,255,.02);}
.report-box hr{border:none;border-top:1px solid var(--line);margin:16px 0;}
.report-box code{background:rgba(255,255,255,.07);padding:2px 7px;border-radius:5px;font-size:12px;}
.report-empty{color:var(--dim);text-align:center;padding:40px 20px;font-size:14px;}

/* TOOLBAR */
.toolbar{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-bottom:12px;flex-wrap:wrap;}
.toolbar-btns{display:flex;gap:8px;}
.tb-btn{
  padding:8px 16px;font-size:13px;font-weight:700;border-radius:var(--r3);border:none;
  font-family:'Cairo',Arial,sans-serif;cursor:pointer;color:#fff;
  transition:transform .12s,opacity .12s;
}
.tb-btn:hover{transform:translateY(-1px);opacity:.9;}
.tb-copy{background:rgba(255,255,255,.1);border:1px solid var(--line);}
.tb-pdf{background:#15803d;}
.report-meta{font-size:12px;color:var(--muted);}

/* DISCLAIMER */
.disclaimer{
  padding:10px 14px;
  background:rgba(245,158,11,.06);border:1px solid rgba(245,158,11,.2);
  border-radius:var(--r3);font-size:12px;color:#fbbf24;
  margin-bottom:12px;display:none;
}

/* ERROR */
#formError{font-size:13px;color:var(--bad);font-weight:700;min-height:18px;margin-top:10px;}

/* GHOST BTN */
.ghost-btn{
  background:rgba(255,255,255,.06);border:1px solid var(--line);
  border-radius:var(--r3);padding:9px 16px;font-size:13px;font-weight:800;
  font-family:'Cairo',Arial,sans-serif;cursor:pointer;color:var(--text);
  transition:all .13s;
}
.ghost-btn:hover{background:rgba(255,255,255,.1);}

/* RESPONSIVE */
@media(max-width:700px){
  .depth-grid{grid-template-columns:1fr;}
  .product-row{grid-template-columns:1fr;}
  .adv-grid{grid-template-columns:1fr;}
  .quick-grid{gap:6px;}
  .quick-btn{font-size:12px;padding:6px 12px;}
}
</style>
</head>
<body>
<div class="wrap">

<!-- NAV -->
<nav class="nav">
  <div style="display:flex;align-items:center;gap:12px;">
    <button class="ghost-btn" onclick="goBack()" style="padding:8px 14px;font-size:13px;">&#8592; العودة</button>
    <div class="nav-brand">WissamXpoHub <span>/ Export Intelligence</span></div>
  </div>
  <div id="authBadge">جارٍ التحقق...</div>
</nav>

<!-- STEP 1: QUESTION -->
<div class="card">
  <div class="step-header">
    <div class="step-num">1</div>
    <div>
      <div class="step-title">ما الذي تريد معرفته؟</div>
      <div class="step-sub">اكتب سؤالك أو اختر من الخيارات السريعة</div>
    </div>
  </div>

  <div class="question-wrap">
    <span class="q-icon">🔍</span>
    <textarea class="question-input" id="questionInput"
      placeholder="مثال: ما هي تكلفة شحن الفراولة المجمدة من مصر إلى ألمانيا؟ أو ما هي الرسوم الجمركية؟ أو من هم أكبر المستوردين؟"
      oninput="onQuestionInput()" rows="2"></textarea>
  </div>

  <div class="quick-grid">
    <button class="quick-btn" onclick="setQuick(this,'شحن وتكاليف لوجستية')">🚢 الشحن والخدمات اللوجستية</button>
    <button class="quick-btn" onclick="setQuick(this,'الرسوم الجمركية ومتطلبات دخول السوق')">⚖️ الرسوم الجمركية</button>
    <button class="quick-btn" onclick="setQuick(this,'أهم المستوردين والموزعين في السوق')">🏢 أهم المستوردين</button>
    <button class="quick-btn" onclick="setQuick(this,'الشهادات والمتطلبات الصحية المطلوبة')">📋 الشهادات والمتطلبات</button>
    <button class="quick-btn" onclick="setQuick(this,'استراتيجية التسعير والربحية')">💰 التسعير والربحية</button>
    <button class="quick-btn" onclick="setQuick(this,'استراتيجية دخول السوق وخطة التصدير')">🚀 دخول السوق</button>
    <button class="quick-btn" onclick="setQuick(this,'')">📊 تقرير شامل</button>
  </div>
</div>

<!-- STEP 2: DEPTH -->
<div class="card">
  <div class="step-header">
    <div class="step-num">2</div>
    <div>
      <div class="step-title">مستوى التحليل</div>
      <div class="step-sub">اختر عمق التقرير المناسب لاحتياجك</div>
    </div>
  </div>

  <div class="depth-grid">
    <div class="depth-card" id="d-quick" onclick="setDepth('quick')">
      <div class="depth-icon">⚡</div>
      <div class="depth-name">إجابة سريعة</div>
      <div class="depth-desc">إجابة مباشرة ومختصرة</div>
      <div class="depth-time">~30 ثانية</div>
    </div>
    <div class="depth-card active" id="d-pro" onclick="setDepth('pro')">
      <div class="depth-icon">📊</div>
      <div class="depth-name">تحليل احترافي</div>
      <div class="depth-desc">تقرير مفصل مع بيانات</div>
      <div class="depth-time">~60-90 ثانية</div>
    </div>
    <div class="depth-card" id="d-full" onclick="setDepth('full')">
      <div class="depth-icon">📚</div>
      <div class="depth-name">تقرير شامل</div>
      <div class="depth-desc">تحليل معمق متكامل</div>
      <div class="depth-time">~3-5 دقائق</div>
    </div>
  </div>
</div>

<!-- STEP 3: PRODUCT -->
<div class="card">
  <div class="step-header">
    <div class="step-num">3</div>
    <div>
      <div class="step-title">المنتج والسوق</div>
      <div class="step-sub">حدد المنتج والسوق المستهدف</div>
    </div>
  </div>

  <div class="product-row">
    <div>
      <label class="fl">كود HS <span style="color:var(--bad)">*</span></label>
      <input class="fi" id="hsInput" placeholder="مثال: 081110" maxlength="10" oninput="onHsInput()"/>
      <div class="product-name-hint" id="productHint"></div>
    </div>
    <div>
      <label class="fl">السوق المستهدف <span style="color:var(--bad)">*</span></label>
      <select class="fi" id="countryInput" onchange="updatePreview()">
        <option value="">— اختر الدولة (مطلوب) —</option>
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
  <div class="preview-card" id="previewCard">
    <div class="preview-row">
      <div class="preview-icon">🎯</div>
      <div>
        <div class="preview-label">سيتم تحليل طلبك باستخدام</div>
        <div class="preview-tags" id="previewModules"></div>
      </div>
    </div>
    <div class="preview-row">
      <div class="preview-icon">📚</div>
      <div>
        <div class="preview-label">المصادر المستخدمة</div>
        <div class="preview-tags" id="previewSources"></div>
      </div>
    </div>
  </div>

  <!-- Advanced Toggle -->
  <button class="adv-toggle" onclick="toggleAdv()">
    <span id="advArrow">▶</span> الإعدادات المتقدمة (اختياري)
  </button>
  <div class="adv-wrap" id="advWrap">
    <div class="adv-grid">
      <div>
        <div class="adv-section-title">تركيز التقرير</div>
        <div class="check-grid">
          <label class="check-item"><input type="checkbox" class="mod" value="logistics"> 🚢 الشحن واللوجستيات</label>
          <label class="check-item"><input type="checkbox" class="mod" value="tariffs"> ⚖️ الرسوم الجمركية</label>
          <label class="check-item"><input type="checkbox" class="mod" value="buyers"> 🏢 قائمة المشترين</label>
          <label class="check-item"><input type="checkbox" class="mod" value="compliance"> 📋 السلامة الغذائية</label>
          <label class="check-item"><input type="checkbox" class="mod" value="pricing"> 💰 استراتيجية التسعير</label>
          <label class="check-item"><input type="checkbox" class="mod" value="competitors"> 📊 تحليل المنافسين</label>
          <label class="check-item"><input type="checkbox" class="mod" value="packaging"> 📦 التغليف والتوسيم</label>
        </div>
      </div>
      <div>
        <div class="adv-section-title">مصادر البيانات</div>
        <div class="check-grid">
          <label class="check-item"><input type="checkbox" class="src" value="trade_map" checked> ITC Trade Map</label>
          <label class="check-item"><input type="checkbox" class="src" value="un_comtrade"> UN Comtrade</label>
          <label class="check-item"><input type="checkbox" class="src" value="access2markets" checked> Access2Markets</label>
          <label class="check-item"><input type="checkbox" class="src" value="eu_taric" checked> EU TARIC</label>
          <label class="check-item"><input type="checkbox" class="src" value="eurostat" checked> Eurostat</label>
          <label class="check-item"><input type="checkbox" class="src" value="cbi"> CBI Netherlands</label>
          <label class="check-item"><input type="checkbox" class="src" value="eu_food_safety"> EU Food Safety</label>
          <label class="check-item"><input type="checkbox" class="src" value="europages"> Europages</label>
          <label class="check-item"><input type="checkbox" class="src" value="globy"> Globy B2B</label>
          <label class="check-item"><input type="checkbox" class="src" value="egyptian_customs"> الجمارك المصرية</label>
        </div>
      </div>
    </div>
  </div>
</div>

<!-- RUN -->
<button class="run-btn" id="runBtn" onclick="runAnalysis()">
  <span>▶</span> تشغيل Export Intelligence
</button>
<div id="formError"></div>

<!-- OUTPUT -->
<div class="card" id="outputCard" style="display:none;">
  <div class="toolbar">
    <div class="report-meta" id="reportMeta"></div>
    <div class="toolbar-btns">
      <button class="tb-btn tb-copy" onclick="copyReport()">📋 نسخ</button>
      <button class="tb-btn tb-pdf" onclick="exportPDF()">📄 PDF</button>
    </div>
  </div>

  <div class="loader" id="aiLoader">
    <div class="spin"></div>
    <div>
      <div class="loader-text">جارٍ تشغيل التحليل...</div>
      <div class="loader-steps">
        <div class="loader-step" id="ls1">⏳ تحليل السؤال واختيار المصادر</div>
        <div class="loader-step" id="ls2">⏳ جمع البيانات من المصادر الموثوقة</div>
        <div class="loader-step" id="ls3">⏳ كتابة التقرير</div>
        <div class="loader-step" id="ls4">⏳ مراجعة وإنهاء التقرير</div>
      </div>
    </div>
  </div>

  <div class="disclaimer" id="disclaimer">
    ⚠️ الإحصاءات مستقاة من Trade Map وEurostat وCBI. راجع الأرقام الحرجة قبل اتخاذ القرارات التجارية.
  </div>

  <div class="report-box" id="reportBox">
    <div class="report-empty">شغّل Export Intelligence لإنشاء تقرير مخصص.</div>
  </div>
</div>

</div><!-- .wrap -->

<script>
if(typeof marked!=="undefined") marked.setOptions({breaks:true,gfm:true});

const SB_URL = "https://hfvhivxpaqnqaooyqmaw.supabase.co";
const SB_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhmdmhpdnhwYXFucWFvb3lxbWF3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzI0NDg1OTMsImV4cCI6MjA4ODAyNDU5M30.HaTO3Ngeq6oaw9eLddgJpxg-_6fwD6G9aj8EJZSRUcY";

const HS_MAP = {
  "081110":"Frozen strawberries","081120":"Frozen raspberries","081190":"Frozen fruits",
  "080510":"Fresh oranges","080520":"Mandarins","080550":"Lemons and limes",
  "080610":"Fresh grapes","070200":"Tomatoes","070320":"Garlic","070310":"Onions",
  "100630":"Rice milled","100610":"Rice in husks","090111":"Coffee","030617":"Frozen shrimp",
  "020130":"Fresh beef","040221":"Milk powder","170111":"Raw cane sugar",
  "151190":"Palm oil","160414":"Tuna","190190":"Food preparations"
};

// Intent detection
const INTENT_MAP = {
  shipping: {
    keywords: ["شحن","freight","shipping","حاوية","ميناء","port","container","logistics","لوجستي","نقل","تكلفة النقل","مدة الشحن"],
    modules: ["الشحن واللوجستيات","قواعد دخول السوق"],
    sources: ["Access2Markets","EU TARIC","Eurostat","الجمارك المصرية","UN Comtrade"],
    srcValues: ["access2markets","eu_taric","eurostat","egyptian_customs","un_comtrade"]
  },
  tariffs: {
    keywords: ["جمارك","tariff","رسوم","duty","ضريبة","tax","متطلبات","دخول السوق","اتفاقيات"],
    modules: ["الرسوم الجمركية","قواعد دخول السوق","اللوائح التجارية"],
    sources: ["EU TARIC","Access2Markets","EU Trade Regs","Eurostat"],
    srcValues: ["eu_taric","access2markets","eu_trade_regulations","eurostat"]
  },
  buyers: {
    keywords: ["مشتري","buyer","importer","مستورد","موزع","distributor","عميل","client","شركات"],
    modules: ["قائمة المشترين","إحصاءات الاستيراد","تحليل المنافسين"],
    sources: ["Trade Map","Europages","Globy B2B","CBI Netherlands"],
    srcValues: ["trade_map","europages","globy","cbi"]
  },
  compliance: {
    keywords: ["شهادة","certificate","سلامة","safety","صحي","health","مواصفات","standards","تعبئة","تغليف"],
    modules: ["السلامة الغذائية","التغليف والتوسيم","قواعد دخول السوق"],
    sources: ["EU Food Safety","Access2Markets","EU Trade Regs"],
    srcValues: ["eu_food_safety","access2markets","eu_trade_regulations"]
  },
  pricing: {
    keywords: ["سعر","تسعير","pricing","price","ربح","profit","هامش","margin","تكلفة","cost"],
    modules: ["استراتيجية التسعير","تحليل المنافسين","إحصاءات الاستيراد","الشحن"],
    sources: ["Trade Map","Eurostat","Logistics Data"],
    srcValues: ["trade_map","eurostat","access2markets"]
  },
  market_entry: {
    keywords: ["دخول","entry","استراتيجية","strategy","خطة","plan","كيف أبدأ","بداية"],
    modules: ["دخول السوق","الرسوم الجمركية","المشترين","الشحن"],
    sources: ["Trade Map","Access2Markets","EU TARIC","CBI","Eurostat"],
    srcValues: ["trade_map","access2markets","eu_taric","cbi","eurostat"]
  }
};

let sb = null;
let currentDepth = "pro";
let currentIntent = "general";

const qs = id => document.getElementById(id);

function initSB(){
  if(!sb && window.supabase) sb = window.supabase.createClient(SB_URL, SB_KEY);
  return sb;
}

async function getToken(){
  if(!sb) initSB();
  try {
    const {data} = await sb.auth.getSession();
    if(data?.session?.access_token){
      localStorage.setItem("wx_access_token", data.session.access_token);
      return data.session.access_token;
    }
  } catch(_){}
  return localStorage.getItem("wx_access_token") || "";
}

async function fetchWT(url, opts, timeoutMs=600000){
  const c = new AbortController();
  const t = setTimeout(()=>c.abort(), timeoutMs);
  try{ return await fetch(url, {...opts, signal:c.signal}); }
  catch(e){ if(e.name==="AbortError") throw new Error("انتهت مهلة الاتصال"); throw e; }
  finally{ clearTimeout(t); }
}

// ── Quick buttons
function setQuick(btn, text){
  document.querySelectorAll(".quick-btn").forEach(b=>b.classList.remove("active"));
  btn.classList.add("active");
  qs("questionInput").value = text;
  onQuestionInput();
}

// ── Depth
function setDepth(d){
  currentDepth = d;
  ["quick","pro","full"].forEach(x => qs("d-"+x).classList.remove("active"));
  qs("d-"+d).classList.add("active");
}

// ── HS Code
function onHsInput(){
  const hs = qs("hsInput").value.trim();
  const name = HS_MAP[hs] || (hs.length>=4 ? "Product ("+hs+")" : "");
  qs("productHint").textContent = name ? "📦 " + name : "";
  try{ localStorage.setItem("wx_ei_hs", hs); }catch(_){}
  updatePreview();
}

// ── Question input
function onQuestionInput(){
  detectIntent();
  updatePreview();
}

// ── Intent detection
function detectIntent(){
  const q = qs("questionInput").value.toLowerCase();
  if(!q.trim()){ currentIntent = "general"; return; }
  for(const [intent, cfg] of Object.entries(INTENT_MAP)){
    if(cfg.keywords.some(k => q.includes(k))){
      currentIntent = intent;
      return;
    }
  }
  currentIntent = "general";
}

// ── Preview
function updatePreview(){
  const hs = qs("hsInput").value.trim();
  const country = qs("countryInput").value;
  const question = qs("questionInput").value.trim();

  if(!hs && !country && !question){
    qs("previewCard").style.display="none";
    return;
  }

  const cfg = INTENT_MAP[currentIntent];
  const modules = cfg ? cfg.modules : ["تقرير شامل","تحليل السوق","المنافسين","التوقعات"];
  const sources = cfg ? cfg.sources : ["Trade Map","Eurostat","Access2Markets","CBI"];

  qs("previewModules").innerHTML = modules.map(m=>`<span class="preview-tag">${m}</span>`).join("");
  qs("previewSources").innerHTML = sources.map(s=>`<span class="preview-tag green">${s}</span>`).join("");
  qs("previewCard").style.display = "block";
}

// ── Advanced settings toggle
function toggleAdv(){
  const wrap = qs("advWrap");
  const arrow = qs("advArrow");
  if(wrap.classList.contains("show")){
    wrap.classList.remove("show");
    arrow.textContent = "▶";
  } else {
    wrap.classList.add("show");
    arrow.textContent = "▼";
  }
}

// ── Get selected sources
function getSelectedSources(){
  const adv = Array.from(document.querySelectorAll(".src:checked")).map(e=>e.value);
  if(adv.length > 0) return adv;
  const cfg = INTENT_MAP[currentIntent];
  return cfg ? cfg.srcValues : ["trade_map","eurostat","access2markets","cbi"];
}

// ── Loader steps animation
function setLoaderStep(step){
  for(let i=1;i<=4;i++){
    const el = qs("ls"+i);
    if(!el) continue;
    if(i < step) el.className = "loader-step done";
    else if(i === step) el.className = "loader-step active";
    else el.className = "loader-step";
  }
}

// ── Run Analysis
async function runAnalysis(){
  qs("formError").textContent = "";
  const hs = qs("hsInput").value.trim();
  const country = qs("countryInput").value;
  const question = qs("questionInput").value.trim();

  if(!hs || hs.length < 4){ qs("formError").textContent = "أدخل كود HS صحيح (4-6 أرقام)"; return; }
  if(!country){ qs("formError").textContent = "اختر السوق المستهدف"; return; }

  const backendUrl = (localStorage.getItem("wx_backend_url")||"http://localhost:4000").replace(/\/$/,"");
  const token = await getToken();
  if(!token){ qs("formError").textContent = "سجّل الدخول من الصفحة الرئيسية أولاً"; return; }

  const productName = HS_MAP[hs] || "Product ("+hs+")";
  const sources = getSelectedSources();

  // Build smart company_info combining question + depth + modules
  const advModules = Array.from(document.querySelectorAll(".mod:checked")).map(e=>e.value);
  let smartPrompt = question || "";
  if(advModules.length > 0){
    smartPrompt += (smartPrompt?" — ":"") + "Focus: " + advModules.join(", ");
  }
  smartPrompt += " | Depth: " + currentDepth;
  smartPrompt += " | Intent: " + currentIntent;

  // Save for cross-page
  try{ localStorage.setItem("wx_ei_hs",hs); localStorage.setItem("wx_ei_country",country); }catch(_){}

  // Show output card + loader
  qs("outputCard").style.display = "block";
  qs("outputCard").scrollIntoView({behavior:"smooth", block:"start"});
  qs("aiLoader").classList.add("show");
  qs("disclaimer").style.display = "none";
  qs("reportBox").innerHTML = "";
  qs("runBtn").disabled = true;
  qs("runBtn").textContent = "جارٍ التحليل...";
  qs("reportMeta").textContent = productName + " ← " + country;

  // Animate loader steps
  setLoaderStep(1);
  const stepTimer = setInterval(()=>{
    const current = [...document.querySelectorAll(".loader-step.active")];
    if(current.length > 0){
      const idx = parseInt(current[0].id.replace("ls",""));
      if(idx < 4) setLoaderStep(idx+1);
    }
  }, 8000);

  try{
    const res = await fetchWT(backendUrl+"/api/ai/export-advisor", {
      method:"POST",
      headers:{"Content-Type":"application/json","Authorization":"Bearer "+token},
      body: JSON.stringify({
        hs_code: hs,
        product: productName,
        target_market: country,
        company_info: smartPrompt,
        sources_mode: sources.join(",")
      })
    });

    const data = await res.json().catch(()=>({}));
    if(!res.ok){
      qs("reportBox").innerHTML = `<div style="color:var(--bad);padding:20px;">خطأ (${res.status}): ${data.error||data.message||"Unknown error"}</div>`;
      return;
    }

    const text = typeof data.advisor==="string" ? data.advisor : (data.advisor?.text || JSON.stringify(data,null,2));
    const wordCount = text.split(/\s+/).length;

    qs("reportBox").innerHTML = marked.parse(text);
    qs("disclaimer").style.display = "block";
    qs("reportMeta").textContent = `${productName} ← ${country} | ~${wordCount.toLocaleString()} كلمة`;

    setLoaderStep(5);

  } catch(err){
    qs("reportBox").innerHTML = `<div style="color:var(--bad);padding:20px;">خطأ في الاتصال: ${err.message}</div>`;
    qs("formError").textContent = err.message;
  } finally {
    clearInterval(stepTimer);
    qs("aiLoader").classList.remove("show");
    qs("runBtn").disabled = false;
    qs("runBtn").innerHTML = "<span>▶</span> تشغيل Export Intelligence";
  }
}

// ── Copy
function copyReport(){
  const text = qs("reportBox")?.innerText || "";
  if(!text.trim()){ alert("لا يوجد محتوى للنسخ"); return; }
  const copy = () => {
    const ta = document.createElement("textarea");
    ta.value = text;
    ta.style.cssText = "position:fixed;top:0;left:0;opacity:0;";
    document.body.appendChild(ta);
    ta.focus(); ta.select();
    try{ document.execCommand("copy"); alert("✅ تم النسخ — "+text.length.toLocaleString()+" حرف"); }
    catch(e){ alert("فشل النسخ"); }
    document.body.removeChild(ta);
  };
  if(navigator.clipboard && window.isSecureContext){
    navigator.clipboard.writeText(text)
      .then(()=>alert("✅ تم النسخ — "+text.length.toLocaleString()+" حرف"))
      .catch(copy);
  } else { copy(); }
}

// ── Export PDF
function exportPDF(){
  const htmlContent = qs("reportBox")?.innerHTML?.trim() || "";
  const plainText = qs("reportBox")?.innerText?.trim() || "";
  if(!plainText || plainText.length < 20){ alert("التقرير فارغ"); return; }

  const today = new Date().toLocaleDateString("ar-EG",{year:"numeric",month:"long",day:"numeric"});
  const hs = qs("hsInput").value;
  const country = qs("countryInput").value;
  const product = HS_MAP[hs] || "Export Intelligence";
  const wordCount = plainText.split(/\s+/).length;

  const win = window.open("","_blank","width=900,height=700");
  if(!win){ alert("يرجى السماح بالنوافذ المنبثقة"); return; }

  win.document.write(`<!DOCTYPE html>
<html dir="rtl" lang="ar"><head>
<meta charset="UTF-8"/>
<title>Export Intelligence — ${product}</title>
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&display=swap" rel="stylesheet"/>
<style>
  *{box-sizing:border-box;margin:0;padding:0;}
  body{font-family:'Cairo',Arial,sans-serif;direction:rtl;color:#111;line-height:1.9;font-size:13px;background:#fff;padding:28px 36px;}
  .cover{text-align:center;padding:30px 0 24px;border-bottom:3px solid #1d4ed8;margin-bottom:28px;}
  .cover h1{font-size:24px;color:#1d4ed8;margin-bottom:8px;}
  .cover .badges{display:flex;justify-content:center;gap:8px;flex-wrap:wrap;margin-top:10px;}
  .badge{display:inline-block;background:#dbeafe;color:#1d4ed8;padding:4px 12px;border-radius:999px;font-size:12px;font-weight:700;}
  h1{font-size:19px;color:#1d4ed8;border-bottom:2px solid #bfdbfe;padding-bottom:7px;margin:22px 0 10px;}
  h2{font-size:16px;color:#1e40af;margin:18px 0 8px;}
  h3{font-size:14px;color:#1e3a8a;margin:14px 0 6px;}
  h4{font-size:13px;color:#374151;margin:10px 0 5px;}
  p{margin:7px 0;}
  ul,ol{padding-right:22px;margin:7px 0;}
  li{margin:4px 0;}
  strong{font-weight:700;}
  table{width:100%;border-collapse:collapse;margin:12px 0;font-size:12px;}
  th{background:#1d4ed8;color:#fff;padding:8px 10px;text-align:right;font-weight:700;border:1px solid #1d4ed8;}
  td{padding:7px 10px;border:1px solid #cbd5e1;vertical-align:top;}
  tr:nth-child(even) td{background:#f0f7ff;}
  hr{border:none;border-top:1px solid #e5e7eb;margin:18px 0;}
  code{background:#f3f4f6;padding:2px 5px;border-radius:4px;font-size:11px;}
  .footer{margin-top:32px;padding-top:14px;border-top:1px solid #e5e7eb;text-align:center;color:#9ca3af;font-size:11px;}
  .print-btn{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);background:#1d4ed8;color:#fff;border:none;padding:12px 28px;border-radius:8px;font-size:14px;font-family:Cairo,sans-serif;cursor:pointer;font-weight:700;box-shadow:0 4px 14px rgba(0,0,0,.2);}
  @page{margin:15mm;size:A4;}
  @media print{.print-btn{display:none!important;}body{padding:0;font-size:12px;}h1{font-size:17px;}h2{font-size:14px;}}
</style>
</head><body>
<div class="cover">
  <div style="font-size:32px;margin-bottom:6px;">📊</div>
  <h1>تقرير Export Intelligence</h1>
  <div class="badges">
    <span class="badge">📦 ${product}</span>
    <span class="badge">🌍 ${country}</span>
    <span class="badge">HS: ${hs}</span>
    <span class="badge">~${wordCount.toLocaleString()} كلمة</span>
    <span class="badge">📅 ${today}</span>
  </div>
</div>
${htmlContent}
<div class="footer">WissamXpoHub — AI Export Intelligence | ${today}</div>
<button class="print-btn" onclick="window.print()">🖨️ طباعة / حفظ كـ PDF (Ctrl+P)</button>
<script>setTimeout(()=>window.print(),1800);<\/script>
</body></html>`);
  win.document.close();
}

// ── Back
function goBack(){
  if(document.referrer) history.back();
  else window.location.href = "WissamXpoHub_V3_Frontend_FIXED.html";
}

// ── Auth check
async function checkAuth(){
  let t=0;
  while(typeof window.supabase==="undefined" && t++<30)
    await new Promise(r=>setTimeout(r,100));
  initSB();
  try{
    const{data}=await sb.auth.getSession();
    if(data?.session?.access_token){
      localStorage.setItem("wx_access_token",data.session.access_token);
      qs("authBadge").innerHTML='<span style="color:var(--ok)">✓ '+data.session.user?.email+'</span>';
    } else if(localStorage.getItem("wx_user_email")){
      qs("authBadge").innerHTML='<span style="color:var(--warn)">'+localStorage.getItem("wx_user_email")+'</span>';
    } else {
      qs("authBadge").innerHTML='<span style="color:var(--bad)">غير مسجّل الدخول</span>';
    }
  } catch(_){}
}

// ── Init
function init(){
  const savedHs = localStorage.getItem("wx_ei_hs");
  const savedCountry = localStorage.getItem("wx_ei_country");
  if(savedHs){ qs("hsInput").value=savedHs; onHsInput(); }
  if(savedCountry){ qs("countryInput").value=savedCountry; }
  checkAuth();
}
init();
</script>
</body>
</html>"""

with open("ExportIntelligence.html", "w", encoding="utf-8") as f:
    f.write(HTML)
print("Done - size:", len(HTML))
