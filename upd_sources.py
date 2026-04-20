f = open("WissamXpoHub_V3_Frontend_FIXED.html", encoding="utf-8")
html = f.read()
f.close()
import shutil
from datetime import datetime
shutil.copy2("WissamXpoHub_V3_Frontend_FIXED.html", f"WissamXpoHub_V3_Frontend_FIXED_BACKUP_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html")

old_sources = """      <div class="research-grid">
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
      </div>"""

new_sources = """      <div class="research-grid">
        <div>
          <div class="section-label">Data Sources</div>
          <div class="checks" style="margin-top:8px;">
            <label><input type="checkbox" class="srcOpt" value="trade_map" checked> Trade Map (ITC)</label>
            <label><input type="checkbox" class="srcOpt" value="un_comtrade" checked> UN Comtrade</label>
            <label><input type="checkbox" class="srcOpt" value="access2markets" checked> Access2Markets</label>
            <label><input type="checkbox" class="srcOpt" value="eu_taric" checked> EU TARIC</label>
            <label><input type="checkbox" class="srcOpt" value="eurostat" checked> Eurostat</label>
            <label><input type="checkbox" class="srcOpt" value="cbi"> CBI Netherlands</label>
            <label><input type="checkbox" class="srcOpt" value="eu_food_safety"> EU Food Safety</label>
            <label><input type="checkbox" class="srcOpt" value="eu_trade_regulations"> EU Trade Regs</label>
            <label><input type="checkbox" class="srcOpt" value="europages"> Europages</label>
            <label><input type="checkbox" class="srcOpt" value="globy"> Globy B2B</label>
            <label><input type="checkbox" class="srcOpt" value="export_egypt"> صادر مصر</label>
            <label><input type="checkbox" class="srcOpt" value="egyptian_customs"> الجمارك المصرية</label>
          </div>
        </div>
        <div>
          <div class="section-label">Report Focus</div>
          <div class="checks" style="margin-top:8px;">
            <label><input type="checkbox" class="infoOpt" value="full_export_brief" checked> Full export brief</label>
            <label><input type="checkbox" class="infoOpt" value="import_statistics" checked> Import statistics</label>
            <label><input type="checkbox" class="infoOpt" value="market_access_rules" checked> Market access rules</label>
            <label><input type="checkbox" class="infoOpt" value="food_safety_requirements"> Food safety</label>
            <label><input type="checkbox" class="infoOpt" value="tariff_duties" checked> Tariffs & duties</label>
            <label><input type="checkbox" class="infoOpt" value="buyer_list"> Buyer list</label>
            <label><input type="checkbox" class="infoOpt" value="competitor_insights"> Competitor insights</label>
            <label><input type="checkbox" class="infoOpt" value="packaging_labeling"> Packaging / labeling</label>
            <label><input type="checkbox" class="infoOpt" value="logistics_shipping"> Logistics & shipping</label>
            <label><input type="checkbox" class="infoOpt" value="pricing_strategy"> Pricing strategy</label>
          </div>
        </div>
      </div>"""

if old_sources in html:
    html = html.replace(old_sources, new_sources, 1)
    open("WissamXpoHub_V3_Frontend_FIXED.html", "w", encoding="utf-8").write(html)
    print("OK - sources updated")
else:
    print("Pattern not found")
    idx = html.find("Selected Sources")
    print("Found at:", idx)
