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

SKIP_DOMAINS = {
    "cloudflare.com","facebook.com","linkedin.com","twitter.com","instagram.com",
    "google.com","microsoft.com","hubspot.com","cookie-script.com","visable.com",
    "europages.com","europages.co.uk","bme.de","privacy.microsoft.com",
    "youtube.com","pinterest.com","xing.com","apple.com","amazon.com"
}

def clean(val):
    return re.sub(r'\s+', ' ', val).strip() if val else ""

def extract_from_json_ld(content):
    """Extract company data from JSON-LD structured data"""
    data = {}
    # URL/website
    url_match = re.search(r'"url"\s*:\s*"(https?://(?!www\.europages)[^"]+)"', content)
    if url_match:
        domain = url_match.group(1).replace("https://","").replace("http://","").split("/")[0]
        if domain and "." in domain and domain not in SKIP_DOMAINS:
            data["website"] = domain

    # Phone from JSON-LD
    phone_match = re.search(r'"telephone"\s*:\s*"([^"]+)"', content)
    if phone_match:
        data["phone"] = phone_match.group(1)

    # Email from JSON-LD
    email_match = re.search(r'"email"\s*:\s*"([^"]+@[^"]+)"', content)
    if email_match:
        data["email"] = email_match.group(1)

    # Address
    city_match = re.search(r'"addressLocality"\s*:\s*"([^"]+)"', content)
    if city_match:
        data["city"] = city_match.group(1)

    return data

async def test_profile_scraping():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(LP_WS)
        ctx = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await ctx.new_page()

        # Login
        await page.goto("https://www.europages.co.uk/en/login", timeout=30000, wait_until="domcontentloaded")
        await page.wait_for_timeout(2000)
        await page.evaluate(FILL_JS, {"email": EMAIL, "pass": EP_PASS})
        await page.evaluate("()=>{const b=document.querySelector(\"button[type='submit']\");if(b)b.click();}")
        await page.wait_for_timeout(5000)
        await page.wait_for_load_state("networkidle")
        await page.wait_for_timeout(1000)
        print("Logged in:", "login" not in page.url)

        # Get search results
        try:
            await page.goto("https://www.europages.co.uk/companies/germany/frozen-strawberries.html",
                          timeout=30000, wait_until="domcontentloaded")
        except:
            await page.wait_for_timeout(3000)

        content = await page.content()

        # Extract unique company profile links
        profiles = list(dict.fromkeys(
            re.findall(r'/en/company/([a-z0-9-]+-\d+)(?=/|")', content)
        ))
        print(f"Profiles found: {len(profiles)}")

        # Also extract names from JSON-LD
        companies_data = re.findall(
            r'"name"\s*:\s*"([^"]{3,60})".*?"url"\s*:\s*"(https://www\.europages\.co\.uk/en/firma/[^"]+)"',
            content[:50000]
        )
        print(f"JSON-LD companies: {len(companies_data)}")

        # Visit first 3 profiles to extract contact info
        results = []
        for slug in profiles[:3]:
            profile_url = f"https://www.europages.co.uk/en/company/{slug}"
            print(f"\nVisiting: {profile_url}")
            try:
                await page.goto(profile_url, timeout=25000, wait_until="domcontentloaded")
                await page.wait_for_timeout(2000)
                profile_content = await page.content()

                data = extract_from_json_ld(profile_content)
                print(f"  Website: {data.get('website','')}")
                print(f"  Phone:   {data.get('phone','')}")
                print(f"  Email:   {data.get('email','')}")
                print(f"  City:    {data.get('city','')}")

                # Also try visible phone numbers
                phones = re.findall(r'\+[\d\s\-]{8,18}|\(?\d{3,5}\)?[\s\-]?\d{3,5}[\s\-]?\d{3,5}', profile_content)
                if phones and not data.get("phone"):
                    print(f"  Phones (regex): {phones[:2]}")

                results.append({"slug": slug, **data})
            except Exception as e:
                print(f"  Error: {str(e)[:80]}")

        print(f"\nTotal results: {len(results)}")
        await browser.close()
        return results

asyncio.run(test_profile_scraping())
