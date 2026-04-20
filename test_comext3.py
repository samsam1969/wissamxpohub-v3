import urllib.request, json, time

# Tests with correct Eurostat country codes
# NL=NL, EG=EG are text codes - Eurostat uses ISO2
# Also need FLOW=1 (imports) and correct STAT_PROCEDURE

tests = [
    # Annual + all filters
    "https://ec.europa.eu/eurostat/api/comext/dissemination/statistics/1.0/data/ds-045409?format=JSON&REPORTER=NL&PARTNER=EG&PRODUCT=08111000&FLOW=1&STAT_PROCEDURE=0&PERIOD=2023",
    "https://ec.europa.eu/eurostat/api/comext/dissemination/statistics/1.0/data/ds-045409?format=JSON&REPORTER=NL&PARTNER=EG&PRODUCT=08111000&FLOW=1&STAT_PROCEDURE=0&PERIOD=2024",
    # Egypt exports to Netherlands
    "https://ec.europa.eu/eurostat/api/comext/dissemination/statistics/1.0/data/ds-045409?format=JSON&REPORTER=EG&PARTNER=NL&PRODUCT=08111000&FLOW=2&STAT_PROCEDURE=0&PERIOD=2023",
]

for i, url in enumerate(tests):
    print(f"\nTest {i+1}:")
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0","Accept":"application/json"})
            with urllib.request.urlopen(req, timeout=20) as r:
                data = json.loads(r.read())
                print(f"  OK! size={data.get('size')}")
                print(f"  dims={list(data.get('dimension',{}).keys())}")
                vals = data.get('value',{})
                print(f"  values={str(vals)[:300]}")
                # Show dimension labels
                for dim, dd in data.get("dimension",{}).items():
                    cats = dd.get("category",{}).get("label",{})
                    print(f"    {dim}: {list(cats.items())[:3]}")
                break
        except urllib.error.HTTPError as e:
            body = e.read().decode()[:150]
            print(f"  Attempt {attempt+1} - Error {e.code}: {body[:100]}")
            if "ASYNCHRONOUS" in body:
                print("  Waiting 5s then retry...")
                time.sleep(5)
            else:
                break
        except Exception as e:
            print(f"  Error: {e}"); break
