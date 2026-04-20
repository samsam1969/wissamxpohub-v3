import urllib.request, json, urllib.parse

# ext_lt_maineu works - explore it for frozen strawberries
# Also try DS-018995 alternative name

tests = [
    # Try Comext proper dataset name
    "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/DS-059322?startPeriod=2022&endPeriod=2024",
    # Try with HS product filter
    "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/ext_lt_introeu?startPeriod=2023&endPeriod=2024",
    # Comext via different path
    "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/DS-016890?startPeriod=2023",
    # Trade by CN - the correct one
    "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/DS-018995?sinceTimePeriod=2022",
]

for i, url in enumerate(tests):
    print(f"\nTest {i+1}: {url[:90]}")
    try:
        req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0","Accept":"application/json"})
        with urllib.request.urlopen(req, timeout=10) as r:
            raw = r.read().decode()[:400]
            print(f"  OK: {raw[:200]}")
    except urllib.error.HTTPError as e:
        print(f"  Error {e.code}: {e.read().decode()[:150]}")
    except Exception as e:
        print(f"  Error: {e}")

# Also check what dims ext_lt_maineu has
print("\n\nChecking ext_lt_maineu dimensions:")
url = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/ext_lt_maineu?geo=NL&time=2023,2024&partner=EG"
try:
    req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=10) as r:
        data = json.loads(r.read())
        print("Dims:", list(data.get("dimension",{}).keys()))
        print("Size:", data.get("size"))
        print("Values:", str(data.get("value",{}))[:300])
        # Show labels
        for dim,ddata in data.get("dimension",{}).items():
            cats = ddata.get("category",{}).get("label",{})
            print(f"  {dim}: {list(cats.items())[:5]}")
except Exception as e:
    print(f"Error: {e}")
