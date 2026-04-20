import asyncio
import os
from dotenv import load_dotenv
load_dotenv()

LP_TOKEN = os.getenv("LIGHTPANDA_TOKEN", "")
LP_WS = f"wss://cloud.lightpanda.io/ws?token={LP_TOKEN}"
EMAIL = os.getenv("B2B_EMAIL", "")
EP_PASS = os.getenv("EUROPAGES_PASSWORD", "")
WLW_PASS = os.getenv("WLW_PASSWORD", "")

async def try_login_js(name, url, email, password):
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(LP_WS)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        try:
            await page.goto(url, timeout=30000, wait_until="domcontentloaded")
            await page.wait_for_timeout(3000)
            print(f"\n{name}: {await page.title()} | {page.url}")

            # Use JS to fill fields directly
            result = await page.evaluate(f"""() => {{
                const emailSel = "input[type='email'],input[name='email'],#email,input[name='identifier']";
                const passSel  = "input[type='password']";
                const emailEl  = document.querySelector(emailSel);
                const passEl   = document.querySelector(passSel);
                if (!emailEl || !passEl) return {{ok: false, msg: "Fields not found"}};
                
                // Set values via native setter
                const nativeInputVal = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value');
                nativeInputVal.set.call(emailEl, '{email}');
                emailEl.dispatchEvent(new Event('input', {{bubbles: true}}));
                emailEl.dispatchEvent(new Event('change', {{bubbles: true}}));
                
                nativeInputVal.set.call(passEl, '{password}');
                passEl.dispatchEvent(new Event('input', {{bubbles: true}}));
                passEl.dispatchEvent(new Event('change', {{bubbles: true}}));
                
                return {{ok: true, email: emailEl.value.length, pass: passEl.value.length}};
            }}""")
            print(f"  JS fill result: {result}")

            if result and result.get("ok"):
                # Submit form
                await page.evaluate("""() => {
                    const form = document.querySelector("form");
                    const btn  = document.querySelector("button[type='submit'],input[type='submit']");
                    if (btn) btn.click();
                    else if (form) form.submit();
                }""")
                await page.wait_for_timeout(4000)
                print(f"  After: {await page.title()} | {page.url}")
                if "login" not in page.url.lower() and "flow" not in page.url.lower():
                    print(f"  SUCCESS!")
                else:
                    print(f"  Still on login page")

        except Exception as e:
            print(f"  ERROR: {str(e)[:200]}")
        finally:
            await browser.close()

async def main():
    await try_login_js("Europages", "https://www.europages.co.uk/en/login", EMAIL, EP_PASS)
    await try_login_js("WLW", "https://www.wlw.de/en/login", EMAIL, WLW_PASS)

asyncio.run(main())
