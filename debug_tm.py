import asyncio, os
from dotenv import load_dotenv
load_dotenv()

LP_TOKEN = os.getenv("LIGHTPANDA_TOKEN","")
LP_WS = f"wss://cloud.lightpanda.io/ws?token={LP_TOKEN}"

async def debug():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(LP_WS)
        ctx = await browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        page = await ctx.new_page()
        url = "https://www.trademap.org/Country_SelProductCountry_TS.aspx?nvpm=1%7c818%7c%7c%7c%7c081110%7c%7c%7c6%7c1%7c1%7c2%7c2%7c1%7c2%7c1%7c1%7c1"
        await page.goto(url, timeout=25000, wait_until="domcontentloaded")
        await page.wait_for_timeout(3000)

        result = await page.evaluate("""() => {
            const tables = document.querySelectorAll('table');
            const out = [];
            tables.forEach((t, i) => {
                const rows = [];
                t.querySelectorAll('tr').forEach(tr => {
                    const cells = [];
                    tr.querySelectorAll('td,th').forEach(td => cells.push(td.innerText.trim()));
                    if(cells.some(c => c.length > 0)) rows.push(cells);
                });
                if(rows.length > 2) out.push({idx: i, id: t.id, rows: rows.slice(0,10)});
            });
            return out;
        }""")

        for tbl in result:
            print(f"\n=== Table {tbl['idx']} id={repr(tbl['id'])} rows={len(tbl['rows'])} ===")
            for row in tbl["rows"][:8]:
                print(repr(row))

        await browser.close()

asyncio.run(debug())
