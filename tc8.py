import urllib.request, json

tests = [
    # Remove last dimension (INDICATORS)
    "https://ec.europa.eu/eurostat/api/comext/dissemination/sdmx/2.1/data/DS-059341/A.NL.EG.081110.1/?startperiod=2022&endperiod=2024&format=JSON",
    # Try with VALUE_IN_EUROS as INDICATORS
    "https://ec.europa.eu/eurostat/api/comext/dissemination/sdmx/2.1/data/DS-059341/A.NL.EG.081110.1.VALUE_IN_EUROS/?startperiod=2022&endperiod=2024&format=JSON",
    # Try ALL indicators
    "https://ec.europa.eu/eurostat/api/comext/dissemination/sdmx/2.1/data/DS-059341/A.NL.EG.081110.1.+/?startperiod=2023&endperiod=2024&format=JSON",
    # Statistics endpoint without STAT_PROCEDURE
    "https://ec.europa.eu/eurostat/api/comext/dissemination/statistics/1.0/data/DS-059341?format=JSON&REPORTER=NL&PARTNER=EG&PRODUCT=081110&FLOW=1&PERIOD=2022,2023,2024",
]

for i, url in enumerate(tests):
    print(f"\nTest {i+1}: ...{url[65:130]}")
    try:
        req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0","Accept":"application/json"})
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read())
            print(f"  ✅ size={data.get('size')} vals={str(data.get('value',{}))[:200]}")
            print(f"  dims={list(data.get('dimension',{}).keys())}")
    except urllib.error.HTTPError as e:
        print(f"  Error {e.code}: {e.read().decode()[:150]}")
    except Exception as e:
        print(f"  Error: {e}")
