# Create shared auth guard
auth_js = """
// WissamXpoHub — Shared Auth Guard
// Include this in every protected page

const WX_AUTH = {
  SB_URL: "https://hfvhivxpaqnqaooyqmaw.supabase.co",
  SB_KEY: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhmdmhpdnhwYXFucWFvb3lxbWF3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzI0NDg1OTMsImV4cCI6MjA4ODAyNDU5M30.HaTO3Ngeq6oaw9eLddgJpxg-_6fwD6G9aj8EJZSRUcY",
  DASHBOARD: "WissamXpoHub_V3_Frontend_FIXED.html",

  getToken()  { return localStorage.getItem("wx_access_token") || ""; },
  getEmail()  { return localStorage.getItem("wx_user_email")   || ""; },
  isLoggedIn(){ return !!(this.getToken() && this.getEmail()); },

  // Call this on every protected page load
  async guard(redirectIfFail = true) {
    // Check localStorage first (instant)
    if (this.isLoggedIn()) return true;

    // Try Supabase refresh
    try {
      let sb = null;
      let t = 0;
      while (typeof window.supabase === "undefined" && t++ < 20)
        await new Promise(r => setTimeout(r, 100));

      if (typeof window.supabase !== "undefined") {
        sb = window.supabase.createClient(this.SB_URL, this.SB_KEY);
        const { data } = await sb.auth.getSession();
        if (data?.session?.access_token) {
          localStorage.setItem("wx_access_token", data.session.access_token);
          localStorage.setItem("wx_user_email",   data.session.user?.email || "");
          return true;
        }
      }
    } catch(e) { console.warn("Auth guard error:", e); }

    // No session found
    if (redirectIfFail) {
      alert("Please login first");
      window.location.href = this.DASHBOARD;
      return false;
    }
    return false;
  },

  // Save session after login
  save(token, email) {
    localStorage.setItem("wx_access_token", token);
    localStorage.setItem("wx_user_email",   email);
  },

  // Clear session on logout
  clear() {
    localStorage.removeItem("wx_access_token");
    localStorage.removeItem("wx_user_email");
    localStorage.removeItem("wx_user_plan");
    localStorage.removeItem("wx_user_remaining");
  }
};
"""
with open("auth_guard.js", "w", encoding="utf-8") as f:
    f.write(auth_js)
print("OK: auth_guard.js created")
