import asyncio
import os
import re
from dotenv import load_dotenv
load_dotenv()

LP_TOKEN = os.getenv("LIGHTPANDA_TOKEN", "")
LP_WS = f"wss://cloud.lightpanda.io/ws?token={LP_TOKEN}"
EMAIL = os.getenv("B2B_EMAIL", "")
EP_PASS = os.getenv("EUROPAGES_PASSWORD", "")
WLW_PASS = os.getenv("WLW_PASSWORD", "")

def clean(val):
    if not val: return ""
    return re.sub(r'\s+', ' ', val).strip()

async def login_and_search_europages(product, country):
    from playwright.async_api import async_playwright
    buyers = []
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(LP_WS)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        try:
            # Login
            await page.goto("https://www.europages.co.uk/en/login", timeout=30000, wait_until="domcontentloaded")
            await page.wait_for_timeout(2000)
            await page.evaluate(f"""() => {{
                const niv = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value');
                const e = document.querySelector("input[type='email'],input[name='identifier']");
                const p2 = document.querySelector("input[type='password']");
                if(e){{niv.set.call(e,'{EMAIL}');e.dispatchEvent(new Event('input',{{bubbles:true}}));}}
                if(p2){{niv.set.call(p2,'{EP_PASS}');p2.dispatchEvent(new Event('input',{{bubbles:true}}));}}
                const btn=document.querySelector("button[type='submit']");if(btn)btn.click();
            }}""")
            await page.wait_for_timeout(3000)
            print(f"Logged in: {page.url}")

            # Search
            q = product.replace(" ", "-").lower()
            c = country.lower()
            search_url = f"https://www.europages.co.uk/companies/{c}/{q}.html"
            await page.goto(search_url, timeout=30000, wait_until="domcontentloaded")
            await page.wait_for_timeout(3000)
            print(f"Search URL: {page.url}")
            print(f"Page title: {await page.title()}")
            print(f"Page size: {len(await page.content())}")

            # Print all text content for debugging
            content = await page.content()
            # Look for company names in HTML
            names = re.findall(r'<h[23][^>]*>([^<]{5,80})</h[23]>', content)
            print(f"\nH2/H3 elements found: {len(names)}")
            for n in names[:10]:
                print(f"  - {clean(n)}")

            # Try various selectors
            for sel in ["h2","h3",".company-name","[data-testid*='company']","[class*='company-name']","[class*='CompanyName']"]:
                els = await page.query_selector_all(sel)
                if els:
                    texts = []
                    for el in els[:5]:
                        try:
                            t = clean(await el.inner_text())
                            if t and len(t) > 2: texts.append(t)
                        except: pass
                    if texts:
                        print(f"\n{sel} ({len(els)}): {texts}")

        except Exception as e:
            print(f"ERROR: {e}")
        finally:
            await browser.close()
    return buyers

async def login_and_search_wlw(product, country):
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(LP_WS)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        try:
            # Login
            await page.goto("https://www.wlw.de/en/login", timeout=30000, wait_until="domcontentloaded")
            await page.wait_for_timeout(2000)
            await page.evaluate(f"""() => {{
                const niv = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value');
                const e = document.querySelector("input[type='email'],input[name='identifier']");
                const p2 = document.querySelector("input[type='password']");
                if(e){{niv.set.call(e,'{EMAIL}');e.dispatchEvent(new Event('input',{{bubbles:true}}));}}
                if(p2){{niv.set.call(p2,'{WLW_PASS}');p2.dispatchEvent(new Event('input',{{bubbles:true}}));}}
                const btn=document.querySelector("button[type='submit']");if(btn)btn.click();
            }}""")
            await page.wait_for_timeout(3000)
            print(f"\nWLW Logged in: {page.url}")

            # Search
            q = product.replace(" ", "+")
            search_url = f"https://www.wlw.de/en/find/{q}"
            await page.goto(search_url, timeout=30000, wait_until="domcontentloaded")
            await page.wait_for_timeout(3000)
            print(f"WLW Search: {page.url}")
            print(f"WLW Title: {await page.title()}")

            content = await page.content()
            names = re.findall(r'<h[234][^>]*>([^<]{5,80})</h[234]>', content)
            print(f"H2/H3/H4: {len(names)}")
            for n in names[:10]:
                print(f"  - {clean(n)}")

        except Exception as e:
            print(f"WLW ERROR: {e}")
        finally:
            await browser.close()

async def main():
    print("=== Testing Europages ===")
    await login_and_search_europages("frozen strawberries", "germany")
    print("\n=== Testing WLW ===")
    await login_and_search_wlw("frozen strawberries", "germany")

asyncio.run(main())
