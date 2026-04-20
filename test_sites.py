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
        
        # Test 4 sites
        sites = [
            "https://www.europages.co.uk/",
            "https://www.kompass.com/",
            "https://www.importyeti.com/",
            "https://www.wlw.de/en"
        ]
        
        for url in sites:
            try:
                await page.goto(url, timeout=20000, wait_until="domcontentloaded")
                await page.wait_for_timeout(1000)
                title = await page.title()
                print(f"OK  {url} -> {title[:50]}")
            except Exception as e:
                print(f"FAIL {url} -> {str(e)[:60]}")
        
        await browser.close()

asyncio.run(test())
