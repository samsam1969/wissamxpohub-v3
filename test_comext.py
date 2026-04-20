import urllib.request, json, urllib.parse

# CORRECT endpoint: comext/dissemination (not dissemination)
# Dataset: ds-045409 = Extra-EU trade

# Test with comext prefix
tests = [
    # Basic test
    "https://ec.europa.eu/eurostat/api/comext/dissemination/statistics/1.0/data/ds-045409?format=JSON&REPORTER=NL&PARTNER=EG&PRODUCT=08111000&FLOW=1&PERIOD=2022,2023,2024&STAT_PROCEDURE=0",
    # Try ds-059322
    "https://ec.europa.eu/eurostat/api/comext/dissemination/statistics/1.0/data/ds-059322?format=JSON&REPORTER=NL&PARTNER=EG&PRODUCT=08111000&FLOW=1&PERIOD=2023",
    # Try DS-018995 with comext
    "https://ec.europa.eu/eurostat/api/comext/dissemination/statistics/1.0/data/DS-018995?format=JSON&REPORTER=NL&PARTNER=EG&PRODUCT=08111000&FLOW=1&PERIOD=2023",
]

for i, url in enumerate(tests):
    print(f"\nTest {i+1}: {url[:100]}")
    try:
        req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0","Accept":"application/json"})
        with urllib.request.urlopen(req, timeout=15) as r:
            raw = r.read().decode()
            data = json.loads(raw)
            print(f"  OK! Keys: {list(data.keys())[:6]}")
            print(f"  Size: {data.get('size')}")
            print(f"  Values: {str(data.get('value',{}))[:200]}")
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:200]
        print(f"  Error {e.code}: {body}")
    except Exception as e:
        print(f"  Error: {e}")
