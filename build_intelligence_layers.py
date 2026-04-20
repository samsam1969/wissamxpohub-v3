"""
build_intelligence_layers.py
Builds 3 services:
1. trade_data_service.py v4 (fixed Comtrade)
2. deepsearch_service.py (OpenAI web search)
3. cbi_scraper_service.py (Lightpanda → CBI/Access2Markets)
Then patches claude_service.py to use all 3.
"""
import os, shutil
from datetime import datetime

BASE = r"C:\Users\DELL\Desktop\wissamxpohub-backend"
SVC  = os.path.join(BASE, "services")

# ══════════════════════════════════════════════════════
# 1. trade_data_service.py v4 — Fixed Comtrade
# ══════════════════════════════════════════════════════
TDS = '''"""
trade_data_service.py v4.0
Fixes: partnerCode=ALL, breakdownMode=classic, netWgt for tons,
       includeDesc=true, exponential backoff, France=250
"""
import urllib.request, urllib.parse, json, logging, hashlib, time
from datetime import datetime, timedelta
logger = logging.getLogger(__name__)

COUNTRY_CODES = {
    "Netherlands":528,"Germany":276,"France":250,"Belgium":56,
    "Italy":381,"Spain":724,"Poland":616,"Austria":40,"Sweden":752,
    "Denmark":208,"Finland":246,"Portugal":620,"Greece":300,
    "Czech Republic":203,"Romania":642,"Hungary":348,"Bulgaria":100,
}
EGYPT_CODE = 818
BASE_URL   = "https://comtradeapi.un.org/public/v1/preview/C/A/HS"

_cache = {}
CACHE_TTL = 24

def _cache_key(params):
    return hashlib.md5(json.dumps(params, sort_keys=True).encode()).hexdigest()

def _get_cache(key):
    e = _cache.get(key)
    return e["data"] if e and datetime.utcnow() < e["exp"] else None

def _set_cache(key, data):
    _cache[key] = {"data": data, "exp": datetime.utcnow() + timedelta(hours=CACHE_TTL)}

def _fetch_one(params: dict) -> list:
    # Add required params for correct results
    full_params = {
        **params,
        "partnerCode":    "ALL",
        "breakdownMode":  "classic",
        "customsCode":    "C00",
        "motCode":        "0",
        "includeDesc":    "true",
    }
    key = _cache_key(full_params)
    cached = _get_cache(key)
    if cached is not None:
        logger.info(f"Cache hit: {params.get('period')}")
        return cached

    url = BASE_URL + "?" + urllib.parse.urlencode(full_params)
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent":"WissamXpoHub/4.0"})
            with urllib.request.urlopen(req, timeout=15) as r:
                data = json.loads(r.read().decode("utf-8")).get("data", [])
                _set_cache(key, data)
                return data
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = (2 ** attempt) + 1
                logger.warning(f"Rate limit hit, waiting {wait}s...")
                time.sleep(wait)
            else:
                logger.warning(f"HTTP {e.code}: {e}")
                return []
        except Exception as e:
            logger.warning(f"Fetch error attempt {attempt+1}: {e}")
            time.sleep(1)
    return []

def _fetch_years(flow, reporter_code, hs_code, years):
    all_records = []
    for yr in years:
        records = _fetch_one({"flowCode":flow,"reporterCode":str(reporter_code),"cmdCode":hs_code,"period":yr})
        # Filter: only C00 (total customs) to prevent double counting
        records = [r for r in records if r.get("customsCode","C00") in ("C00","")]
        all_records.extend(records)
        time.sleep(0.5)
    return all_records

def _summarize(records):
    by_year = {}
    for r in records:
        yr      = str(r.get("period",""))
        val     = float(r.get("primaryValue") or 0)
        # Use netWgt (kg→tons) — correct per Comtrade guidance
        net_wgt = float(r.get("netWgt") or 0) / 1000
        partner = r.get("partnerDesc") or r.get("partner","")
        if not yr: continue
        if yr not in by_year:
            by_year[yr] = {"value":0,"tons":0,"partners":{}}
        by_year[yr]["value"] += val
        by_year[yr]["tons"]  += net_wgt
        if partner and partner not in ("World",""):
            p = by_year[yr]["partners"]
            p[partner] = p.get(partner,0) + val
    return by_year

def _cagr(v1, v2, years):
    if not v1 or not v2 or years <= 0: return None
    return ((v2/v1)**(1/years)-1)*100

def _timeseries(by_year, label, src_tag):
    lines = [f"  [{label}]"]
    years = sorted(by_year.keys())
    prev_val, year_vals = None, []
    fetch_time = datetime.utcnow().strftime("%Y-%m-%d")
    for yr in years:
        d = by_year[yr]
        yoy = ""
        if prev_val and prev_val > 0:
            chg = (d["value"]-prev_val)/prev_val*100
            arrow = "▲" if chg >= 0 else "▼"
            yoy = f"  YoY:{arrow}{abs(chg):.1f}%"
        uv = d["value"]/d["tons"] if d["tons"] > 0 else 0
        uv_str = f"  Unit=${uv:,.0f}/ton" if uv > 0 else "  Unit=N/A"
        lines.append(
            f"  {yr}: Value=${d['value']:,.0f}USD | Wgt={d['tons']:,.1f}mt{uv_str}{yoy}"
            f"  [src:{src_tag}|{yr}|fetched:{fetch_time}|breakdownMode:classic|customsCode:C00]"
        )
        prev_val = d["value"]
        year_vals.append((yr, d["value"], d["tons"]))
    if len(year_vals) >= 2:
        y1,v1,q1 = year_vals[0]; y2,v2,q2 = year_vals[-1]
        n = int(y2)-int(y1)
        cv = _cagr(v1,v2,n); cq = _cagr(q1,q2,n)
        if cv is not None:
            trend = "📈 نمو" if cv>2 else ("📉 تراجع" if cv<-2 else "➡️ مستقر")
            lines.append(f"  CAGR({y1}→{y2}): Value={cv:+.1f}%/yr | Wgt={cq:+.1f}%/yr | {trend}")
            if v2 > 0:
                e24=v2*(1+cv/100); e25=e24*(1+cv/100); e26=e25*(1+cv/100)
                lines.append(
                    f"  CAGR estimates: 2024≈${e24:,.0f} | 2025≈${e25:,.0f} | 2026≈${e26:,.0f}"
                    f"  [ESTIMATE-NOT-OFFICIAL]"
                )
    return "\\n".join(lines)

def fetch_real_trade_data(hs_code: str, country: str) -> str:
    hs = hs_code.strip()[:6]
    reporter_code = COUNTRY_CODES.get(country)
    if not reporter_code:
        return f"[No country code for {country}]"
    years = ["2020","2021","2022","2023"]
    fetch_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    imp = _fetch_years("M", reporter_code, hs, years)
    exp = _fetch_years("X", EGYPT_CODE, hs, years)
    imp_by_yr = _summarize(imp)
    exp_by_yr = _summarize(exp)
    lines = [
        "╔══════════════════════════════════════════════════════════════════╗",
        "║  VERIFIED — UN Comtrade Official (classic mode, C00, netWgt)   ║",
        "║  SCOPE RULE: Use country figures only. EU = CONTEXT not TARGET ║",
        "╚══════════════════════════════════════════════════════════════════╝",
        f"HS:{hs} | Market:{country}(#{reporter_code}) | Egypt:#{EGYPT_CODE} | {fetch_time}",
        "⚠️ Preview API: up to 500 records. Figures are indicative.",
        "",
    ]
    if imp_by_yr:
        lines.append(f"━━ {country} IMPORTS — HS {hs} ━━")
        lines.append(_timeseries(imp_by_yr, f"{country} Imports", f"Comtrade/M/{country}"))
        latest = max(imp_by_yr.keys())
        top = sorted(imp_by_yr[latest]["partners"].items(), key=lambda x:-x[1])[:6]
        if top:
            lines.append(f"  Top suppliers in {latest}:")
            for p,v in top:
                sh = v/imp_by_yr[latest]["value"]*100
                lines.append(f"    → {p}: ${v:,.0f} ({sh:.1f}%)")
        lines.append("")
    if exp_by_yr:
        lines.append(f"━━ EGYPT EXPORTS — HS {hs} ━━")
        lines.append(_timeseries(exp_by_yr, "Egypt Exports", "Comtrade/X/Egypt"))
        latest_e = max(exp_by_yr.keys())
        top_e = sorted(exp_by_yr[latest_e]["partners"].items(), key=lambda x:-x[1])[:6]
        if top_e:
            lines.append(f"  Top destinations in {latest_e}:")
            for p,v in top_e:
                sh = v/exp_by_yr[latest_e]["value"]*100
                lines.append(f"    → {p}: ${v:,.0f} ({sh:.1f}%)")
        lines.append("")
    lines += [
        "══════════════════════════════════════════════════════════════════",
        "AI RULES: (1) Use ONLY above numbers for {country}",
        "(2) Label 2024+ as [ESTIMATE] (3) Never mix EU totals with country",
        "(4) Buyer lists = Europages/B2B only, NOT Comtrade",
        "══════════════════════════════════════════════════════════════════",
    ]
    return "\\n".join(lines)
'''

