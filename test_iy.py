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
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        url = "https://www.importyeti.com/search?search=frozen+strawberries"
        await page.goto(url, timeout=30000, wait_until="domcontentloaded")
        await page.wait_for_timeout(4000)
        print("URL:", page.url)
        print("Title:", await page.title())
        print("Page size:", len(await page.content()))
        
        selectors = ["h2","h3","h4",".company","[class*='consignee']","[class*='importer']","[class*='company']","[class*='result']","table tr","td"]
        for sel in selectors:
            els = await page.query_selector_all(sel)
            if els:
                try:
                    text = await els[0].inner_text()
                    print(f"  {sel}: {len(els)} found — first: {text[:80]}")
                except: pass
        
        await browser.close()

asyncio.run(test())
