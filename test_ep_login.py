import asyncio
import os
from dotenv import load_dotenv
load_dotenv()

LP_TOKEN = os.getenv("LIGHTPANDA_TOKEN", "")
LP_WS = f"wss://cloud.lightpanda.io/ws?token={LP_TOKEN}"
EMAIL = os.getenv("B2B_EMAIL", "")
EP_PASS = os.getenv("EUROPAGES_PASSWORD", "")

async def test_europages_login():
    from playwright.async_api import async_playwright
    print("Testing Europages login...")
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(LP_WS)
        context = await browser.new_context()
        page = await context.new_page()
        
        # Go to login page
        await page.goto("https://www.europages.com/login", timeout=30000, wait_until="domcontentloaded")
        await page.wait_for_timeout(2000)
        print("Login page loaded:", await page.title())
        
        # Find email/password fields
        email_input = await page.query_selector("input[type='email'], input[name='email'], input[id*='email']")
        pass_input  = await page.query_selector("input[type='password']")
        
        print("Email field found:", email_input is not None)
        print("Password field found:", pass_input is not None)
        
        if email_input and pass_input:
            await email_input.fill(EMAIL)
            await pass_input.fill(EP_PASS)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(3000)
            print("After login URL:", page.url)
            print("After login title:", await page.title())
        
        await browser.close()

asyncio.run(test_europages_login())
