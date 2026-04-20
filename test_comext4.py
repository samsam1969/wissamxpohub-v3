import asyncio, os, re
from dotenv import load_dotenv
load_dotenv()

LP_TOKEN = os.getenv("LIGHTPANDA_TOKEN","")
LP_WS = f"wss://cloud.lightpanda.io/ws?token={LP_TOKEN}"

async def test():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(LP_WS)
        ctx = await browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        page = await ctx.new_page()

        # Easy Comext - direct data URL for NL imports from EG of 08111000
        url = "https://ec.europa.eu/eurostat/comext/newxtweb/submitrequest.do?PRODUCT=08111000&REPORTER=NL&PARTNER=EG&FLOW=1&PERIOD=2020-2024&INDICATORS=VALUE_IN_EUROS,QUANTITY_IN_100KG&FORMAT=HTML"
        print("Testing Easy Comext...")
        try:
            await page.goto(url, timeout=20000, wait_until="domcontentloaded")
            await page.wait_for_timeout(2000)
            print("Title:", await page.title())
            print("URL:", page.url)
            content = await page.content()
            print("Size:", len(content))
            # Look for years
            years = re.findall(r'\b(202[0-9])\b', content)
            print("Years:", set(years))
            # Look for numbers
            nums = re.findall(r'[\d,]{5,}', content[:3000])
            print("Numbers:", nums[:10])
        except Exception as e:
            print(f"Error: {e}")

        # Try Eurostat data browser direct
        url2 = "https://ec.europa.eu/eurostat/api/comext/dissemination/statistics/1.0/data/ds-045409?format=JSON&REPORTER=NL&PARTNER=EG&PRODUCT=08111000&FLOW=1&STAT_PROCEDURE=0&PERIOD=2023&INDICATORS=VALUE_IN_EUROS"
        print("\nTesting with INDICATORS filter...")
        import urllib.request, json
        try:
            req = urllib.request.Request(url2, headers={"User-Agent":"Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=15) as r:
                data = json.loads(r.read())
                print("OK! size:", data.get("size"))
                print("values:", str(data.get("value",""))[:200])
        except urllib.error.HTTPError as e:
            print(f"Error {e.code}:", e.read().decode()[:150])

        await browser.close()

asyncio.run(test())
