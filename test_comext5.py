import urllib.request, json

# Correct Comext SDMX format: /FREQ.REPORTER.PARTNER.PRODUCT.FLOW.STAT_PROCEDURE/
# A=Annual, NL=Netherlands, EG=Egypt, 08111000=CN8, 1=Import, 0=Normal

tests = [
    # Annual NL imports from EG
    "https://ec.europa.eu/eurostat/api/comext/dissemination/sdmx/2.1/data/DS-045409/A.NL.EG.08111000.1.0/?startperiod=2022&endperiod=2024&format=JSON",
    # Monthly
    "https://ec.europa.eu/eurostat/api/comext/dissemination/sdmx/2.1/data/DS-045409/M.NL.EG.08111000.1.0/?startperiod=202201&endperiod=202412&format=JSON",
    # Different dataset DS-016890
    "https://ec.europa.eu/eurostat/api/comext/dissemination/sdmx/2.1/data/DS-016890/A.NL.EG.08111000.1.0/?startperiod=2022&endperiod=2024&format=JSON",
    # Try DS-059322
    "https://ec.europa.eu/eurostat/api/comext/dissemination/sdmx/2.1/data/DS-059322/A.NL.EG.08111000.1.0/?startperiod=2022&endperiod=2024&format=JSON",
]

for i, url in enumerate(tests):
    print(f"\nTest {i+1}: {url[60:120]}")
    try:
        req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0","Accept":"application/json"})
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read())
            print(f"  OK! size={data.get('size')}")
            print(f"  values={str(data.get('value',{}))[:300]}")
            print(f"  dims={list(data.get('dimension',{}).keys())}")
    except urllib.error.HTTPError as e:
        print(f"  Error {e.code}: {e.read().decode()[:150]}")
    except Exception as e:
        print(f"  Error: {e}")
