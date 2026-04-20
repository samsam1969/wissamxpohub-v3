"""
lightpanda_service.py - Production v2
Real buyer scraping from Europages with phone + website extraction
"""
import asyncio, os, re, logging, hashlib
from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv()

logger = logging.getLogger(__name__)

LP_TOKEN = os.getenv("LIGHTPANDA_TOKEN", "")
LP_WS    = f"wss://cloud.lightpanda.io/ws?token={LP_TOKEN}"
EMAIL    = os.getenv("B2B_EMAIL", "")
EP_PASS  = os.getenv("EUROPAGES_PASSWORD", "")

_cache: dict = {}
CACHE_TTL = 12

def _cache_key(p, c): return hashlib.md5(f"{p}:{c}".lower().encode()).hexdigest()
def _get_cache(k):
    e=_cache.get(k)
    return e["data"] if e and datetime.utcnow()<e["expires"] else None
def _set_cache(k,d):
    _cache[k]={"data":d,"expires":datetime.utcnow()+timedelta(hours=CACHE_TTL)}

FILL_JS = """(c) => {
    const niv=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value');
    const e=document.querySelector("input[name='identifier'],input[type='email']");
    const p=document.querySelector("input[type='password']");
    if(!e||!p)return false;
    niv.set.call(e,c.email);e.dispatchEvent(new Event('input',{bubbles:true}));
    niv.set.call(p,c.pass);p.dispatchEvent(new Event('input',{bubbles:true}));
    return true;
}"""

SKIP = {"cloudflare.com","facebook.com","linkedin.com","twitter.com","instagram.com",
        "google.com","microsoft.com","hubspot.com","cookie-script.com","visable.com",
        "media.visable.com","europages.com","europages.co.uk","bme.de","xing.com",
        "youtube.com","apple.com","amazon.com","w3.org","schema.org","wlw.de"}

def clean(t): return re.sub(r'\s+',' ',t).strip() if t else ""
def valid_name(n):
    if not n or len(n)<3: return False
    skip={"login","register","home","back","next","page","search","filter","more","all"}
    if n.lower() in skip: return False
    return bool(re.match(r'^[A-Za-zÀ-ÿ]',n))

def extract_profile_data(content):
    data={"website":"","phone":"","email":""}
    pm=re.search(r'"telephone"\s*:\s*"([+\d\s\-\(\)]{7,20})"',content)
    if pm: data["phone"]=pm.group(1).strip()
    for pat in [
        r'"sameAs"\s*:\s*\["(https?://(?!www\.europages)(?!media\.visable)([^"]+))"',
        r'"sameAs"\s*:\s*"(https?://(?!www\.europages)(?!media\.visable)([^"]+))"',
    ]:
        m=re.search(pat,content)
        if m:
            url=m.group(1)
            domain=url.replace("https://","").replace("http://","").split("/")[0]
            if domain and "." in domain and domain not in SKIP and len(domain)>4:
                data["website"]=domain
                break
    em=re.search(r'"email"\s*:\s*"([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})"',content)
    if em: data["email"]=em.group(1)
    return data

async def scrape_europages(product, country, enrich=True):
    if not LP_TOKEN or not EP_PASS: return []
    buyers=[]
    try:
        from playwright.async_api import async_playwright
        async with async_playwright() as p:
            browser=await p.chromium.connect_over_cdp(LP_WS)
            ctx=await browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            page=await ctx.new_page()
            # Login
            await page.goto("https://www.europages.co.uk/en/login",timeout=30000,wait_until="domcontentloaded")
            await page.wait_for_timeout(2000)
            await page.evaluate(FILL_JS,{"email":EMAIL,"pass":EP_PASS})
            await page.evaluate("()=>{const b=document.querySelector(\"button[type='submit']\");if(b)b.click();}")
            await page.wait_for_timeout(5000)
            await page.wait_for_load_state("networkidle")
            await page.wait_for_timeout(1000)
            if "login" in page.url.lower():
                logger.warning("EP login failed")
                await browser.close()
                return []
            # Search
            q=product.lower().replace(" ","-")
            c=country.lower().replace(" ","-")
            url=f"https://www.europages.co.uk/companies/{c}/{q}.html"
            try:
                await page.goto(url,timeout=30000,wait_until="domcontentloaded")
            except: pass
            await page.wait_for_timeout(2000)
            content=await page.content()
            raw_names=re.findall(r'<h[23][^>]*>([^<]{4,80})</h[23]>',content)
            slugs=list(dict.fromkeys(re.findall(r'/en/company/([a-z0-9-]+-\d+)(?=/|")',content)))
            logger.info(f"EP: {len(raw_names)} names, {len(slugs)} slugs")
            for i,raw in enumerate(raw_names[:20]):
                name=clean(raw.replace("&amp;","&").replace("&#39;","'").strip())
                if not valid_name(name): continue
                slug=slugs[i] if i<len(slugs) else ""
                buyers.append({
                    "name":name,"country":country,
                    "source":"Europages",
                    "source_link":f"https://www.europages.co.uk/en/company/{slug}" if slug else url,
                    "website":"","email":"","phone":"","_slug":slug
                })
            # Enrich top 8
            if enrich:
                for b in buyers[:8]:
                    slug=b.pop("_slug","")
                    if not slug: continue
                    try:
                        await page.goto(f"https://www.europages.co.uk/en/company/{slug}",timeout=20000,wait_until="domcontentloaded")
                        await page.wait_for_timeout(1500)
                        d=extract_profile_data(await page.content())
                        b.update({"phone":d["phone"],"website":d["website"],"email":d["email"]})
                        logger.info(f"  {b['name']}: ph={b['phone']} web={b['website']}")
                    except Exception as e:
                        logger.warning(f"Profile {slug}: {e}")
                        b.pop("_slug",None)
                for b in buyers[8:]:
                    b.pop("_slug",None)
            else:
                for b in buyers: b.pop("_slug",None)
            await browser.close()
            logger.info(f"EP done: {len(buyers)}")
    except Exception as e:
        logger.error(f"EP error: {e}")
    return buyers

def score_buyer(b):
    s=30
    s+={"Europages":25,"WLW":20}.get(b.get("source",""),10)
    if b.get("website"): s+=20
    if b.get("phone"):   s+=15
    if b.get("email"):   s+=15
    return min(s,100)

def deduplicate(buyers):
    seen=set(); result=[]
    for b in buyers:
        k=re.sub(r'\b(gmbh|bv|srl|sa|nv|ltd|llc|inc|ag|kg)\b','',b["name"].lower()).strip()
        if k not in seen: seen.add(k); result.append(b)
    return result

def search_buyers_live(product, hs_code, country):
    if not LP_TOKEN:
        return {"buyers":[],"error":"LIGHTPANDA_TOKEN not set","sources_used":[]}
    key=_cache_key(product,country)
    cached=_get_cache(key)
    if cached: return {"buyers":cached,"sources_used":["cache"],"error":None}
    try:
        loop=asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        buyers=loop.run_until_complete(scrape_europages(product,country,enrich=True))
        loop.close()
        buyers=deduplicate(buyers)
        for b in buyers: b["score"]=score_buyer(b)
        buyers.sort(key=lambda x:x.get("score",0),reverse=True)
        _set_cache(key,buyers)
        return {"buyers":buyers,"sources_used":["Europages"],"error":None}
    except Exception as e:
        logger.error(f"live error: {e}")
        return {"buyers":[],"sources_used":[],"error":str(e)}
