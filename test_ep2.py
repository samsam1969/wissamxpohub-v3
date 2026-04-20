import asyncio
import os
from dotenv import load_dotenv
load_dotenv()

LP_TOKEN = os.getenv("LIGHTPANDA_TOKEN", "")
LP_WS = f"wss://cloud.lightpanda.io/ws?token={LP_TOKEN}"
EMAIL = os.getenv("B2B_EMAIL", "")
EP_PASS = os.getenv("EUROPAGES_PASSWORD", "")

async def test_europages():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(LP_WS)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        # Login
        await page.goto("https://www.europages.co.uk/login", timeout=30000, wait_until="domcontentloaded")
        await page.wait_for_timeout(2000)
        print("Login page:", await page.title())
        print("URL:", page.url)
        
        # Print form fields
        inputs = await page.query_selector_all("input")
        for inp in inputs:
            t = await inp.get_attribute("type")
            n = await inp.get_attribute("name")
            i = await inp.get_attribute("id")
            print(f"  input type={t} name={n} id={i}")
        
        await browser.close()

asyncio.run(test_europages())
