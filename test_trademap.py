import asyncio, os, re
from dotenv import load_dotenv
load_dotenv()

LP_TOKEN = os.getenv("LIGHTPANDA_TOKEN","")
LP_WS = f"wss://cloud.lightpanda.io/ws?token={LP_TOKEN}"

async def test_trademap():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(LP_WS)
        ctx = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
        page = await ctx.new_page()

        # Test Trade Map without login first
        url = "https://www.trademap.org/Country_SelProductCountry_TS.aspx?nvpm=1%7c818%7c%7c%7c%7c081110%7c%7c%7c6%7c1%7c1%7c2%7c2%7c1%7c2%7c1%7c1%7c1"
        print(f"Loading: {url[:80]}...")
        try:
            await page.goto(url, timeout=25000, wait_until="domcontentloaded")
            await page.wait_for_timeout(3000)
            print("Title:", await page.title())
            print("URL:", page.url)
            content = await page.content()
            print("Size:", len(content))

            # Look for data tables
            tables = re.findall(r'<table[^>]*id="[^"]*"[^>]*>', content)
            print("Tables found:", len(tables))
            for t in tables[:5]:
                print(" ", t[:80])

            # Look for year data
            years = re.findall(r'\b(2023|2024|2025)\b', content)
            print("Years found:", set(years))

            # Look for numbers
            numbers = re.findall(r'\d{3,}', content[:5000])
            print("Numbers sample:", numbers[:10])

        except Exception as e:
            print(f"Error: {e}")
        finally:
            await browser.close()

asyncio.run(test_trademap())
