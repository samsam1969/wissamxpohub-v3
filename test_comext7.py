import urllib.request, json

tests = [
    # DS-059341 with HS6
    "https://ec.europa.eu/eurostat/api/comext/dissemination/sdmx/2.1/data/DS-059341/A.NL.EG.081110.1.0/?startperiod=2022&endperiod=2024&format=JSON",
    # Try all FLOW
    "https://ec.europa.eu/eurostat/api/comext/dissemination/sdmx/2.1/data/DS-059341/A.NL.EG.081110.?.?/?startperiod=2023&endperiod=2024&format=JSON",
    # statistics endpoint
    "https://ec.europa.eu/eurostat/api/comext/dissemination/statistics/1.0/data/DS-059341?format=JSON&REPORTER=NL&PARTNER=EG&PRODUCT=081110&FLOW=1&STAT_PROCEDURE=0&PERIOD=2022,2023,2024",
    # HS4 level
    "https://ec.europa.eu/eurostat/api/comext/dissemination/sdmx/2.1/data/DS-059341/A.NL.EG.0811.1.0/?startperiod=2022&endperiod=2024&format=JSON",
]

for i, url in enumerate(tests):
    print(f"\nTest {i+1}: {url[60:130]}")
    try:
        req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0","Accept":"application/json"})
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read())
            print(f"  ✅ OK! size={data.get('size')} vals={str(data.get('value',{}))[:200]}")
    except urllib.error.HTTPError as e:
        print(f"  Error {e.code}: {e.read().decode()[:150]}")
    except Exception as e:
        print(f"  Error: {e}")
