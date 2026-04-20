import asyncio
import os
from dotenv import load_dotenv
load_dotenv()

LP_TOKEN = os.getenv("LIGHTPANDA_TOKEN", "")
LP_WS = f"wss://cloud.lightpanda.io/ws?token={LP_TOKEN}"
EMAIL = os.getenv("B2B_EMAIL", "")
EP_PASS = os.getenv("EUROPAGES_PASSWORD", "")
WLW_PASS = os.getenv("WLW_PASSWORD", "")

print("Testing with:")
print("  Email:", EMAIL)
print("  EP Pass length:", len(EP_PASS))
print("  WLW Pass length:", len(WLW_PASS))

FILL_JS = """(creds) => {
    const niv = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value');
    const emailEl = document.querySelector("input[name='identifier'],input[type='email'],#email,input[name='email']");
    const passEl  = document.querySelector("input[type='password']");
    if (!emailEl || !passEl) return {ok: false, msg: "fields not found"};
    niv.set.call(emailEl, creds.email);
    emailEl.dispatchEvent(new Event('input', {bubbles: true}));
    emailEl.dispatchEvent(new Event('change', {bubbles: true}));
    niv.set.call(passEl, creds.pass);
    passEl.dispatchEvent(new Event('input', {bubbles: true}));
    passEl.dispatchEvent(new Event('change', {bubbles: true}));
    return {ok: true, eLen: emailEl.value.length, pLen: passEl.value.length};
}"""

SUBMIT_JS = """() => {
    const btn = document.querySelector("button[type='submit'],input[type='submit']");
    if (btn) { btn.click(); return "clicked"; }
    const form = document.querySelector("form");
    if (form) { form.submit(); return "submitted"; }
    return "no submit found";
}"""

async def do_login(page, login_url, email, password):
    await page.goto(login_url, timeout=30000, wait_until="domcontentloaded")
    await page.wait_for_timeout(2000)
    print(f"  Login page: {await page.title()}")

    result = await page.evaluate(FILL_JS, {"email": email, "pass": password})
    print(f"  Fill result: {result}")

    if result and result.get("ok"):
        sub = await page.evaluate(SUBMIT_JS)
        print(f"  Submit: {sub}")
        await page.wait_for_timeout(4000)
        url = page.url
        print(f"  After URL: {url}")
        return "login" not in url and "flow" not in url
    return False

async def test_europages():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(LP_WS)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        try:
            print("\n=== Europages ===")
            ok = await do_login(page, "https://www.europages.co.uk/en/login", EMAIL, EP_PASS)
            print(f"  Logged in: {ok}")

            if ok:
                await page.goto("https://www.europages.co.uk/companies/germany/frozen-strawberries.html",
                                timeout=30000, wait_until="domcontentloaded")
                await page.wait_for_timeout(3000)
                content = await page.content()
                print(f"  Search page size: {len(content)}")
                import re
                names = re.findall(r'<h[23][^>]*>([^<]{4,60})</h[23]>', content)
                print(f"  Names in H2/H3: {len(names)}")
                for n in names[:10]:
                    print(f"    - {n.strip()}")
        except Exception as e:
            print(f"  ERROR: {e}")
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
            print("\n=== WLW ===")
            ok = await do_login(page, "https://www.wlw.de/en/login", EMAIL, WLW_PASS)
            print(f"  Logged in: {ok}")

            if ok:
                await page.goto("https://www.wlw.de/en/find/frozen+strawberries",
                                timeout=30000, wait_until="domcontentloaded")
                await page.wait_for_timeout(3000)
                content = await page.content()
                print(f"  Search page size: {len(content)}")
                import re
                names = re.findall(r'<h[234][^>]*>([^<]{4,60})</h[234]>', content)
                print(f"  Names in H2/H3/H4: {len(names)}")
                for n in names[:10]:
                    print(f"    - {n.strip()}")
        except Exception as e:
            print(f"  ERROR: {e}")
        finally:
            await browser.close()

async def main():
    await test_europages()
    await test_wlw()

asyncio.run(main())
