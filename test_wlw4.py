import asyncio, os, re
from dotenv import load_dotenv
load_dotenv()

LP_TOKEN = os.getenv("LIGHTPANDA_TOKEN","")
LP_WS = f"wss://cloud.lightpanda.io/ws?token={LP_TOKEN}"
EMAIL = os.getenv("B2B_EMAIL","")
WLW_PASS = os.getenv("WLW_PASSWORD","")

FILL_JS = """(c) => {
    const niv=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value');
    const e=document.querySelector("input[name='identifier'],input[type='email']");
    const p=document.querySelector("input[type='password']");
    if(!e||!p)return false;
    niv.set.call(e,c.email);e.dispatchEvent(new Event('input',{bubbles:true}));
    niv.set.call(p,c.pass);p.dispatchEvent(new Event('input',{bubbles:true}));
    return true;
}"""

async def test():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(LP_WS)
        ctx = await browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        page = await ctx.new_page()

        # Login
        await page.goto("https://www.wlw.de/en/login", timeout=30000, wait_until="domcontentloaded")
        await page.wait_for_timeout(2000)
        await page.evaluate(FILL_JS, {"email": EMAIL, "pass": WLW_PASS})
        await page.evaluate("()=>{const b=document.querySelector(\"button[type='submit']\");if(b)b.click();}")
        await page.wait_for_timeout(5000)
        print("Logged in:", page.url)

        # Try search with commit (fastest - grabs HTML before JS executes)
        try:
            response = await page.goto("https://www.wlw.de/en/find/frozen+strawberries",
                                       timeout=20000, wait_until="commit")
            await page.wait_for_timeout(2000)
            content = await page.content()
            print("Size:", len(content))
            names = re.findall(r'<h[234][^>]*>([^<]{4,80})</h[234]>', content)
            print(f"Names: {len(names)}")
            for n in names[:5]: print(f"  {n.strip()}")
        except Exception as e:
            print(f"ERROR: {e}")

        await browser.close()

asyncio.run(test())
