import asyncio, os, re
from dotenv import load_dotenv
load_dotenv()

LP_TOKEN = os.getenv("LIGHTPANDA_TOKEN","")
LP_WS = f"wss://cloud.lightpanda.io/ws?token={LP_TOKEN}"

async def get_years():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(LP_WS)
        ctx = await browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        page = await ctx.new_page()
        url = "https://www.trademap.org/Country_SelProductCountry_TS.aspx?nvpm=1%7c818%7c%7c%7c%7c081110%7c%7c%7c6%7c1%7c1%7c2%7c2%7c1%7c2%7c1%7c1%7c1"
        await page.goto(url, timeout=25000, wait_until="domcontentloaded")
        await page.wait_for_timeout(3000)

        result = await page.evaluate("""() => {
            const t = document.querySelector('#ctl00_PageContent_MyGridView1');
            if(!t) return null;
            const rows = [];
            t.querySelectorAll('tr').forEach(tr => {
                const cells = [];
                tr.querySelectorAll('td,th').forEach(td => cells.push(td.innerText.trim()));
                if(cells.some(c=>c.length>0)) rows.push(cells);
            });
            return rows.slice(0,25);
        }""")

        print("Full table:")
        for row in result[:6]:
            print(" | ".join(str(c)[:25] for c in row[:8]))

        await browser.close()

asyncio.run(get_years())
