content = open('WissamXpoHub_V3_Frontend_FIXED.html', encoding='utf-8').read()

# Find the Login button and add Sign Up next to it
old = '<button type="button" class="primary" id="loginBtn" onclick="loginUser()">Login</button>'

new = '''<button type="button" class="primary" id="loginBtn" onclick="loginUser()">Login</button>
          <button type="button" class="ghost" id="signupBtn" onclick="signupUser()" style="background:rgba(99,102,241,.2);border:1px solid rgba(99,102,241,.4);color:#a5b4fc;padding:10px 20px;border-radius:10px;font-family:Cairo,Arial,sans-serif;font-weight:700;cursor:pointer;font-size:14px;">تسجيل جديد</button>'''

content = content.replace(old, new, 1)

# Add signupUser function after loginUser function
old2 = '  /* Login — open modal */'
new2 = '''  /* Signup */
  function signupUser() {
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
  }

  async function submitSignup() {
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
  }

  /* Login — open modal */'''

content = content.replace(old2, new2, 1)
open('WissamXpoHub_V3_Frontend_FIXED.html', 'w', encoding='utf-8').write(content)
print('Done - Sign Up button added')
