f = open("WissamXpoHub_V3_Frontend_FIXED.html", encoding="utf-8")
html = f.read()
f.close()
import shutil, re
from datetime import datetime
shutil.copy2("WissamXpoHub_V3_Frontend_FIXED.html", f"WissamXpoHub_V3_Frontend_FIXED_BACKUP_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html")

# Fix copyBoxText function
old_copy = """  function copyBoxText(boxId) {
    const box = qs(boxId);
    if (!box) return;
    const text = box.innerText || box.textContent || "";
    navigator.clipboard.writeText(text)
      .then(() => alert("تم النسخ!"))
      .catch(() => {
        const ta = document.createElement("textarea");
        ta.value = text;
        document.body.appendChild(ta);
        ta.select();
        document.execCommand("copy");
        document.body.removeChild(ta);
        alert("تم النسخ!");
      });
  }"""

new_copy = """  function copyBoxText(boxId) {
    const box = qs(boxId);
    if (!box) { alert("لا يوجد محتوى للنسخ"); return; }
    const text = box.innerText || box.textContent || "";
    if (!text.trim()) { alert("التقرير فارغ"); return; }
    const copyFn = () => {
      const ta = document.createElement("textarea");
      ta.value = text;
      ta.style.cssText = "position:fixed;top:0;left:0;opacity:0;";
      document.body.appendChild(ta);
      ta.focus(); ta.select();
      try { document.execCommand("copy"); alert("✅ تم النسخ — " + text.length.toLocaleString() + " حرف"); }
      catch(e) { alert("فشل النسخ: " + e.message); }
      document.body.removeChild(ta);
    };
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(text).then(() => alert("✅ تم النسخ — " + text.length.toLocaleString() + " حرف")).catch(copyFn);
    } else { copyFn(); }
  }"""

if old_copy in html:
    html = html.replace(old_copy, new_copy, 1)
    print("OK1: copyBoxText fixed")
else:
    # Try to find and replace whatever copy function exists
    idx = html.find("function copyBoxText")
    if idx != -1:
        end = html.find("\n  }", idx) + 4
        html = html[:idx] + new_copy[2:] + html[end:]
        print("OK1b: copyBoxText replaced")
    else:
        print("FAIL1: copyBoxText not found")

# Fix exportBoxToPdf to generate real PDF using jsPDF
old_pdf = """  function exportBoxToPdf(title, boxId) {
    const html = qs(boxId)?.innerHTML?.trim() || "";
    const plain = qs(boxId)?.innerText?.trim() || "";
    if (!plain || plain.length < 20) { alert("لا يوجد محتوى للتصدير"); return; }
    const win = window.open("", "_blank");
    if (!win) { alert("السماح بالنوافذ المنبثقة"); return; }
    win.document.write(`<!DOCTYPE html><html dir="rtl"><head>
    <meta charset="UTF-8">
    <title>${title}</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap" rel="stylesheet"/>
    <style>
      body{font-family:'Cairo',Arial,sans-serif;padding:36px;direction:rtl;color:#111;line-height:2;font-size:14px;max-width:860px;margin:0 auto;}
      h1{font-size:22px;color:#1d4ed8;border-bottom:2px solid #1d4ed8;padding-bottom:10px;margin-bottom:6px;}
      h2,h3{color:#1d4ed8;margin:16px 0 8px;font-weight:800;}
      table{width:100%;border-collapse:collapse;margin:12px 0;}
      th{background:#dbeafe;padding:8px;text-align:right;font-weight:700;border:1px solid #93c5fd;}
      td{padding:8px;border:1px solid #cbd5e1;}
      @media print { body{padding:20px;} }
    </style>
    </head><body>
    <h1>${title}</h1>
    ${html}
    <script>window.onload=()=>{window.print();}<\\/script>
    </body></html>`);
    win.document.close();
  }"""

