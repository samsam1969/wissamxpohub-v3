"""
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
            content = re.sub(r"\n{3,}", "\n\n", content or "")
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
            content = re.sub(r"\n{3,}", "\n\n", content or "")
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
    return "\n".join(lines)
