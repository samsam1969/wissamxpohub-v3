with open('WissamXpoHub_V3_Frontend_FIXED.html', encoding='utf-8') as f:
    content = f.read()

# Find and replace initSupabase + loginUser
start = content.find('  function initSupabase()')
end   = content.find('  function closeLoginModal()')

if start == -1 or end == -1:
    print('ERROR: Could not find auth functions')
    print('initSupabase found:', content.find('function initSupabase()'))
    print('closeLoginModal found:', content.find('function closeLoginModal()'))
else:
    new_auth = '''  function initSupabase() {
    if (!window.supabase) return false;
    if (!supabaseClient) {
      supabaseClient = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
    }
    return true;
  }

  function loginUser() {
    var modal = document.getElementById('loginModal');
    if (!modal) { alert('Modal not found'); return; }
    var emailEl = document.getElementById('loginEmail');
    var passEl  = document.getElementById('loginPassword');
    var errEl   = document.getElementById('loginError');
    if (emailEl) emailEl.value = localStorage.getItem('wx_user_email') || '';
    if (passEl)  passEl.value  = '';
    if (errEl)   errEl.textContent = '';
    modal.style.display = 'flex';
    modal.classList.add('show');
    if (emailEl) setTimeout(function(){ emailEl.focus(); }, 100);
    initSupabase();
  }

  '''

    content = content[:start] + new_auth + content[end:]

    with open('WissamXpoHub_V3_Frontend_FIXED.html', 'w', encoding='utf-8') as f:
        f.write(content)

    print('SUCCESS! Login fixed.')
    print('initSupabase in file:', 'function initSupabase()' in content)
    print('loginUser in file:', 'function loginUser()' in content)