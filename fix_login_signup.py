content = open('WissamXpoHub_V3_Frontend_FIXED.html', encoding='utf-8').read()

# Fix loginUser to reset modal to login mode
old = '''  function loginUser() {
    // Always show the modal first
    const modal = qs("loginModal");
    if (!modal) return;
    qs("loginEmail").value       = localStorage.getItem("wx_user_email") || "";
    qs("loginPassword").value    = "";
    if(qs("loginError"))qs("loginError").textContent = "";
    modal.classList.add("show");
    setTimeout(() => qs("loginEmail").focus(), 100);
    // Init Supabase silently in background
    initSupabase();
  }'''

new = '''  function loginUser() {
    const modal = qs("loginModal");
    if (!modal) return;
    // Reset to LOGIN mode
    const title = modal.querySelector("h2, .modal-title, h3");
    if(title) title.textContent = "تسجيل الدخول";
    const submitBtn = qs("submitLoginBtn");
    if(submitBtn) { submitBtn.textContent = "دخول"; submitBtn.onclick = submitLogin; }
    // Hide extra signup fields
    const extraFields = qs("signupExtraFields");
    if(extraFields) extraFields.style.display = "none";
    qs("loginEmail").value = localStorage.getItem("wx_user_email") || "";
    qs("loginPassword").value = "";
    if(qs("loginError")) { qs("loginError").textContent = ""; qs("loginError").style.color = "#ef4444"; }
    modal.classList.add("show");
    setTimeout(() => qs("loginEmail").focus(), 100);
    initSupabase();
  }'''

content = content.replace(old, new, 1)

# Fix signupUser to show extra fields
old2 = '''  function signupUser() {
    const modal = qs("loginModal");
    if (!modal) return;
    qs("loginEmail").value = "";
    qs("loginPassword").value = "";
    if(qs("loginError")) qs("loginError").textContent = "";
    // Change modal title to Sign Up
    const title = modal.querySelector("h2, .modal-title, h3");
    if(title) title.textContent = "إنشاء حساب جديد";
    const submitBtn = qs("submitLoginBtn");
    if(submitBtn) {
      submitBtn.textContent = "إنشاء الحساب";
      submitBtn.onclick = submitSignup;
    }
    modal.classList.add("show");
    setTimeout(() => qs("loginEmail").focus(), 100);
    initSupabase();
  }'''

new2 = '''  function signupUser() {
    const modal = qs("loginModal");
    if (!modal) return;
    // Switch to SIGNUP mode
    const title = modal.querySelector("h2, .modal-title, h3");
    if(title) title.textContent = "إنشاء حساب جديد";
    const submitBtn = qs("submitLoginBtn");
    if(submitBtn) { submitBtn.textContent = "إنشاء الحساب"; submitBtn.onclick = submitSignup; }
    // Show extra signup fields
    const extraFields = qs("signupExtraFields");
    if(extraFields) extraFields.style.display = "block";
    qs("loginEmail").value = "";
    qs("loginPassword").value = "";
    if(qs("loginError")) { qs("loginError").textContent = ""; qs("loginError").style.color = "#ef4444"; }
    modal.classList.add("show");
    setTimeout(() => qs("loginEmail").focus(), 100);
    initSupabase();
  }'''

content = content.replace(old2, new2, 1)

# Add extra fields HTML inside the login modal - after password field
old3 = '''        <button type="button" class="primary" id="submitLoginBtn" onclick="submitLogin()" style="flex:1;">دخول</button>'''

new3 = '''        <!-- Extra Signup Fields (hidden by default) -->
        <div id="signupExtraFields" style="display:none;width:100%">
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:10px">
            <div>
              <label style="font-size:12px;color:#9ca3af;display:block;margin-bottom:4px">الاسم الأول *</label>
              <input type="text" id="signupFirstName" placeholder="أحمد" style="width:100%;background:rgba(255,255,255,.05);border:1px solid rgba(99,102,241,.3);border-radius:8px;color:#e2e8f0;padding:10px;font-family:Cairo,Arial,sans-serif"/>
            </div>
            <div>
              <label style="font-size:12px;color:#9ca3af;display:block;margin-bottom:4px">الاسم الأخير *</label>
              <input type="text" id="signupLastName" placeholder="محمد" style="width:100%;background:rgba(255,255,255,.05);border:1px solid rgba(99,102,241,.3);border-radius:8px;color:#e2e8f0;padding:10px;font-family:Cairo,Arial,sans-serif"/>
            </div>
          </div>
          <div style="margin-bottom:10px">
            <label style="font-size:12px;color:#9ca3af;display:block;margin-bottom:4px">اسم الشركة</label>
            <input type="text" id="signupCompany" placeholder="شركة التصدير المصري" style="width:100%;background:rgba(255,255,255,.05);border:1px solid rgba(99,102,241,.3);border-radius:8px;color:#e2e8f0;padding:10px;font-family:Cairo,Arial,sans-serif"/>
          </div>
          <div style="margin-bottom:10px">
            <label style="font-size:12px;color:#9ca3af;display:block;margin-bottom:4px">رقم الهاتف (واتساب)</label>
            <input type="tel" id="signupPhone" placeholder="201012345678" style="width:100%;background:rgba(255,255,255,.05);border:1px solid rgba(99,102,241,.3);border-radius:8px;color:#e2e8f0;padding:10px;font-family:Cairo,Arial,sans-serif;direction:ltr"/>
          </div>
        </div>
        <button type="button" class="primary" id="submitLoginBtn" onclick="submitLogin()" style="flex:1;">دخول</button>'''

