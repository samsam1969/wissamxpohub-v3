content = """
import asyncio
import json
import logging
import os
import re
from typing import Optional

logger = logging.getLogger(__name__)

LP_TOKEN = os.getenv("LIGHTPANDA_TOKEN", "")
LP_WS = f"wss://cloud.lightpanda.io/ws?token={LP_TOKEN}"

async def _scrape_with_lp(url: str, extract_fn, timeout: int = 30) -> list:
    try:
        from playwright.async_api import async_playwright
        async with async_playwright() as p:
            browser = await p.chromium.connect_over_cdp(LP_WS)
            context = await browser.new_context()
            page = await context.new_page()
            await page.goto(url, timeout=timeout*1000, wait_until="domcontentloaded")
            await page.wait_for_timeout(3000)
            result = await extract_fn(page)
            await browser.close()
            return result
    except Exception as e:
        logger.error(f"Lightpanda error: {e}")
        return []

def _clean(val: str) -> str:
    if not val: return ""
    return re.sub(r"\\s+", " ", val).strip()

async def scrape_europages(product: str, country: str) -> list:
    q = product.replace(" ", "+")
    c = country.lower().replace(" ", "-")
    url = f"https://www.europages.com/companies/{c}/{q}.html"

    async def extract(page):
        buyers = []
        try:
            cards = await page.query_selector_all(".company-card, .company-name, [class*='company']")
            for card in cards[:15]:
                try:
                    name_el = await card.query_selector("h2, h3, .name, [class*='name']")
                    name = _clean(await name_el.inner_text()) if name_el else ""
                    if not name or len(name) < 3: continue
                    web_el = await card.query_selector("a[href*='http']:not([href*='europages'])")
                    website = ""
                    if web_el:
                        href = await web_el.get_attribute("href")
                        website = href.replace("https://","").replace("http://","").split("/")[0] if href else ""
                    buyers.append({
                        "name": name, "country": country,
                        "source": "Europages", "source_link": url,
                        "website": website, "email": "", "phone": ""
                    })
                except: continue
        except Exception as e:
            logger.error(f"Europages extract error: {e}")
        return buyers

    return await _scrape_with_lp(url, extract)

async def scrape_wlw(product: str, country: str) -> list:
    q = product.replace(" ", "+")
    url = f"https://www.wlw.de/en/find/{q}"

    async def extract(page):
        buyers = []
        try:
            cards = await page.query_selector_all(".supplier-tile, .company-tile, [class*='supplier'], [class*='company']")
            for card in cards[:15]:
                try:
                    name_el = await card.query_selector("h2, h3, .name, [class*='name'], strong")
                    name = _clean(await name_el.inner_text()) if name_el else ""
                    if not name or len(name) < 3: continue
                    buyers.append({
                        "name": name, "country": country,
                        "source": "WLW", "source_link": url,
                        "website": "", "email": "", "phone": ""
                    })
                except: continue
        except Exception as e:
            logger.error(f"WLW extract error: {e}")
        return buyers

    return await _scrape_with_lp(url, extract)

async def scrape_kompass(product: str, country: str) -> list:
    q = product.replace(" ", "+")
    url = f"https://www.kompass.com/a/search/?search={q}&lang=en"

    async def extract(page):
        buyers = []
        try:
            cards = await page.query_selector_all(".company-result, .k-result, [class*='result']")
            for card in cards[:15]:
                try:
                    name_el = await card.query_selector("h2, h3, .company-name, [class*='name']")
                    name = _clean(await name_el.inner_text()) if name_el else ""
                    if not name or len(name) < 3: continue
                    phone_el = await card.query_selector("[class*='phone'], .tel")
                    phone = _clean(await phone_el.inner_text()) if phone_el else ""
                    buyers.append({
                        "name": name, "country": country,
                        "source": "Kompass", "source_link": url,
                        "website": "", "email": "", "phone": phone
                    })
                except: continue
        except Exception as e:
            logger.error(f"Kompass extract error: {e}")
        return buyers

    return await _scrape_with_lp(url, extract)

async def scrape_importyeti(product: str) -> list:
    q = product.replace(" ", "%20")
    url = f"https://www.importyeti.com/search?search={q}"

    async def extract(page):
        buyers = []
        try:
            rows = await page.query_selector_all(".consignee-row, .company-row, [class*='consignee'], [class*='importer']")
            for row in rows[:15]:
                try:
                    name_el = await row.query_selector(".name, h3, h4, strong, [class*='name']")
                    name = _clean(await name_el.inner_text()) if name_el else ""
                    if not name or len(name) < 3: continue
                    buyers.append({
                        "name": name, "country": "Various",
                        "source": "ImportYeti", "source_link": url,
                        "website": "", "email": "", "phone": ""
                    })
                except: continue
        except Exception as e:
            logger.error(f"ImportYeti extract error: {e}")
        return buyers

    return await _scrape_with_lp(url, extract)

def search_buyers_live(product: str, hs_code: str, country: str) -> dict:
    if not LP_TOKEN:
        return {"buyers": [], "error": "LIGHTPANDA_TOKEN not set", "sources_used": []}

    async def run_all():
        tasks = [
            scrape_europages(product, country),
            scrape_kompass(product, country),
            scrape_importyeti(product),
        ]
        # Add WLW only for DACH countries
        dach = ["Germany", "Austria", "Switzerland"]
        if country in dach:
            tasks.append(scrape_wlw(product, country))

        results = await asyncio.gather(*tasks, return_exceptions=True)
        all_buyers = []
        sources = []
        for r in results:
            if isinstance(r, list) and r:
                all_buyers.extend(r)
                if r: sources.append(r[0].get("source",""))
        return all_buyers, sources

    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        buyers, sources = loop.run_until_complete(run_all())
        loop.close()

        # Deduplicate by name
        seen = set()
        unique = []
        for b in buyers:
            key = b["name"].lower().strip()
            if key not in seen and len(key) > 2:
                seen.add(key)
                # Add score
                score = 30
                if b.get("website"): score += 20
                if b.get("email"): score += 20
                if b.get("phone"): score += 15
                if b["source"] in ["ImportYeti","Europages"]: score += 15
                b["score"] = min(score, 100)
                unique.append(b)

        unique.sort(key=lambda x: x.get("score",0), reverse=True)
        return {"buyers": unique, "sources_used": list(set(sources)), "error": None}

    except Exception as e:
        logger.error(f"search_buyers_live error: {e}")
        return {"buyers": [], "sources_used": [], "error": str(e)}
"""
with open("services/lightpanda_service.py", "w", encoding="utf-8") as f:
    f.write(content)
print("Done - lightpanda_service.py created")
