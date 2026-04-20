f = open("WissamXpoHub_V3_Frontend_FIXED.html", encoding="utf-8")
html = f.read()
f.close()
import shutil
from datetime import datetime
shutil.copy2("WissamXpoHub_V3_Frontend_FIXED.html", f"WissamXpoHub_V3_Frontend_FIXED_BACKUP_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html")

# Fix updateProductName - null safe
old = """  function updateProductName() {
    const hs      = qs("hs").value.trim();
    const product = hsProductMap[hs] || (hs.length >= 4 ? `Product (${hs})` : "—");
    const country = qs("country").value || "—";

    qs("productNameBox").textContent = `اسم المنتج: ${product}`;
    qs("statProduct").textContent    = product;
    qs("statHs").textContent         = hs || "—";
    qs("statMarket").textContent     = country;
    const badge = qs("countryBadge");
    if (badge) {
      const sel = qs("country");
      badge.textContent = (sel && sel.value === "__ALL__") ? "🌍 27 دولة" : "";
    }
    qs("heroProduct").textContent    = product;
    qs("heroHs").textContent         = hs || "—";
    qs("heroMarket").textContent     = (qs("country") && qs("country").value === "__ALL__") ? "EU-27" : country;
  }"""

new = """  function updateProductName() {
    const hsEl    = qs("hs");
    const cntryEl = qs("country");
    if (!hsEl) return; // element removed from dashboard
    const hs      = hsEl.value.trim();
    const product = hsProductMap[hs] || (hs.length >= 4 ? `Product (${hs})` : "—");
    const country = cntryEl ? cntryEl.value || "—" : "—";

    if (qs("productNameBox")) qs("productNameBox").textContent = `اسم المنتج: ${product}`;
    if (qs("statProduct"))    qs("statProduct").textContent    = product;
    if (qs("statHs"))         qs("statHs").textContent         = hs || "—";
    if (qs("statMarket"))     qs("statMarket").textContent     = country;
    const badge = qs("countryBadge");
    if (badge) {
      badge.textContent = (cntryEl && cntryEl.value === "__ALL__") ? "🌍 27 دولة" : "";
    }
    if (qs("heroProduct")) qs("heroProduct").textContent = product;
    if (qs("heroHs"))      qs("heroHs").textContent      = hs || "—";
    if (qs("heroMarket"))  qs("heroMarket").textContent  = (cntryEl && cntryEl.value === "__ALL__") ? "EU-27" : country;
  }"""

if old in html:
    html = html.replace(old, new, 1)
    open("WissamXpoHub_V3_Frontend_FIXED.html", "w", encoding="utf-8").write(html)
    print("OK - updateProductName fixed")
else:
    # Try to find and patch differently
    idx = html.find("function updateProductName()")
    print("Found at:", idx)
    print(repr(html[idx:idx+100]))
