"""
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
    return "\n".join(lines)

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
    return "\n".join(lines)
