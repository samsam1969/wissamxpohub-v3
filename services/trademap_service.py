"""
trademap_service.py v2
Uses table ID: ctl00_PageContent_MyGridView1
"""
import asyncio, os, re, logging, hashlib
from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv()

logger = logging.getLogger(__name__)
LP_TOKEN = os.getenv("LIGHTPANDA_TOKEN", "")
LP_WS    = f"wss://cloud.lightpanda.io/ws?token={LP_TOKEN}"

_cache = {}
CACHE_TTL = 48

def _ck(h,c): return hashlib.md5(f"tm:{h}:{c}".encode()).hexdigest()
def _gc(k):
    e=_cache.get(k); return e["data"] if e and datetime.utcnow()<e["exp"] else None
def _sc(k,d): _cache[k]={"data":d,"exp":datetime.utcnow()+timedelta(hours=CACHE_TTL)}

TM_EXP = "https://www.trademap.org/Country_SelProductCountry_TS.aspx?nvpm=1%7c818%7c%7c%7c%7c{hs}%7c%7c%7c6%7c1%7c1%7c2%7c2%7c1%7c2%7c1%7c1%7c1"
TM_IMP = "https://www.trademap.org/Country_SelProductCountry_TS.aspx?nvpm=1%7c{rep}%7c%7c%7c%7c{hs}%7c%7c%7c6%7c1%7c1%7c1%7c2%7c1%7c2%7c1%7c1%7c1"

ITC_CODES = {
    "Netherlands":528,"Germany":276,"France":250,"Belgium":56,
    "Italy":381,"Spain":724,"Poland":616,"Austria":40,"Sweden":752,
    "Denmark":208,"Finland":246,"Portugal":620,"Greece":300,
    "Czech Republic":203,"Romania":642,"Hungary":348,
}

async def _scrape(url):
    if not LP_TOKEN: return {}
    try:
        from playwright.async_api import async_playwright
        async with async_playwright() as p:
            browser = await p.chromium.connect_over_cdp(LP_WS)
            ctx = await browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
            page = await ctx.new_page()
            await page.goto(url, timeout=25000, wait_until="domcontentloaded")
            await page.wait_for_timeout(3000)
            result = await page.evaluate("""() => {
                const tbl = document.getElementById('ctl00_PageContent_MyGridView1');
                if (!tbl) return {error: 'no table'};
                const rows = [];
                tbl.querySelectorAll('tr').forEach(tr => {
                    const cells = [];
                    tr.querySelectorAll('td,th').forEach(td => cells.push(td.innerText.trim()));
                    if(cells.some(c=>c.length>0)) rows.push(cells);
                });
                return {rows};
            }""")
            await browser.close()
            return result
    except Exception as e:
        logger.error(f"TM: {e}"); return {}

def _parse(raw):
    rows = raw.get("rows",[])
    if not rows: return {}
    header, data_rows = None, []
    for i, row in enumerate(rows):
        rs = " ".join(row)
        if re.search(r'202[0-9]', rs) and ("value" in rs.lower() or "Exported" in rs or "Imported" in rs):
            header = row; data_rows = rows[i+1:]; break
    if not header: return {}
    years, yidx = [], []
    for j, cell in enumerate(header):
        m = re.search(r'(202[0-9])', cell)
        if m: years.append(m.group(1)); yidx.append(j)
    if not years: return {}
    parsed = []
    for row in data_rows:
        if len(row) < 3: continue
        country = row[1].strip()
        if not country or re.match(r'^[\d\s]+$', country): continue
        vals = {}
        for k, yr in enumerate(years):
            if k < len(yidx) and yidx[k] < len(row):
                s = row[yidx[k]].replace(",","").strip()
                try: vals[yr] = float(s) * 1000
                except: vals[yr] = None
        if any(v for v in vals.values() if v):
            parsed.append({"country": country, "values": vals})
    return {"years": years, "rows": parsed}

def _cagr(v1,v2,n):
    if not v1 or not v2 or n<=0: return None
    return ((v2/v1)**(1/n)-1)*100

