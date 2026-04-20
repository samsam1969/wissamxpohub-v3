import urllib.request, json

# First get the datastructure to know correct dimension values
url = "https://ec.europa.eu/eurostat/api/comext/dissemination/sdmx/2.1/datastructure/ESTAT/DSD_DS-045409?format=JSON"
print("Getting structure...")
try:
    req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as r:
        data = json.loads(r.read())
        print("OK! Keys:", list(data.keys()))
        print(str(data)[:1000])
except Exception as e:
    print(f"Error: {e}")

# Also try dataflow list
url2 = "https://ec.europa.eu/eurostat/api/comext/dissemination/sdmx/2.1/dataflow/ESTAT/all?format=JSON"
print("\nGetting dataflows...")
try:
    req2 = urllib.request.Request(url2, headers={"User-Agent":"Mozilla/5.0"})
    with urllib.request.urlopen(req2, timeout=15) as r:
        raw = r.read().decode()[:2000]
        print("OK:", raw[:500])
except Exception as e:
    print(f"Error: {e}")

# Try correct key format - check error message details
url3 = "https://ec.europa.eu/eurostat/api/comext/dissemination/sdmx/2.1/data/DS-045409/A.NL.EG.08111000.1.0/?startperiod=2022&endperiod=2024&format=JSON"
try:
    req3 = urllib.request.Request(url3, headers={"User-Agent":"Mozilla/5.0"})
    with urllib.request.urlopen(req3, timeout=15) as r:
        print(r.read().decode()[:300])
except urllib.error.HTTPError as e:
    # Show full error
    print("Full error:", e.read().decode()[:500])
