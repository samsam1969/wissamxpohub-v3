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

        await page.goto("https://www.europages.co.uk/en/login", timeout=30000, wait_until="domcontentloaded")
        await page.wait_for_timeout(2000)
        await page.evaluate(FILL_JS, {"email": EMAIL, "pass": EP_PASS})
        await page.evaluate("()=>{const b=document.querySelector(\"button[type='submit']\");if(b)b.click();}")
        await page.wait_for_timeout(5000)
        await page.wait_for_load_state("networkidle")
        await page.wait_for_timeout(1000)

        search_url = "https://www.europages.co.uk/companies/germany/frozen-strawberries.html"
        try:
            await page.goto(search_url, timeout=30000, wait_until="domcontentloaded")
        except:
            await page.wait_for_timeout(3000)

        content = await page.content()

        # Find ALL href patterns near company names
        # Look for links that contain company-related paths
        all_hrefs = re.findall(r'href="([^"]{10,120})"', content)
        ep_links = [h for h in all_hrefs if 'europages' in h.lower() or h.startswith('/en/')]
        print(f"Europages links: {len(ep_links)}")
        for l in ep_links[:15]:
            print(f"  {l}")

        # Also find context around "Olmuhle" or "GmbH"
        idx = content.find("Solling GmbH")
        if idx > 0:
            print(f"\nContext around first company:")
            print(repr(content[idx-200:idx+200]))

        await browser.close()

asyncio.run(test())