new_pdf = """  function exportBoxToPdf(title, boxId) {
    const box = qs(boxId);
    if (!box) { alert("لا يوجد محتوى"); return; }
    const htmlContent = box.innerHTML?.trim() || "";
    const plainText = box.innerText?.trim() || "";
    if (!plainText || plainText.length < 20) { alert("التقرير فارغ"); return; }

    // Build a printable page and auto-trigger print-to-PDF
    const win = window.open("", "_blank", "width=900,height=700");
    if (!win) { alert("يرجى السماح بالنوافذ المنبثقة ثم المحاولة مرة أخرى"); return; }

    const today = new Date().toLocaleDateString("ar-EG", {year:"numeric",month:"long",day:"numeric"});
    const product = qs("statProduct")?.textContent || "";
    const market  = qs("statMarket")?.textContent || "";
    const hs      = qs("statHs")?.textContent || "";

    win.document.write(`<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
<meta charset="UTF-8"/>
<title>${title}</title>
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&display=swap" rel="stylesheet"/>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: 'Cairo', Arial, sans-serif;
    direction: rtl;
    color: #111;
    line-height: 1.9;
    font-size: 13px;
    background: #fff;
    padding: 30px 40px;
  }
  .cover {
    text-align: center;
    padding: 40px 0 30px;
    border-bottom: 3px solid #1d4ed8;
    margin-bottom: 30px;
  }
  .cover h1 { font-size: 26px; color: #1d4ed8; margin-bottom: 10px; }
  .cover .meta { color: #555; font-size: 13px; margin-top: 10px; line-height: 2; }
  .cover .badge {
    display: inline-block; background: #dbeafe; color: #1d4ed8;
    padding: 4px 14px; border-radius: 999px; font-size: 12px; font-weight: 700; margin: 4px;
  }
  h1 { font-size: 20px; color: #1d4ed8; border-bottom: 2px solid #1d4ed8;
       padding-bottom: 8px; margin: 24px 0 12px; }
  h2 { font-size: 17px; color: #1e40af; margin: 20px 0 10px; }
  h3 { font-size: 15px; color: #1e3a8a; margin: 16px 0 8px; }
  h4 { font-size: 14px; color: #374151; margin: 12px 0 6px; }
  p  { margin: 8px 0; }
  ul, ol { padding-right: 24px; margin: 8px 0; }
  li { margin: 5px 0; }
  strong { color: #111; font-weight: 700; }
  table { width: 100%; border-collapse: collapse; margin: 14px 0; font-size: 12px; }
  th { background: #1d4ed8; color: #fff; padding: 9px 10px; text-align: right; font-weight: 700; border: 1px solid #1d4ed8; }
  td { padding: 8px 10px; border: 1px solid #cbd5e1; vertical-align: top; }
  tr:nth-child(even) td { background: #f0f7ff; }
  hr { border: none; border-top: 1px solid #e5e7eb; margin: 20px 0; }
  code { background: #f3f4f6; padding: 2px 6px; border-radius: 4px; font-size: 12px; }
  .footer { margin-top: 40px; padding-top: 16px; border-top: 1px solid #e5e7eb;
            text-align: center; color: #9ca3af; font-size: 11px; }
  @page { margin: 15mm 15mm 15mm 15mm; size: A4; }
  @media print {
    body { padding: 0; font-size: 12px; }
    h1 { font-size: 18px; } h2 { font-size: 15px; }
    .no-print { display: none !important; }
  }
</style>
</head>
<body>
<div class="cover no-print">
  <div style="font-size:28px;margin-bottom:8px;">📊</div>
  <h1>${title}</h1>
  <div class="meta">
    ${product ? '<span class="badge">📦 ' + product + '</span>' : ''}
    ${market  ? '<span class="badge">🌍 ' + market  + '</span>' : ''}
    ${hs      ? '<span class="badge">HS: ' + hs     + '</span>' : ''}
    <br/><span style="color:#9ca3af">📅 ${today}</span>
  </div>
</div>
${htmlContent}
<div class="footer">
  WissamXpoHub — تقرير AI Export Intelligence | ${today}
</div>
<div class="no-print" style="text-align:center;padding:20px;background:#f0f9ff;border-top:1px solid #bae6fd;">
  <p style="color:#0369a1;font-size:14px;margin-bottom:12px;">⬇️ لتحميل PDF: اضغط Ctrl+P ثم اختر "Save as PDF"</p>
  <button onclick="window.print()" style="background:#1d4ed8;color:#fff;border:none;padding:12px 28px;border-radius:8px;font-size:15px;font-family:Cairo,sans-serif;cursor:pointer;font-weight:700;">
    🖨️ طباعة / حفظ كـ PDF
  </button>
</div>
<script>
  // Auto-focus print dialog after fonts load
  window.onload = function() {
    setTimeout(() => window.print(), 1500);
  };
<\/script>
</body>
</html>`);
    win.document.close();
  }"""

if old_pdf in html:
    html = html.replace(old_pdf, new_pdf, 1)
    print("OK2: PDF function upgraded")
else:
    idx = html.find("function exportBoxToPdf")
    if idx != -1:
        end = html.find("\n  }", idx) + 4
        html = html[:idx] + new_pdf[2:] + html[end:]
        print("OK2b: PDF function replaced")
    else:
        print("FAIL2: exportBoxToPdf not found")

open("WissamXpoHub_V3_Frontend_FIXED.html", "w", encoding="utf-8").write(html)
print("Done - size:", len(html))