# ══════════════════════════════════════════════════════
# 2. deepsearch_service.py — OpenAI Web Search
# ══════════════════════════════════════════════════════
DS = '''"""
deepsearch_service.py
OpenAI Responses API with web_search_preview tool.
Fetches recent 2024-2025 market data not in Comtrade yet.
"""
import os, json, logging
from dotenv import load_dotenv
load_dotenv()
logger = logging.getLogger(__name__)

OPENAI_KEY = os.getenv("OPENAI_API_KEY","")

def deep_search(query: str, max_results: int = 5) -> str:
    """Search the web for recent trade/market data using OpenAI."""
    if not OPENAI_KEY or OPENAI_KEY == "sk-your-key-here":
        return "[DeepSearch unavailable: no OPENAI_API_KEY]"
    try:
        import urllib.request, urllib.parse
        payload = json.dumps({
            "model": "gpt-4o-mini",
            "tools": [{"type": "web_search_preview"}],
            "input": query,
            "max_output_tokens": 1500
        }).encode("utf-8")
        req = urllib.request.Request(
            "https://api.openai.com/v1/responses",
            data=payload,
            headers={
                "Authorization": f"Bearer {OPENAI_KEY}",
                "Content-Type": "application/json"
            }
        )
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.loads(r.read().decode("utf-8"))
            # Extract text from response
            output = data.get("output", [])
            texts = []
            for item in output:
                if item.get("type") == "message":
                    for c in item.get("content", []):
                        if c.get("type") == "output_text":
                            texts.append(c.get("text",""))
            return "\\n".join(texts) if texts else "[No results]"
    except Exception as e:
        logger.error(f"DeepSearch error: {e}")
        return f"[DeepSearch error: {e}]"

def get_market_intelligence(product: str, hs_code: str, country: str) -> str:
    """Get recent 2024-2025 market data for a product+country."""
    queries = [
        f"{product} import market {country} 2024 2025 statistics price trends",
        f"Egypt {product} export {country} {hs_code} 2024 news",
        f"{product} {country} importers buyers market outlook 2025",
    ]
    results = []
    for q in queries[:2]:  # Limit to 2 searches to save cost
        result = deep_search(q)
        if result and "unavailable" not in result and "error" not in result.lower():
            results.append(f"Search: {q}\\nResult: {result[:800]}")
    if not results:
        return "[No recent web data found]"
    lines = [
        "╔══════════════════════════════════════════════════════╗",
        "║  RECENT WEB DATA (OpenAI DeepSearch 2024-2025)      ║",
        "║  Source: Live web search — not official statistics  ║",
        "╚══════════════════════════════════════════════════════╝",
        "",
    ]
    lines.extend(results)
    lines += [
        "",
        "⚠️ Web data is indicative. Cross-check with official sources.",
        "══════════════════════════════════════════════════════",
    ]
    return "\\n".join(lines)
'''

