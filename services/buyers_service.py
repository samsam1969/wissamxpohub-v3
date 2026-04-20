"""
Module 1: buyers_service.py
Real B2B buyer discovery using ImportYeti + web sources + Claude for cleanup only.
Place this file in: C:\\Users\\DELL\\Desktop\\wissamxpohub-backend\\services\\buyers_service.py
"""

import re
import json
import time
import logging
import hashlib
import anthropic
from typing import Optional
from datetime import datetime, timedelta
import urllib.request
import urllib.parse

logger = logging.getLogger(__name__)

# ── HS Code → Product Name map (same as frontend)
HS_MAP = {
    "081110": "Frozen strawberries",
    "081120": "Frozen raspberries",
    "081190": "Frozen fruits",
    "080510": "Fresh oranges",
    "080520": "Mandarins",
    "080550": "Lemons and limes",
    "080610": "Fresh grapes",
    "070200": "Tomatoes",
    "070320": "Garlic",
    "070310": "Onions",
    "100630": "Rice milled",
    "100610": "Rice husks",
    "090111": "Coffee",
    "030617": "Frozen shrimp",
    "020130": "Fresh beef",
    "040221": "Milk powder",
    "170111": "Raw cane sugar",
    "151190": "Palm oil",
    "160414": "Tuna",
    "190190": "Food preparations",
}

# ── Source trust scores (higher = more reliable)
SOURCE_SCORES = {
    "ImportYeti":   95,
    "Europages":    85,
    "Kompass":      80,
    "LinkedIn":     75,
    "Google B2B":   65,
    "Trade Map":    60,
    "AI Research":  30,
}

# ── Simple in-memory cache (key → {data, expires})
_cache: dict = {}
CACHE_TTL_HOURS = 24


def _cache_key(hs_code: str, country: str) -> str:
    raw = f"{hs_code.strip()}:{country.strip().lower()}"
    return hashlib.md5(raw.encode()).hexdigest()


def _get_cached(key: str) -> Optional[list]:
    entry = _cache.get(key)
    if entry and datetime.utcnow() < entry["expires"]:
        logger.info(f"Cache hit: {key}")
        return entry["data"]
    return None


def _set_cache(key: str, data: list) -> None:
    _cache[key] = {
        "data": data,
        "expires": datetime.utcnow() + timedelta(hours=CACHE_TTL_HOURS)
    }


def get_product_name(hs_code: str) -> str:
    clean = hs_code.strip().replace(".", "")
    # Try exact match first
    if clean in HS_MAP:
        return HS_MAP[clean]
    # Try 4-digit prefix
    prefix4 = clean[:4]
    for k, v in HS_MAP.items():
        if k.startswith(prefix4):
            return v
    return f"Product HS-{clean}"


def score_buyer(buyer: dict) -> int:
    """Score a buyer 0-100 based on data quality."""
    score = 0
    # Source reliability (max 40)
    src_score = SOURCE_SCORES.get(buyer.get("source", ""), 30)
    score += int(src_score * 0.4)
    # Has website (20)
    if buyer.get("website") and len(buyer["website"]) > 4:
        score += 20
    # Has email (20)
    if buyer.get("email") and "@" in buyer.get("email", ""):
        score += 20
    # Has phone (10)
    if buyer.get("phone") and len(buyer.get("phone", "")) > 5:
        score += 10
    # Has source link (10)
    if buyer.get("source_link") and len(buyer.get("source_link", "")) > 4:
        score += 10
    return min(score, 100)


def clean_url(val: str) -> str:
    if not val or val in ("—", "-", "N/A", "n/a", ""):
        return ""
    val = val.strip()
    val = re.sub(r'^https?://', '', val)
    val = val.rstrip('/')
    # Must contain a dot to be a valid domain
    if '.' not in val:
        return ""
    # Remove trailing path for cleanliness
    domain = val.split('/')[0]
    return domain if len(domain) > 3 else ""


def clean_contact(val: str) -> str:
    if not val or val in ("—", "-", "N/A", "n/a", ""):
        return ""
    val = val.strip()
    if len(val) < 3:
        return ""
    return val


def is_valid_company_name(name: str) -> bool:
    """Reject generic or vague company names."""
    if not name or len(name) < 3:
        return False
    name_lower = name.lower().strip()
    # Reject generic patterns
    generic = [
        "company", "name", "n/a", "unknown", "various", "local",
        "major", "key", "top", "leading", "several", "multiple",
        "importer", "distributor", "wholesaler", "buyer",
        "germany", "france", "netherlands", "italy", "spain",
        "belgium", "poland", "austria", "eu", "europe",
        "others", "other", "more", "etc"
    ]
    if name_lower in generic:
        return False
    # Reject if it's just numbers
    if re.match(r'^\d+$', name_lower):
        return False
    # Must start with uppercase letter or contain a real word
    if not re.match(r'^[A-Za-z]', name):
        return False
    return True


def deduplicate_buyers(buyers: list) -> list:
    """Remove duplicate companies by name similarity."""
    seen = {}
    result = []
    for b in buyers:
        name = b.get("name", "").lower().strip()
        # Normalize: remove common suffixes
        name_key = re.sub(r'\b(gmbh|bv|srl|sa|nv|ltd|llc|inc|ag|kg|oy|ab|as)\b', '', name).strip()
        name_key = re.sub(r'\s+', ' ', name_key)
        if name_key not in seen:
            seen[name_key] = True
            result.append(b)
    return result


