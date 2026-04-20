import urllib.request, json

url = "https://ec.europa.eu/eurostat/api/comext/dissemination/sdmx/2.1/datastructure/ESTAT/DS-059341?format=JSON"
try:
    req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as r:
        data = json.loads(r.read())
        print(str(data)[:3000])
except Exception as e:
    print(f"Error: {e}")

# Full error details
url2 = "https://ec.europa.eu/eurostat/api/comext/dissemination/sdmx/2.1/data/DS-059341/A.NL.EG.081110.1.0/?startperiod=2022&endperiod=2024&format=JSON"
try:
    req2 = urllib.request.Request(url2, headers={"User-Agent":"Mozilla/5.0"})
    with urllib.request.urlopen(req2, timeout=15) as r:
        print(r.read().decode()[:300])
except urllib.error.HTTPError as e:
    print("Full error:", e.read().decode())