# ══════════════════════════════════════════════════════
# 3. cbi_scraper_service.py — Lightpanda → CBI
# ══════════════════════════════════════════════════════
CBI = '''"""
cbi_scraper_service.py
Scrapes CBI Netherlands and Access2Markets using Lightpanda.
Returns market trends, requirements, and buyer behavior.
"""
import asyncio, os, re, logging
from dotenv import load_dotenv
load_dotenv()
logger = logging.getLogger(__name__)

LP_TOKEN = os.getenv("LIGHTPANDA_TOKEN","")
LP_WS    = f"wss://cloud.lightpanda.io/ws?token={LP_TOKEN}"

# CBI product URL mapping
CBI_PRODUCTS = {
    "strawberries": "https://www.cbi.eu/market-information/fresh-fruit-vegetables/strawberries",
    "frozen fruit": "https://www.cbi.eu/market-information/processed-fruit-vegetables-edible-nuts/frozen-fruit",
    "vegetables":   "https://www.cbi.eu/market-information/fresh-fruit-vegetables",
    "herbs":        "https://www.cbi.eu/market-information/fresh-fruit-vegetables/herbs-spices",
    "citrus":       "https://www.cbi.eu/market-information/fresh-fruit-vegetables/citrus",
}

def _get_cbi_url(product: str) -> str:
    product_lower = product.lower()
    for key, url in CBI_PRODUCTS.items():
        if key in product_lower:
            return url
    return "https://www.cbi.eu/market-information"

async def _scrape_url(url: str, max_chars: int = 3000) -> str:
    if not LP_TOKEN:
        return ""
    try:
        from playwright.async_api import async_playwright
        async with async_playwright() as p:
            browser = await p.chromium.connect_over_cdp(LP_WS)
            ctx  = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            )
            page = await ctx.new_page()
            await page.goto(url, timeout=25000, wait_until="domcontentloaded")
            await page.wait_for_timeout(2000)
            # Extract main content
            content = await page.evaluate("""() => {
                const sel = [
                    'article', 'main', '.content', '.market-information',
                    '#main-content', '.page-content'
                ];
                for (const s of sel) {
                    const el = document.querySelector(s);
                    if (el) return el.innerText;
                }
                return document.body.innerText;
            }""")
            await browser.close()
            # Clean up
            content = re.sub(r"\\n{3,}", "\\n\\n", content or "")
            return content[:max_chars]
    except Exception as e:
        logger.warning(f"CBI scrape error {url}: {e}")
        return ""

async def _scrape_access2markets(country: str, hs_code: str) -> str:
    """Scrape Access2Markets for tariff info."""
    url = f"https://trade.ec.europa.eu/access-to-markets/en/results?product={hs_code}&origin=EG&destination={country}"
    try:
        from playwright.async_api import async_playwright
        async with async_playwright() as p:
            browser = await p.chromium.connect_over_cdp(LP_WS)
            ctx  = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            )
            page = await ctx.new_page()
            await page.goto(url, timeout=25000, wait_until="domcontentloaded")
            await page.wait_for_timeout(2000)
            content = await page.evaluate("() => document.body.innerText")
            await browser.close()
            content = re.sub(r"\\n{3,}", "\\n\\n", content or "")
            return content[:2000]
    except Exception as e:
        logger.warning(f"Access2Markets scrape error: {e}")
        return ""

def get_cbi_intelligence(product: str, hs_code: str, country: str) -> str:
    """Get CBI market intelligence + Access2Markets tariff data."""
    if not LP_TOKEN:
        return "[CBI scraping unavailable: no LIGHTPANDA_TOKEN]"
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        cbi_url = _get_cbi_url(product)
        cbi_data, a2m_data = loop.run_until_complete(asyncio.gather(
            _scrape_url(cbi_url),
            _scrape_access2markets(country, hs_code),
        ))
        loop.close()
    except Exception as e:
        logger.error(f"CBI intelligence error: {e}")
        return f"[CBI error: {e}]"

    lines = []
    if cbi_data and len(cbi_data) > 100:
        lines += [
            "╔══════════════════════════════════════════════════╗",
            "║  CBI Netherlands — Market Intelligence          ║",
            f"║  Source: {cbi_url[:45]}  ║",
            "╚══════════════════════════════════════════════════╝",
            cbi_data[:2500],
            "",
        ]
    if a2m_data and len(a2m_data) > 50:
        lines += [
            "╔══════════════════════════════════════════════════╗",
            "║  Access2Markets — Tariff & Requirements         ║",
            "║  Egypt → EU market access info                  ║",
            "╚══════════════════════════════════════════════════╝",
            a2m_data[:1500],
            "",
        ]
    if not lines:
        return "[No CBI/Access2Markets data retrieved]"
    return "\\n".join(lines)
'''

# ══════════════════════════════════════════════════════
# Write files
# ══════════════════════════════════════════════════════
files = {
    "trade_data_service.py": TDS,
    "deepsearch_service.py": DS,
    "cbi_scraper_service.py": CBI,
}

for fname, content in files.items():
    path = os.path.join(SVC, fname)
    if os.path.exists(path):
        shutil.copy2(path, path.replace(".py", f"_BACKUP_{datetime.now().strftime('%H%M%S')}.py"))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"OK: {fname} ({len(content):,} chars)")

print("\nAll 3 services written.")
print("Next: patch claude_service.py to use all 3 layers.")
