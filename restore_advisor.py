import shutil
from datetime import datetime

f = open("WissamXpoHub_V3_Frontend_FIXED.html", encoding="utf-8")
html = f.read()
f.close()

shutil.copy2("WissamXpoHub_V3_Frontend_FIXED.html", f"WissamXpoHub_V3_Frontend_FIXED_BACKUP_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html")

# Find end of HERO section and insert after it
end_hero = html.find("  </div><!-- end .wrap -->")

advisor_section = """
    <!-- PRODUCT SETUP + AI ADVISOR -->
    <section class="grid" style="margin-top:18px;">

      <!-- Product Setup -->
      <div class="card">
        <div class="card-header">
          <h2>Product Setup</h2>
          <h3>HS Code + target EU market</h3>
        </div>
        <label for="hs">HS Code</label>
        <input id="hs" placeholder="e.g. 081110" value="081110" oninput="updateProductName()"/>
        <div class="product-box" id="productNameBox">Product: Frozen strawberries</div>
        <div class="hint">Don't know the code? <a href="https://www.trademap.org/" target="_blank">Search Trade Map &#8599;</a></div>

        <label for="country">EU Country / Market</label>
        <div style="display:flex;gap:8px;align-items:center;">
          <select id="country" onchange="onCountryChange()" style="flex:1;">
            <option value="__ALL__">All EU (27 countries)</option>
            <optgroup label="Top Markets">
              <option value="Germany">Germany</option>
              <option value="France">France</option>
              <option value="Netherlands">Netherlands</option>
              <option value="Italy">Italy</option>
              <option value="Spain">Spain</option>
              <option value="Belgium">Belgium</option>
              <option value="Poland">Poland</option>
            </optgroup>
            <optgroup label="All 27 EU Countries">
              <option value="Austria">Austria</option>
              <option value="Bulgaria">Bulgaria</option>
              <option value="Croatia">Croatia</option>
              <option value="Cyprus">Cyprus</option>
              <option value="Czech Republic">Czech Republic</option>
              <option value="Denmark">Denmark</option>
              <option value="Estonia">Estonia</option>
              <option value="Finland">Finland</option>
              <option value="Greece">Greece</option>
              <option value="Hungary">Hungary</option>
              <option value="Ireland">Ireland</option>
              <option value="Latvia">Latvia</option>
              <option value="Lithuania">Lithuania</option>
              <option value="Luxembourg">Luxembourg</option>
              <option value="Malta">Malta</option>
              <option value="Portugal">Portugal</option>
              <option value="Romania">Romania</option>
              <option value="Slovakia">Slovakia</option>
              <option value="Slovenia">Slovenia</option>
              <option value="Sweden">Sweden</option>
            </optgroup>
          </select>
          <span id="countryBadge" style="font-size:11px;color:#10b981;font-weight:700;white-space:nowrap;"></span>
        </div>

        <label for="userQuestion">Custom Question (optional)</label>
        <textarea id="userQuestion" placeholder="e.g. Focus on cold chain requirements and top importers..." style="min-height:80px;resize:vertical;"></textarea>

        <div style="display:flex;gap:10px;margin-top:14px;flex-wrap:wrap;">
          <button type="button" class="primary" id="runBtn" onclick="runIntelligence()" style="flex:1;">Run Export Intelligence</button>
          <button type="button" class="ghost" id="resetBtn" onclick="resetAll()">Reset</button>
        </div>
      </div>

      <!-- Navigation to standalone pages -->
      <div class="card">
        <div class="card-header">
          <h2>Tools</h2>
          <h3>Standalone analysis pages</h3>
        </div>
        <div style="display:flex;flex-direction:column;gap:12px;">
          <button type="button" onclick="goToPotentialBuyers()"
            style="width:100%;background:#1e40af;border:none;border-radius:14px;padding:16px 20px;font-size:15px;font-weight:800;font-family:'Cairo',Arial,sans-serif;cursor:pointer;color:#fff;text-align:left;display:flex;align-items:center;gap:12px;">
            <span style="font-size:24px;">&#127970;</span>
            <div>
              <div>Potential Buyers</div>
              <div style="font-size:12px;font-weight:600;color:#93c5fd;margin-top:2px;">Find real importers by HS Code + Country</div>
            </div>
          </button>
          <button type="button" onclick="window.location.href='ExportOpportunityScanner.html'"
            style="width:100%;background:rgba(16,185,129,.15);border:1px solid rgba(16,185,129,.4);border-radius:14px;padding:16px 20px;font-size:15px;font-weight:800;font-family:'Cairo',Arial,sans-serif;cursor:pointer;color:#6ee7b7;text-align:left;display:flex;align-items:center;gap:12px;">
            <span style="font-size:24px;">&#127757;</span>
            <div>
              <div>Export Opportunity Scanner</div>
              <div style="font-size:12px;font-weight:600;color:#6ee7b7;margin-top:2px;opacity:.8;">Discover top 10 export markets</div>
            </div>
          </button>
        </div>

        <!-- Connection status -->
        <div style="margin-top:16px;padding:12px 14px;background:rgba(0,0,0,.2);border:1px solid var(--line);border-radius:12px;">
          <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:8px;">
            <span style="font-size:13px;font-weight:700;">Backend Status</span>
            <button type="button" class="ghost" id="healthBtn" onclick="testConnection()" style="padding:6px 12px;font-size:12px;border-radius:8px;">Test</button>
          </div>
          <div class="status-box" id="connectionStatus" style="margin-top:0;padding:8px 12px;font-size:13px;">Click Test to verify connection</div>
        </div>

        <!-- Developer settings -->
        <details style="margin-top:12px;">
          <summary style="font-size:11px;font-weight:700;color:var(--muted);cursor:pointer;">Developer Settings</summary>
          <div style="margin-top:10px;padding:12px;background:rgba(0,0,0,.2);border-radius:10px;border:1px solid var(--line);">
            <label for="backendUrl" style="font-size:11px;color:var(--muted);font-weight:700;">Backend URL</label>
            <input id="backendUrl" placeholder="http://localhost:4000" value="http://localhost:4000" style="margin-top:4px;margin-bottom:8px;"/>
            <label for="accessToken" style="font-size:11px;color:var(--muted);font-weight:700;">Access Token</label>
            <textarea id="accessToken" style="min-height:50px;font-size:11px;margin-top:4px;filter:blur(4px);" onfocus="this.style.filter='none'" onblur="this.style.filter='blur(4px)'"></textarea>
            <button type="button" class="success" onclick="saveSettings()" style="width:100%;margin-top:8px;font-size:12px;">Save Settings</button>
          </div>
        </details>
      </div>
    </section>

    <!-- AI RESEARCH SETTINGS -->
    <section class="card" style="margin-top:18px;">
      <div class="card-header">
        <h2>AI Research Settings</h2>
        <h3>Sources + report focus</h3>
      </div>
      <div class="research-grid">
        <div>
          <div class="section-label">Selected Sources</div>
          <div class="checks" style="margin-top:8px;">
            <label><input type="checkbox" class="srcOpt" value="trade_map" checked> Trade Map</label>
            <label><input type="checkbox" class="srcOpt" value="access2markets" checked> Access2Markets</label>
            <label><input type="checkbox" class="srcOpt" value="eurostat" checked> Eurostat</label>
            <label><input type="checkbox" class="srcOpt" value="eu_food_safety"> EU Food Safety</label>
            <label><input type="checkbox" class="srcOpt" value="eu_trade_regulations"> EU Trade Regs</label>
            <label><input type="checkbox" class="srcOpt" value="europages"> Europages</label>
            <label><input type="checkbox" class="srcOpt" value="kompass"> Kompass</label>
            <label><input type="checkbox" class="srcOpt" value="cbi"> CBI Netherlands</label>
          </div>
        </div>
        <div>
          <div class="section-label">Report Focus</div>
          <div class="checks" style="margin-top:8px;">
            <label><input type="checkbox" class="infoOpt" value="full_export_brief" checked> Full export brief</label>
            <label><input type="checkbox" class="infoOpt" value="import_statistics" checked> Import statistics</label>
            <label><input type="checkbox" class="infoOpt" value="market_access_rules" checked> Market access rules</label>
            <label><input type="checkbox" class="infoOpt" value="food_safety_requirements"> Food safety</label>
            <label><input type="checkbox" class="infoOpt" value="buyer_list"> Buyer list</label>
            <label><input type="checkbox" class="infoOpt" value="competitor_insights"> Competitor insights</label>
            <label><input type="checkbox" class="infoOpt" value="packaging_labeling"> Packaging</label>
            <label><input type="checkbox" class="infoOpt" value="pricing_strategy"> Pricing strategy</label>
          </div>
        </div>
      </div>
    </section>

    <!-- AI OUTPUT -->
    <section class="dashboard-stack">
      <div class="card">
        <div class="card-header">
          <h2>AI Export Advisor</h2>
          <h3>Backend response — /api/ai/export-advisor</h3>
        </div>
        <div style="display:flex;gap:8px;margin-bottom:12px;flex-wrap:wrap;">
          <button type="button" class="secondary" onclick="copyBoxText('aiBox')" style="padding:8px 14px;font-size:13px;border-radius:10px;">Copy</button>
          <button type="button" class="success" onclick="exportBoxToPdf('AI Export Advisor','aiBox')" style="padding:8px 14px;font-size:13px;border-radius:10px;">PDF</button>
        </div>
        <div class="loader-wrap" id="aiLoader">
          <div class="spinner"></div>
          <div class="loader-text">Running AI Export Advisor...</div>
        </div>
        <div id="aiDisclaimer" style="display:none;margin-bottom:10px;padding:10px 14px;background:rgba(245,158,11,.08);border:1px solid rgba(245,158,11,.3);border-radius:10px;font-size:12px;color:#fbbf24;">
          Statistics sourced from Trade Map, Eurostat, and CBI. Verify before business decisions.
        </div>
        <div class="boxout" id="aiBox">Run Export Intelligence to generate a comprehensive market analysis report.</div>
      </div>
    </section>

"""

html = html[:end_hero] + advisor_section + "\n  " + html[end_hero:]
open("WissamXpoHub_V3_Frontend_FIXED.html", "w", encoding="utf-8").write(html)
print("Done - size:", len(html))