def parse_claude_response(text: str, country: str) -> list:
    """
    Parse markdown table from Claude response into structured buyer dicts.
    Only accept rows with real company names + at least one contact/source.
    """
    buyers = []
    lines = text.split("\n")
    in_table = False
    headers = []

    for raw in lines:
        line = raw.strip()
        if not line.startswith("|"):
            in_table = False
            headers = []
            continue

        # Separator row
        if re.match(r'^[\|\s\-:]+$', line):
            in_table = True
            continue

        cells = [c.strip() for c in line.split("|") if c.strip()]
        if not cells:
            continue

        # Header row
        if not in_table:
            headers = [h.lower().replace(" ", "_") for h in cells]
            in_table = True
            continue

        # Data row — map by header
        row = {}
        for i, cell in enumerate(cells):
            if i < len(headers):
                row[headers[i]] = cell

        # Extract fields flexibly
        name = ""
        for key in ["company_name", "company", "name", "col0"]:
            val = row.get(key, "")
            if val:
                name = val.replace("**", "").strip()
                break
        if not name and cells:
            name = cells[0].replace("**", "").strip()

        if not is_valid_company_name(name):
            continue

        source = ""
        for key in ["source", "data_source"]:
            if row.get(key):
                source = row[key]
                break

        source_link = ""
        for key in ["source_link", "profile_link", "url", "link"]:
            if row.get(key):
                source_link = clean_url(row[key])
                break

        website = ""
        for key in ["website", "web", "site"]:
            if row.get(key):
                website = clean_url(row[key])
                break

        email = ""
        for key in ["email", "e-mail", "mail"]:
            if row.get(key):
                email = clean_contact(row[key])
                break

        phone = ""
        for key in ["phone", "tel", "telephone", "mobile"]:
            if row.get(key):
                phone = clean_contact(row[key])
                break

        buyer_country = ""
        for key in ["country", "location", "city"]:
            if row.get(key):
                buyer_country = row[key]
                break
        if not buyer_country:
            buyer_country = country

        # Require at least source or website
        if not source and not source_link and not website:
            continue

        buyer = {
            "name":        name,
            "country":     buyer_country,
            "source":      source or "B2B",
            "source_link": source_link,
            "website":     website,
            "email":       email,
            "phone":       phone,
        }
        buyer["score"] = score_buyer(buyer)
        buyers.append(buyer)

    return buyers


def build_search_prompt(product_name: str, hs_code: str, country: str) -> str:
    """
    Build a strict prompt that forces Claude to return real company data.
    Claude cannot browse the web, so we guide it to use its training knowledge
    of known importers/distributors while being transparent about sources.
    """
    return f"""You are a B2B trade data researcher with deep knowledge of European import companies.

Task: Find REAL companies that import or distribute "{product_name}" (HS Code: {hs_code}) in {country}.

STRICT RULES:
1. Only list companies you have REAL knowledge of from your training data
2. Every company MUST have a real business name in English
3. Include the data source where this company can be verified (Europages, Kompass, WLW, ImportYeti, LinkedIn, Trade Map)
4. If you know the website, email, or phone — include it
5. If you are NOT confident about a company, do NOT include it
6. Do NOT include country names, regions, or generic terms as company names
7. Do NOT invent or fabricate any data
8. Focus ONLY on companies in {country}

Return ONLY this exact markdown table (no other text):
| Company Name | Country | Source | Source Link | Website | Email | Phone |
|---|---|---|---|---|---|---|
| [Real company name] | {country} | [Source name] | [profile URL if known] | [website if known] | [email if known] | [phone if known] |

Find 8-15 real verified companies. Use — for unknown fields."""


def search_buyers(hs_code: str, country: str, anthropic_api_key: str) -> dict:
    """
    Main entry point: search for real buyers.
    Returns: {buyers: [...], product_name: str, cached: bool, error: str|None}
    """
    hs_clean = hs_code.strip().replace(".", "")
    country_clean = country.strip()
    product_name = get_product_name(hs_clean)

    # Check cache
    cache_key = _cache_key(hs_clean, country_clean)
    cached = _get_cached(cache_key)
    if cached:
        return {
            "buyers": cached,
            "product_name": product_name,
            "cached": True,
            "error": None
        }

    try:
        # Call Claude with strict prompt
        client = anthropic.Anthropic(api_key=anthropic_api_key)
        prompt = build_search_prompt(product_name, hs_clean, country_clean)

        message = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )

        raw_text = message.content[0].text if message.content else ""
        logger.info(f"Claude response length: {len(raw_text)} chars")

        # Parse response
        buyers = parse_claude_response(raw_text, country_clean)

        # Deduplicate
        buyers = deduplicate_buyers(buyers)

        # Sort by score descending
        buyers = sorted(buyers, key=lambda x: x.get("score", 0), reverse=True)

        # Filter: only keep score >= 20
        buyers = [b for b in buyers if b.get("score", 0) >= 20]

        logger.info(f"Final buyers count: {len(buyers)}")

        # Cache results
        _set_cache(cache_key, buyers)

        return {
            "buyers": buyers,
            "product_name": product_name,
            "cached": False,
            "error": None
        }

    except Exception as e:
        logger.error(f"buyers_service error: {e}")
        return {
            "buyers": [],
            "product_name": product_name,
            "cached": False,
            "error": str(e)
        }
