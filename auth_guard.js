// WissamXpoHub Auth Guard — Shared across all pages
const WX_AUTH = {
  getToken()  { return localStorage.getItem("wx_access_token") || ""; },
  getEmail()  { return localStorage.getItem("wx_user_email")   || ""; },
  isLoggedIn(){ return !!(this.getToken() && this.getEmail()); },

  // Show overlay until auth confirmed
  showAuthOverlay() {
    const el = document.createElement("div");
    el.id = "authOverlay";
    el.style.cssText = "position:fixed;inset:0;background:#060f1e;z-index:9999;display:flex;align-items:center;justify-content:center;";
    el.innerHTML = '<div style="text-align:center;color:#8fabd4;font-family:Cairo,sans-serif;"><div style="width:40px;height:40px;border:3px solid rgba(255,255,255,.1);border-top-color:#60a5fa;border-radius:50%;animation:spin .9s linear infinite;margin:0 auto 16px;"></div><div>Checking authentication...</div><style>@keyframes spin{to{transform:rotate(360deg)}}</style></div>';
    document.body.prepend(el);
  },

  hideAuthOverlay() {
    const el = document.getElementById("authOverlay");
    if (el) el.remove();
  },

  save(token, email) {
    localStorage.setItem("wx_access_token", token);
    localStorage.setItem("wx_user_email",   email);
  },

  clear() {
    ["wx_access_token","wx_user_email","wx_user_plan","wx_user_remaining"].forEach(k => localStorage.removeItem(k));
  },

  async guard() {
    this.showAuthOverlay();

    // Fast check: localStorage
    if (this.isLoggedIn()) {
      this.hideAuthOverlay();
      return true;
    }

    // Try Supabase session refresh
    try {
      let t = 0;
      while (typeof window.supabase === "undefined" && t++ < 20)
        await new Promise(r => setTimeout(r, 100));

      if (typeof window.supabase !== "undefined") {
        const sb = window.supabase.createClient(
          "https://hfvhivxpaqnqaooyqmaw.supabase.co",
          "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhmdmhpdnhwYXFucWFvb3lxbWF3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzI0NDg1OTMsImV4cCI6MjA4ODAyNDU5M30.HaTO3Ngeq6oaw9eLddgJpxg-_6fwD6G9aj8EJZSRUcY"
        );
        const { data } = await sb.auth.getSession();
        if (data?.session?.access_token) {
          this.save(data.session.access_token, data.session.user?.email || "");
          this.hideAuthOverlay();
          return true;
        }
      }
    } catch(e) { console.warn("Guard error:", e); }

    // No auth — redirect
    this.hideAuthOverlay();
    alert("You need to login first.");
    window.location.href = "WissamXpoHub_V3_Frontend_FIXED.html";
    return false;
  }
};
