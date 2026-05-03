"""
trade_data_service.py — Real trade data from UN Comtrade Preview API (no key needed)
"""
import urllib.request
import urllib.parse
import json
import logging

logger = logging.getLogger(__name__)

COUNTRY_CODES = {
    "Netherlands": 528, "Germany": 276, "France": 251,
    "Belgium": 56, "Italy": 381, "Spain": 724, "Poland": 616,
    "Austria": 40, "Sweden": 752, "Denmark": 208, "Finland": 246,
    "Portugal": 620, "Greece": 300, "Czech Republic": 203,
    "Romania": 642, "Hungary": 348, "Bulgaria": 100,
}
EGYPT_CODE = 818
BASE_URL = "https://comtradeapi.un.org/public/v1/preview/C/A/HS"

def _fetch(params: dict) -> list:
    url = BASE_URL + "?" + urllib.parse.urlencode(params)
    logger.info(f"Comtrade: {url}")
    req = urllib.request.Request(url, headers={"User-Agent": "WissamXpoHub/1.0"})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read().decode("utf-8")).get("data", [])

def get_country_imports(hs_code: str, country: str, years=("2022","2023")) -> list:
    code = COUNTRY_CODES.get(country)
    if not code:
        return []
    records = []
    for yr in years:
        try:
            records += _fetch({"flowCode":"M","reporterCode":str(code),"cmdCode":hs_code,"period":yr})
        except Exception as e:
            logger.warning(f"imports {yr}: {e}")
    return records

def get_egypt_exports(hs_code: str, years=("2022","2023")) -> list:
    records = []
    for yr in years:
        try:
            records += _fetch({"flowCode":"X","reporterCode":str(EGYPT_CODE),"cmdCode":hs_code,"period":yr})
        except Exception as e:
            logger.warning(f"egypt exports {yr}: {e}")
    return records

def _summarize(records: list) -> dict:
    by_year = {}
    for r in records:
        yr  = str(r.get("period",""))
        val = float(r.get("primaryValue") or 0)
        qty = float(r.get("qty") or r.get("netWgt") or 0) / 1000
        partner = r.get("partnerDesc","")
        if yr not in by_year:
            by_year[yr] = {"value":0,"qty":0,"partners":{}}
        by_year[yr]["value"] += val
        by_year[yr]["qty"]   += qty
        if partner and partner not in ("World",""):
            p = by_year[yr]["partners"]
            p[partner] = p.get(partner,0) + val
    return by_year

def format_for_claude(hs_code, country, imp_records, exp_records) -> str:
    lines = [
        "╔══════════════════════════════════════════════════════╗",
        "║  VERIFIED DATA — UN COMTRADE OFFICIAL DATABASE      ║",
        "║  Use ONLY these numbers. Do NOT invent other figures ║",
        "╚══════════════════════════════════════════════════════╝",
        f"HS Code: {hs_code}  |  Importing country: {country}",
        "",
    ]

    # Imports
    imp = _summarize(imp_records)
    if imp:
        lines.append(f"── {country} IMPORTS of HS {hs_code} ──")
        for yr in sorted(imp):
            d = imp[yr]
            uv = d["value"]/d["qty"] if d["qty"] else 0
            lines.append(f"  {yr}: Value=${d['value']:,.0f} USD | Qty={d['qty']:,.1f} tons | Unit=${uv:,.0f}/ton")
            top = sorted(d["partners"].items(), key=lambda x:-x[1])[:5]
            for p,v in top:
                sh = v/d["value"]*100 if d["value"] else 0
                lines.append(f"    → {p}: ${v:,.0f} ({sh:.1f}%)")
    else:
        lines.append(f"  No import data returned for {country}")

    lines.append("")

    # Egypt exports
    exp = _summarize(exp_records)
    if exp:
        lines.append("── EGYPT EXPORTS of HS " + hs_code + " (all destinations) ──")
        for yr in sorted(exp):
            d = exp[yr]
            uv = d["value"]/d["qty"] if d["qty"] else 0
            lines.append(f"  {yr}: Value=${d['value']:,.0f} USD | Qty={d['qty']:,.1f} tons | Unit=${uv:,.0f}/ton")
            top = sorted(d["partners"].items(), key=lambda x:-x[1])[:5]
            for p,v in top:
                sh = v/d["value"]*100 if d["value"] else 0
                lines.append(f"    → {p}: ${v:,.0f} ({sh:.1f}%)")
    else:
        lines.append("  No Egypt export data returned")

    lines += [
        "",
        "══════════════════════════════════════════════════════",
        "SOURCE: UN Comtrade Preview API (public.comtradeapi.un.org)",
        "INSTRUCTION: Base your entire analysis on the figures above.",
        "If data is missing, say so explicitly — never substitute estimates.",
        "══════════════════════════════════════════════════════",
    ]
    return "\n".join(lines)

def fetch_real_trade_data(hs_code: str, country: str) -> str:
    hs = hs_code.strip()[:6]
    try:
        imp = get_country_imports(hs, country)
        exp = get_egypt_exports(hs)
        return format_for_claude(hs, country, imp, exp)
    except Exception as e:
        logger.error(f"fetch_real_trade_data: {e}")
        return f"[Trade data unavailable: {e}]"