content = content.replace(old3, new3, 1)

# Fix submitSignup to save extra data
old4 = '''  async function submitSignup() {
    const email    = qs("loginEmail").value.trim();
    const password = qs("loginPassword").value;
    const errEl    = qs("loginError");
    errEl.textContent = "";
    if (!email || !password) { errEl.textContent = "أدخل البريد الإلكتروني وكلمة المرور"; return; }
    if (password.length < 6) { errEl.textContent = "كلمة المرور يجب أن تكون 6 أحرف على الأقل"; return; }
    if (!initSupabase()) return;
    const submitBtn = qs("submitLoginBtn");
    if(submitBtn) submitBtn.textContent = "جاري إنشاء الحساب...";
    try {
      const { data, error } = await supabaseClient.auth.signUp({ email, password });
      if (error) { errEl.textContent = error.message; if(submitBtn) submitBtn.textContent = "إنشاء الحساب"; return; }
      errEl.style.color = "#4ade80";
      errEl.textContent = "تم إنشاء الحساب! تحقق من بريدك الإلكتروني للتأكيد";
      setTimeout(() => { closeLoginModal(); errEl.style.color = ""; }, 3000);
    } catch(e) {
      errEl.textContent = "خطأ: " + e.message;
      if(submitBtn) submitBtn.textContent = "إنشاء الحساب";
    }
  }'''

new4 = '''  async function submitSignup() {
    const email     = qs("loginEmail").value.trim();
    const password  = qs("loginPassword").value;
    const firstName = qs("signupFirstName")?.value.trim() || "";
    const lastName  = qs("signupLastName")?.value.trim() || "";
    const company   = qs("signupCompany")?.value.trim() || "";
    const phone     = qs("signupPhone")?.value.trim() || "";
    const errEl     = qs("loginError");
    errEl.textContent = "";

    if (!email || !password) { errEl.textContent = "البريد وكلمة المرور مطلوبان"; return; }
    if (!firstName || !lastName) { errEl.textContent = "الاسم الأول والأخير مطلوبان"; return; }
    if (password.length < 6) { errEl.textContent = "كلمة المرور 6 أحرف على الأقل"; return; }
    if (!initSupabase()) return;

    const submitBtn = qs("submitLoginBtn");
    if(submitBtn) submitBtn.textContent = "جاري إنشاء الحساب...";

    try {
      const { data, error } = await supabaseClient.auth.signUp({
        email, password,
        options: {
          data: {
            full_name: firstName + " " + lastName,
            first_name: firstName,
            last_name: lastName,
            company: company,
            phone: phone
          }
        }
      });

      if (error) {
        errEl.textContent = error.message;
        if(submitBtn) submitBtn.textContent = "إنشاء الحساب";
        return;
      }

      // Save to backend
      try {
        const s = getSettings();
        await fetch(s.backendUrl + "/api/auth/register", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            user_id: data.user?.id,
            email, full_name: firstName + " " + lastName,
            phone, company
          })
        });
      } catch(e) { console.log("Backend register:", e); }

      errEl.style.color = "#4ade80";
      errEl.textContent = "تم إنشاء الحساب! تحقق من بريدك للتأكيد";
      setTimeout(() => { closeLoginModal(); errEl.style.color = ""; }, 3000);
    } catch(e) {
      errEl.textContent = "خطأ: " + e.message;
      if(submitBtn) submitBtn.textContent = "إنشاء الحساب";
    }
  }'''

content = content.replace(old4, new4, 1)
open('WissamXpoHub_V3_Frontend_FIXED.html', 'w', encoding='utf-8').write(content)
print('Done - Login/Signup fixed')
