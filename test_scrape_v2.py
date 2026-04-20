import asyncio
import os
from dotenv import load_dotenv
load_dotenv()

LP_TOKEN = os.getenv("LIGHTPANDA_TOKEN", "")
LP_WS = f"wss://cloud.lightpanda.io/ws?token={LP_TOKEN}"
EMAIL = os.getenv("B2B_EMAIL", "")
EP_PASS = os.getenv("EUROPAGES_PASSWORD", "")
WLW_PASS = os.getenv("WLW_PASSWORD", "")

async def safe_fill(page, selector, value):
    """Fill input safely using JS with escaped value"""
    escaped = value.replace("\\", "\\\\").replace("'", "\\'").replace('"', '\\"')
    await page.evaluate(f"""() => {{
        const el = document.querySelector("{selector}");
        if (!el) return;
        const niv = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value');
        niv.set.call(el, "{escaped}");
        el.dispatchEvent(new Event('input', {{bubbles: true}}));
        el.dispatchEvent(new Event('change', {{bubbles: true}}));
    }}""")

async def test_europages():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(LP_WS)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        try:
            await page.goto("https://www.europages.co.uk/en/login", timeout=30000, wait_until="domcontentloaded")
            await page.wait_for_timeout(2000)

            # Fill using safe method
            await safe_fill(page, "input[name='identifier'],input[type='email'],#email", EMAIL)
            await page.wait_for_timeout(500)
            await safe_fill(page, "input[type='password']", EP_PASS)
            await page.wait_for_timeout(500)

            # Submit
            await page.evaluate("() => { const b=document.querySelector(\"button[type='submit']\"); if(b)b.click(); }")
            await page.wait_for_timeout(4000)

            url = page.url
            print(f"Europages after login: {url}")
            logged_in = "login" not in url and "flow" not in url
            print(f"Logged in: {logged_in}")

            if logged_in:
                # Search
                await page.goto("https://www.europages.co.uk/companies/germany/frozen-strawberries.html", timeout=30000, wait_until="domcontentloaded")
                await page.wait_for_timeout(3000)
                print(f"Search page: {page.url}")
                content = await page.content()
                print(f"Content size: {len(content)}")

                import re
                names = re.findall(r'<h[23][^>]*class[^>]*>([^<]{5,60})</h[23]>', content)
                print(f"Company names found: {len(names)}")
                for n in names[:8]:
                    print(f"  {n.strip()}")

        except Exception as e:
            print(f"ERROR: {e}")
        finally:
            await browser.close()

async def test_wlw():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(LP_WS)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        try:
            await page.goto("https://www.wlw.de/en/login", timeout=30000, wait_until="domcontentloaded")
            await page.wait_for_timeout(2000)

            await safe_fill(page, "input[name='identifier'],input[type='email'],#email", EMAIL)
            await page.wait_for_timeout(500)
            await safe_fill(page, "input[type='password']", WLW_PASS)
            await page.wait_for_timeout(500)
            await page.evaluate("() => { const b=document.querySelector(\"button[type='submit']\"); if(b)b.click(); }")
            await page.wait_for_timeout(4000)

            url = page.url
            print(f"\nWLW after login: {url}")
            logged_in = "login" not in url and "flow" not in url
            print(f"Logged in: {logged_in}")

            if logged_in:
                await page.goto("https://www.wlw.de/en/find/frozen+strawberries", timeout=30000, wait_until="domcontentloaded")
                await page.wait_for_timeout(3000)
                content = await page.content()
                print(f"WLW content size: {len(content)}")
                import re
                names = re.findall(r'<h[234][^>]*>([^<]{5,60})</h[234]>', content)
                print(f"Names found: {len(names)}")
                for n in names[:8]:
                    print(f"  {n.strip()}")

        except Exception as e:
            print(f"WLW ERROR: {e}")
        finally:
            await browser.close()

async def main():
    print("=== Europages ===")
    await test_europages()
    print("\n=== WLW ===")
    await test_wlw()

asyncio.run(main())
