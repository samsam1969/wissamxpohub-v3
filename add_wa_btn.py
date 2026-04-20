content = open('WissamXpoHub_V3_Frontend_FIXED.html', encoding='utf-8').read()

wa_btn = '''
  <!-- WhatsApp Upgrade Float Button -->
  <div id="waUpgradeBtn" style="display:none;position:fixed;bottom:24px;left:24px;z-index:9999;">
    <a id="waLink" href="#" target="_blank" style="display:flex;align-items:center;gap:10px;background:linear-gradient(135deg,#25d366,#128c7e);color:white;padding:12px 20px;border-radius:50px;text-decoration:none;font-family:Cairo,Arial,sans-serif;font-weight:700;font-size:14px;box-shadow:0 4px 20px rgba(37,211,102,.4);">
      <svg width="22" height="22" viewBox="0 0 24 24" fill="white"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/><path d="M12 0C5.373 0 0 5.373 0 12c0 2.123.555 4.117 1.528 5.845L.057 23.886l6.184-1.622A11.945 11.945 0 0012 24c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 21.894a9.842 9.842 0 01-5.031-1.378l-.361-.214-3.741.981.998-3.648-.235-.374A9.845 9.845 0 012.106 12C2.106 6.57 6.57 2.106 12 2.106S21.894 6.57 21.894 12 17.43 21.894 12 21.894z"/></svg>
      ترقية الباقة
    </a>
  </div>

  <script>
  function initWhatsAppBtn() {
    const btn = document.getElementById('waUpgradeBtn');
    const link = document.getElementById('waLink');
    if (!btn || !link) return;

    const used  = parseInt(localStorage.getItem('wx_plan_used') || '0');
    const limit = parseInt(localStorage.getItem('wx_plan_limit') || '1');
    const type  = localStorage.getItem('wx_plan_type') || 'free';
    const email = localStorage.getItem('wx_user_email') || '';

    if (type === 'agency') { btn.style.display = 'none'; return; }

    const nextPlan = type === 'free' ? 'Starter (299 ج.م)' : type === 'starter' ? 'Pro (599 ج.م)' : 'Agency (1490 ج.م)';
    const msg = encodeURIComponent('مرحباً، أريد الاشتراك في باقة ' + nextPlan + '%0aبريدي: ' + email + '%0aاستخدمت: ' + used + '/' + limit + ' تقارير');
    link.href = 'https://wa.me/201116415272?text=' + msg;

    if (used >= limit) {
      btn.style.display = 'block';
      btn.querySelector('a').style.background = 'linear-gradient(135deg,#ef4444,#dc2626)';
      btn.querySelector('a').innerHTML = btn.querySelector('a').innerHTML.replace('ترقية الباقة', 'وصلت للحد — اشترك الآن 🔴');
    } else if (used >= limit * 0.8) {
      btn.style.display = 'block';
    }
  }

  setTimeout(initWhatsAppBtn, 2000);
  window.addEventListener('storage', initWhatsAppBtn);
  </script>
'''

content = content.replace('</body>', wa_btn + '\n</body>', 1)
open('WissamXpoHub_V3_Frontend_FIXED.html', 'w', encoding='utf-8').write(content)
print('Done - WhatsApp button added')
