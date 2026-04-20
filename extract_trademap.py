import asyncio, os, re
from dotenv import load_dotenv
load_dotenv()

LP_TOKEN = os.getenv("LIGHTPANDA_TOKEN","")
LP_WS = f"wss://cloud.lightpanda.io/ws?token={LP_TOKEN}"

async def extract_trademap_data():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(LP_WS)
        ctx = await browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        page = await ctx.new_page()

        url = "https://www.trademap.org/Country_SelProductCountry_TS.aspx?nvpm=1%7c818%7c%7c%7c%7c081110%7c%7c%7c6%7c1%7c1%7c2%7c2%7c1%7c2%7c1%7c1%7c1"
        await page.goto(url, timeout=25000, wait_until="domcontentloaded")
        await page.wait_for_timeout(3000)

        # Extract main data table
        table_data = await page.evaluate("""() => {
            const table = document.querySelector('#ctl00_PageContent_GridLabelUnitTable')
                       || document.querySelector('table[id*="Grid"]')
                       || document.querySelectorAll('table')[1];
            if (!table) return {error: "no table"};

            const rows = [];
            table.querySelectorAll('tr').forEach(tr => {
                const cells = [];
                tr.querySelectorAll('td, th').forEach(td => {
                    cells.push(td.innerText.trim());
                });
                if (cells.length > 0) rows.push(cells);
            });
            return {rows: rows.slice(0, 30)};
        }""")

        print("Table data:")
        if table_data.get("rows"):
            for row in table_data["rows"][:15]:
                print(" | ".join(str(c) for c in row[:8]))
        else:
            print("Error:", table_data)

        # Also get raw HTML of main table
        content = await page.content()
        # Find the data table HTML
        table_match = re.search(
            r'<table[^>]*id="ctl00_PageContent_GridLabelUnitTable"[^>]*>(.*?)</table>',
            content, re.DOTALL
        )
        if not table_match:
            # Try second table
            tables = re.findall(r'<table[^>]*>(.*?)</table>', content, re.DOTALL)
            if len(tables) > 1:
                # Extract text from second table
                rows = re.findall(r'<tr[^>]*>(.*?)</tr>', tables[1], re.DOTALL)
                print(f"\nTable 2 rows: {len(rows)}")
                for row in rows[:8]:
                    cells = re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>', row, re.DOTALL)
                    clean = [re.sub(r'<[^>]+>', '', c).strip() for c in cells]
                    if any(clean):
                        print(" | ".join(clean[:8]))

        await browser.close()

asyncio.run(extract_trademap_data())
