import asyncio
import os
from dotenv import load_dotenv
load_dotenv()

LP_TOKEN = os.getenv("LIGHTPANDA_TOKEN", "")
LP_WS = f"wss://cloud.lightpanda.io/ws?token={LP_TOKEN}"
EMAIL = os.getenv("B2B_EMAIL", "")
EP_PASS = os.getenv("EUROPAGES_PASSWORD", "")
IY_PASS = os.getenv("IMPORTYETI_PASSWORD", "")
WLW_PASS = os.getenv("WLW_PASSWORD", "")

print("Email:", EMAIL)
print("EP Pass set:", bool(EP_PASS))
print("IY Pass set:", bool(IY_PASS))
print("WLW Pass set:", bool(WLW_PASS))

async def try_login(name, url, email, password):
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(LP_WS)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        try:
            await page.goto(url, timeout=30000, wait_until="domcontentloaded")
            await page.wait_for_timeout(2000)
            title = await page.title()
            print(f"\n{name}: {title} | {page.url}")
            email_el = await page.query_selector("input[type='email'],input[name='email'],#email,input[name='username']")
            pass_el  = await page.query_selector("input[type='password']")
            print(f"  email={email_el is not None} pass={pass_el is not None}")
            if email_el and pass_el:
                await email_el.fill(email)
                await pass_el.fill(password)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(3000)
                print(f"  After: {await page.title()} | {page.url}")
        except Exception as e:
            print(f"  ERROR: {e}")
        finally:
            await browser.close()

async def main():
    await try_login("Europages", "https://www.europages.co.uk/en/login", EMAIL, EP_PASS)
    await try_login("ImportYeti", "https://www.importyeti.com/login", EMAIL, IY_PASS)
    await try_login("WLW", "https://www.wlw.de/en/login", EMAIL, WLW_PASS)

asyncio.run(main())
