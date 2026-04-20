import asyncio, os, re
from dotenv import load_dotenv
load_dotenv()

LP_TOKEN = os.getenv("LIGHTPANDA_TOKEN","")
LP_WS = f"wss://cloud.lightpanda.io/ws?token={LP_TOKEN}"
EMAIL = os.getenv("B2B_EMAIL","")
EP_PASS = os.getenv("EUROPAGES_PASSWORD","")

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
        await page.goto("https://www.europages.co.uk/en/login", timeout=30000, wait_until="domcontentloaded")
        await page.wait_for_timeout(2000)
        await page.evaluate(FILL_JS, {"email": EMAIL, "pass": EP_PASS})
        await page.evaluate("()=>{const b=document.querySelector(\"button[type='submit']\");if(b)b.click();}")
        
        # Wait for redirect to complete
        await page.wait_for_timeout(5000)
        print("After login URL:", page.url)
        logged_in = "login" not in page.url and "flow" not in page.url
        print("Logged in:", logged_in)

        if not logged_in:
            await browser.close()
            return

        # Now navigate to search - wait for any ongoing navigation first
        await page.wait_for_load_state("networkidle")
        await page.wait_for_timeout(1000)
        
        search_url = "https://www.europages.co.uk/companies/germany/frozen-strawberries.html"
        try:
            await page.goto(search_url, timeout=30000, wait_until="domcontentloaded")
        except Exception as e:
            print(f"Navigation interrupted (expected): {str(e)[:80]}")
            await page.wait_for_timeout(3000)
        
        print("Search URL:", page.url)
        content = await page.content()
        print(f"Page size: {len(content)}")

        # Extract profile links
        profiles = re.findall(r'href="(https://www\.europages\.co\.uk/en/pg/[^"]+)"', content)
        profiles += re.findall(r'href="(/en/pg/[^"]+)"', content)
        print(f"Profiles found: {len(profiles)}")
        for pr in profiles[:5]:
            print(f"  {pr}")

        # Also check what H2/H3 we get
        names = re.findall(r'<h[23][^>]*>([^<]{4,60})</h[23]>', content)
        print(f"Names: {len(names)}")
        for n in names[:5]:
            print(f"  {n.strip()}")

        await browser.close()

asyncio.run(test())
