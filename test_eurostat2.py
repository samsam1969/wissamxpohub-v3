import urllib.request, json, urllib.parse

# Test correct Eurostat endpoints
tests = [
    # Test 1: Comext via SDMX
    "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/DS-018995?startPeriod=2022&endPeriod=2024",
    # Test 2: Statistics endpoint
    "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/DS-018995?startPeriod=2022&endPeriod=2024&geo=NL&product=08111000",
    # Test 3: Different format
    "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/ext_lt_maineu?geo=NL&time=2023",
    # Test 4: Comext JSON API
    "https://ec.europa.eu/eurostat/wdds/rest/data/v2.1/json/en/DS-018995?product=08111000&reporter=NL&period=2022",
]

for i, url in enumerate(tests):
    print(f"\nTest {i+1}: {url[:80]}")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=10) as r:
            print(f"  Status: {r.status}")
            raw = r.read().decode("utf-8")[:300]
            print(f"  Response: {raw}")
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:200]
        print(f"  Error {e.code}: {body}")
    except Exception as e:
        print(f"  Error: {e}")
