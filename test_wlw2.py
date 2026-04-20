import asyncio, os
from dotenv import load_dotenv
load_dotenv()

LP_TOKEN = os.getenv("LIGHTPANDA_TOKEN","")
LP_WS = f"wss://cloud.lightpanda.io/ws?token={LP_TOKEN}"
EMAIL = os.getenv("B2B_EMAIL","")
WLW_PASS = os.getenv("WLW_PASSWORD","")

print("Email:", EMAIL)
print("WLW Pass length:", len(WLW_PASS))

FILL_JS = """(c) => {
    const niv=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value');
    const e=document.querySelector("input[name='identifier'],input[type='email']");
    const p=document.querySelector("input[type='password']");
    if(!e||!p)return {ok:false,msg:"fields not found"};
    niv.set.call(e,c.email);e.dispatchEvent(new Event('input',{bubbles:true}));
    niv.set.call(p,c.pass);p.dispatchEvent(new Event('input',{bubbles:true}));
    return {ok:true,eLen:e.value.length,pLen:p.value.length};
}"""

async def test():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(LP_WS)
        ctx = await browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        page = await ctx.new_page()
        await page.goto("https://www.wlw.de/en/login", timeout=30000, wait_until="domcontentloaded")
        await page.wait_for_timeout(2000)
        print("Login page:", await page.title())
        result = await page.evaluate(FILL_JS, {"email": EMAIL, "pass": WLW_PASS})
        print("Fill:", result)
        await page.evaluate("()=>{const b=document.querySelector(\"button[type='submit']\");if(b)b.click();}")
        await page.wait_for_timeout(5000)
        print("After URL:", page.url)
        print("Logged in:", "login" not in page.url and "flow" not in page.url)
        await browser.close()

asyncio.run(test())
