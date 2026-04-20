import asyncio
import os
from dotenv import load_dotenv
load_dotenv()

LP_TOKEN = os.getenv("LIGHTPANDA_TOKEN", "")
LP_WS = f"wss://cloud.lightpanda.io/ws?token={LP_TOKEN}"

async def test():
    from playwright.async_api import async_playwright
    print("Connecting to Lightpanda...")
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(LP_WS)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("https://example.com", timeout=30000)
        title = await page.title()
        print("OK - Page title:", title)
        await browser.close()

asyncio.run(test())