def _format(hs, country, exp, imp):
    ft = datetime.utcnow().strftime("%Y-%m-%d")
    # HS scope descriptions
    HS_SCOPE = {
        "080410": "Dates, fresh or dried (HS 080410) — NOT avocado/mango",
        "080440": "Avocados, fresh or dried (HS 080440)",
        "080450": "Guavas, mangoes, mangosteens (HS 080450)",
        "081110": "Frozen strawberries ONLY (HS 081110)",
        "081120": "Frozen raspberries/blackberries (HS 081120)",
        "080510": "Fresh oranges (HS 080510)",
        "070200": "Tomatoes, fresh or chilled (HS 070200)",
        "070310": "Onions and shallots (HS 070310)",
    }
    scope_note = HS_SCOPE.get(hs, f"HS {hs} — verify product scope before analysis")

    lines = [
        "╔══════════════════════════════════════════════════════════════════╗",
        "║  ITC TRADE MAP — Real Data incl. 2024 (preliminary)            ║",
        f"║  HS:{hs} | {country} | {ft}                                    ║",
        "╚══════════════════════════════════════════════════════════════════╝",
        f"[src:ITC Trade Map|trademap.org|USD thousand×1000]",
        f"⚠️ SCOPE: {scope_note}",
        f"⚠️ DATA NOTE: Figures cover ALL products under HS {hs} — not a single product",
        "",
    ]
    def section(data, label):
        if not data.get("rows"): return
        lines.append(f"━━ {label} ━━")
        yrs = data["years"]
        world = next((r for r in data["rows"] if r["country"]=="World"), None)
        if world:
            prev = None
            for yr in sorted(yrs):
                v = world["values"].get(yr)
                if not v: continue
                yoy = ""
                if prev:
                    chg=(v-prev)/prev*100
                    yoy=f"  YoY:{'▲' if chg>=0 else '▼'}{abs(chg):.1f}%"
                lines.append(f"  {yr}: ${v:,.0f} USD{yoy}  [src:TradeMap|{yr}]")
                prev=v
            valid=[(yr,world["values"][yr]) for yr in sorted(yrs) if world["values"].get(yr)]
            if len(valid)>=2:
                y1,v1=valid[0]; y2,v2=valid[-1]
                cg=_cagr(v1,v2,int(y2)-int(y1))
                if cg:
                    lines.append(f"  CAGR({y1}→{y2}): {cg:+.1f}%/yr | {'📈 نمو' if cg>3 else '📉 تراجع'}")
                    if y2=="2024":
                        e25=v2*(1+cg/100); e26=e25*(1+cg/100)
                        lines.append(f"  CAGR-estimates: 2025≈${e25:,.0f} | 2026≈${e26:,.0f}  [ESTIMATE-NOT-OFFICIAL]")
        # Top markets
        latest=max(yrs)
        others=[r for r in data["rows"] if r["country"]!="World"]
        wv=world["values"].get(latest) if world else None
        top=sorted(others,key=lambda r:r["values"].get(latest,0) or 0,reverse=True)[:10]
        if top:
            lines.append(f"\n  Top ({latest}):")
            for r in top:
                v=r["values"].get(latest)
                if v:
                    sh=f" ({v/wv*100:.1f}%)" if wv else ""
                    lines.append(f"    → {r['country']}: ${v:,.0f}{sh}")
        lines.append("")
    section(exp, f"EGYPT EXPORTS HS {hs}")
    section(imp, f"{country} IMPORTS HS {hs}")
    lines += [
        "══════════════════════════════════════════════════════════════════",
        "SOURCE: ITC Trade Map | 2024 data is preliminary",
        "PRIORITY: These figures supersede Comtrade for 2024 analysis",
        "══════════════════════════════════════════════════════════════════",
    ]
    return "\n".join(lines)

def fetch_trademap_data(hs_code: str, country: str) -> str:
    if not LP_TOKEN: return "[Trade Map: no LIGHTPANDA_TOKEN]"
    hs = hs_code.strip()[:6]
    key = _ck(hs, country)
    cached = _gc(key)
    if cached: return cached
    rep = ITC_CODES.get(country, 528)
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        e_raw, i_raw = loop.run_until_complete(asyncio.gather(
            _scrape(TM_EXP.format(hs=hs)),
            _scrape(TM_IMP.format(rep=rep, hs=hs)),
        ))
        loop.close()
        result = _format(hs, country, _parse(e_raw), _parse(i_raw))
        _sc(key, result)
        return result
    except Exception as e:
        return f"[Trade Map error: {e}]"
