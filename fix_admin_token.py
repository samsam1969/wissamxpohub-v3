content = open('admin_knowledge.html', encoding='utf-8').read()

old = '''async function getToken() {
  return localStorage.getItem('sb-access-token') ||
         localStorage.getItem('supabase.auth.token') ||
         (() => { try { const k = Object.keys(localStorage).find(k => k.includes('auth')); return k ? JSON.parse(localStorage.getItem(k))?.access_token : null; } catch(e) { return null; } })();
}'''

new = '''async function getToken() {
  // Try all possible Supabase token locations
  const keys = Object.keys(localStorage);
  
  // Method 1: direct key
  for (const k of ['sb-access-token', 'access_token', 'wx_access_token']) {
    const v = localStorage.getItem(k);
    if (v && v.startsWith('eyJ')) return v;
  }
  
  // Method 2: Supabase auth key pattern
  for (const k of keys) {
    if (k.includes('auth-token') || k.includes('supabase')) {
      try {
        const parsed = JSON.parse(localStorage.getItem(k));
        const token = parsed?.access_token || parsed?.currentSession?.access_token;
        if (token && token.startsWith('eyJ')) return token;
      } catch(e) {}
    }
  }
  
  // Method 3: scan all keys for JWT
  for (const k of keys) {
    try {
      const v = localStorage.getItem(k);
      if (v && v.startsWith('eyJ')) return v;
      const parsed = JSON.parse(v);
      if (parsed?.access_token?.startsWith('eyJ')) return parsed.access_token;
    } catch(e) {}
  }
  
  return null;
}'''

content = content.replace(old, new)
open('admin_knowledge.html', 'w', encoding='utf-8').write(content)
print('Done - token detection improved')
