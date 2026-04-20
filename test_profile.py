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
        await page.wait_for_timeout(3000)
        print("Logged in:", "login" not in page.url)

        # Go to first company profile
        await page.goto("https://www.europages.co.uk/companies/germany/frozen-strawberries.html", timeout=30000, wait_until="domcontentloaded")
        await page.wait_for_timeout(3000)
        content = await page.content()

        # Extract company profile links
        profiles = re.findall(r'href="(https://www\.europages\.co\.uk/en/pg/[^"]+)"', content)
        print(f"Profile links found: {len(profiles)}")
        for pr in profiles[:3]:
            print(f"  {pr}")

        if profiles:
            # Visit first profile
            await page.goto(profiles[0], timeout=30000, wait_until="domcontentloaded")
            await page.wait_for_timeout(3000)
            profile_content = await page.content()
            print(f"\nProfile page size: {len(profile_content)}")

            # Extract contact info
            phones = re.findall(r'(\+?[\d\s\-\(\)]{10,20})', profile_content)
            emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', profile_content)
            websites = re.findall(r'https?://(?!www\.europages)([a-zA-Z0-9.-]+\.[a-zA-Z]{2,6})[/"\s]', profile_content)

            print(f"Phones: {phones[:3]}")
            print(f"Emails: {emails[:3]}")
            print(f"Websites: {list(set(websites))[:5]}")

        await browser.close()

asyncio.run(test())
