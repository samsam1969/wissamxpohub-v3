import asyncio
import os
from dotenv import load_dotenv
load_dotenv()

LP_TOKEN = os.getenv("LIGHTPANDA_TOKEN", "")
LP_WS = f"wss://cloud.lightpanda.io/ws?token={LP_TOKEN}"

async def test():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(LP_WS)
        context = await browser.new_context()
        page = await context.new_page()
        
        url = "https://www.europages.com/companies/Germany/frozen+strawberries.html"
        print("Opening:", url)
        await page.goto(url, timeout=30000, wait_until="domcontentloaded")
        await page.wait_for_timeout(3000)
        
        # Get page HTML structure
        content = await page.content()
        print("Page size:", len(content))
        
        # Find company elements
        cards = await page.query_selector_all("[class*='company'], [class*='result'], [class*='card']")
        print("Cards found:", len(cards))
        
        # Print first card HTML
        if cards:
            html = await cards[0].inner_html()
            print("First card HTML:", html[:500])
        
        await browser.close()

asyncio.run(test())
