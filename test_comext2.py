import urllib.request, json, urllib.parse

# Reduce extraction by adding more filters
tests = [
    # Annual data only + specific period
    "https://ec.europa.eu/eurostat/api/comext/dissemination/statistics/1.0/data/ds-045409?format=JSON&REPORTER=NL&PARTNER=EG&PRODUCT=08111000&FLOW=1&PERIOD=2022,2023,2024&STAT_PROCEDURE=0&freq=A",
    # Try with PERIOD as range
    "https://ec.europa.eu/eurostat/api/comext/dissemination/statistics/1.0/data/ds-045409?format=JSON&REPORTER=NL&PARTNER=EG&PRODUCT=08111000&FLOW=1&STAT_PROCEDURE=0&startPeriod=2022&endPeriod=2024",
    # Minimal filters - just reporter+partner+product
    "https://ec.europa.eu/eurostat/api/comext/dissemination/statistics/1.0/data/ds-045409?format=JSON&REPORTER=528&PARTNER=818&PRODUCT=08111000&FLOW=1&STAT_PROCEDURE=0&PERIOD=2023",
    # Try with EGY code
    "https://ec.europa.eu/eurostat/api/comext/dissemination/statistics/1.0/data/ds-045409?format=JSON&REPORTER=528&PARTNER=EG&PRODUCT=08111000&FLOW=1&STAT_PROCEDURE=0&PERIOD=2023",
]

for i, url in enumerate(tests):
    print(f"\nTest {i+1}: {url[80:130]}")
    try:
        req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0","Accept":"application/json"})
        with urllib.request.urlopen(req, timeout=15) as r:
            raw = r.read().decode()
            data = json.loads(raw)
            print(f"  OK! size={data.get('size')} vals={str(data.get('value',{}))[:300]}")
            print(f"  dims={list(data.get('dimension',{}).keys())}")
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:200]
        print(f"  Error {e.code}: {body}")
    except Exception as e:
        print(f"  Error: {e}")
