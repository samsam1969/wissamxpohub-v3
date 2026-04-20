content = open('WissamXpoHub_V3_Frontend_FIXED.html', encoding='utf-8').read()

# Remove the wrongly placed WA button block
import re

# Find the WA button block and remove it
wa_start = content.find('>window.onload=()=>{window.print();}<\\/script>\n\n  <!-- WhatsApp Upgrade Float Button -->')
if wa_start != -1:
    # Find end of WA block (the </script> tag after initWhatsAppBtn)
    wa_end = content.find("  window.addEventListener('storage', initWhatsAppBtn);\n  </script>", wa_start)
    if wa_end != -1:
        wa_end = wa_end + len("  window.addEventListener('storage', initWhatsAppBtn);\n  </script>")
        removed = content[wa_start + len('>window.onload=()=>{window.print();}<\\/script>'):wa_end]
        content = content[:wa_start + len('>window.onload=()=>{window.print();}<\\/script>')] + content[wa_end:]
        print(f'Removed {len(removed)} chars of WA button from wrong location')
    else:
        print('Could not find WA end tag')
else:
    print('WA button not found in wrong location')

# Now add it in the CORRECT place - before the REAL last </body>
wa_html = '''
  <!-- WhatsApp Upgrade Float Button -->
  <div id="waUpgradeBtn" style="display:none;position:fixed;bottom:24px;left:24px;z-index:9999;">
    <a id="waLink" href="#" target="_blank" style="display:flex;align-items:center;gap:10px;background:linear-gradient(135deg,#25d366,#128c7e);color:white;padding:12px 20px;border-radius:50px;text-decoration:none;font-family:Cairo,Arial,sans-serif;font-weight:700;font-size:14px;box-shadow:0 4px 20px rgba(37,211,102,.4);">
      📱 ترقية الباقة
    </a>
  </div>
  <script>
  function initWhatsAppBtn() {
    var btn = document.getElementById("waUpgradeBtn");
    var link = document.getElementById("waLink");
    if (!btn || !link) return;
    var used  = parseInt(localStorage.getItem("wx_plan_used") || "0");
    var limit = parseInt(localStorage.getItem("wx_plan_limit") || "1");
    var type  = localStorage.getItem("wx_plan_type") || "free";
    var email = localStorage.getItem("wx_user_email") || "";
    if (type === "agency") { btn.style.display = "none"; return; }
    var nextPlan = type === "free" ? "Starter 299 جم" : type === "starter" ? "Pro 599 جم" : "Agency 1490 جم";
    var msg = "مرحبا، اريد الاشتراك في باقة " + nextPlan + " - بريدي: " + email + " - استخدمت: " + used + "/" + limit + " تقارير";
    link.href = "https://wa.me/201116415272?text=" + encodeURIComponent(msg);
    if (used >= limit) {
      btn.style.display = "block";
      link.style.background = "linear-gradient(135deg,#ef4444,#dc2626)";
      link.textContent = "وصلت للحد - اشترك الان";
    } else if (used >= limit * 0.8) {
      btn.style.display = "block";
    }
  }
  setTimeout(initWhatsAppBtn, 2000);
  window.addEventListener("storage", initWhatsAppBtn);
  </script>
'''

# Add before the REAL last </body>
real_body_end = content.rfind('\n</body>')
if real_body_end != -1:
    content = content[:real_body_end] + wa_html + content[real_body_end:]
    print('WA button added in correct location')
else:
    print('Could not find real </body>')

open('WissamXpoHub_V3_Frontend_FIXED.html', 'w', encoding='utf-8').write(content)
print('Done')
