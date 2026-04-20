content = open('WissamXpoHub_V3_Frontend_FIXED.html', encoding='utf-8').read()

old = '''              <input type="text" id="signupFirstName" placeholder="أحمد" style="width:100%;background:rgba(255,255,255,.05);border:1px solid rgba(99,102,241,.3);border-radius:8px;color:#e2e8f0;padding:10px;font-family:Cairo,Arial,sans-serif"/>
            </div>
            <div>
              <label style="font-size:12px;color:#9ca3af;display:block;margin-bottom:4px">الاسم الأخير *</label>
              <input type="text" id="signupLastName" placeholder="محمد" style="width:100%;background:rgba(255,255,255,.05);border:1px solid rgba(99,102,241,.3);border-radius:8px;color:#e2e8f0;padding:10px;font-family:Cairo,Arial,sans-serif"/>'''

new = '''              <input type="text" id="signupFirstName" placeholder="أحمد" autocomplete="given-name" style="width:100%;background:rgba(255,255,255,.05);border:1px solid rgba(99,102,241,.3);border-radius:8px;color:#e2e8f0;padding:10px;font-family:Cairo,Arial,sans-serif"/>
            </div>
            <div>
              <label style="font-size:12px;color:#9ca3af;display:block;margin-bottom:4px">الاسم الأخير *</label>
              <input type="text" id="signupLastName" placeholder="محمد" autocomplete="family-name" style="width:100%;background:rgba(255,255,255,.05);border:1px solid rgba(99,102,241,.3);border-radius:8px;color:#e2e8f0;padding:10px;font-family:Cairo,Arial,sans-serif"/>'''

content = content.replace(old, new, 1)

# Fix company and phone autocomplete
old2 = '''<input type="text" id="signupCompany" placeholder="شركة التصدير المصري" style="width:100%;background:rgba(255,255,255,.05);border:1px solid rgba(99,102,241,.3);border-radius:8px;color:#e2e8f0;padding:10px;font-family:Cairo,Arial,sans-serif"/>'''
new2 = '''<input type="text" id="signupCompany" placeholder="شركة التصدير المصري" autocomplete="organization" style="width:100%;background:rgba(255,255,255,.05);border:1px solid rgba(99,102,241,.3);border-radius:8px;color:#e2e8f0;padding:10px;font-family:Cairo,Arial,sans-serif"/>'''
content = content.replace(old2, new2, 1)

old3 = '''<input type="tel" id="signupPhone" placeholder="201012345678" style="width:100%;background:rgba(255,255,255,.05);border:1px solid rgba(99,102,241,.3);border-radius:8px;color:#e2e8f0;padding:10px;font-family:Cairo,Arial,sans-serif;direction:ltr"/>'''
new3 = '''<input type="tel" id="signupPhone" placeholder="201012345678" autocomplete="tel" style="width:100%;background:rgba(255,255,255,.05);border:1px solid rgba(99,102,241,.3);border-radius:8px;color:#e2e8f0;padding:10px;font-family:Cairo,Arial,sans-serif;direction:ltr"/>'''
content = content.replace(old3, new3, 1)

# Clear signup fields when modal opens for signup
old4 = '''    // Show extra signup fields
    const extraFields = qs("signupExtraFields");
    if(extraFields) extraFields.style.display = "block";
    qs("loginEmail").value = "";
    qs("loginPassword").value = "";'''

new4 = '''    // Show extra signup fields
    const extraFields = qs("signupExtraFields");
    if(extraFields) extraFields.style.display = "block";
    qs("loginEmail").value = "";
    qs("loginPassword").value = "";
    // Clear signup fields
    if(qs("signupFirstName")) qs("signupFirstName").value = "";
    if(qs("signupLastName")) qs("signupLastName").value = "";
    if(qs("signupCompany")) qs("signupCompany").value = "";
    if(qs("signupPhone")) qs("signupPhone").value = "";'''

content = content.replace(old4, new4, 1)

open('WissamXpoHub_V3_Frontend_FIXED.html', 'w', encoding='utf-8').write(content)
print('Done - autocomplete fixed')
