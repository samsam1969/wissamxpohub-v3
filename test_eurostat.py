import urllib.request, json, urllib.parse

# Eurostat Comext - EU trade statistics
# Dataset: DS-018995 (EU imports/exports by product and partner)
# HS 081110 = 08111000 in CN8

# Test 1: Netherlands imports of frozen strawberries from Egypt
params = {
    "product": "08111000",
    "reporter": "NL",
    "partner": "EG",
    "time": "2022,2023,2024",
}
url = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/DS-018995?" + urllib.parse.urlencode(params)
print("URL:", url[:100])
try:
    req = urllib.request.Request(url, headers={"User-Agent":"WissamXpoHub/1.0"})
    with urllib.request.urlopen(req, timeout=15) as r:
        data = json.loads(r.read())
        print("OK - keys:", list(data.keys())[:5])
        print("Dims:", list(data.get("dimension",{}).keys()))
        print("Values sample:", str(data.get("value",{}))[:200])
except Exception as e:
    print(f"Error: {e}")

# Test 2: Try different dataset
url2 = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/DS-645593?freq=A&reporter=NL&partner=EG&product=08111000&time=2023,2024"
print("\nURL2:", url2[:100])
try:
    req2 = urllib.request.Request(url2, headers={"User-Agent":"WissamXpoHub/1.0"})
    with urllib.request.urlopen(req2, timeout=15) as r:
        data2 = json.loads(r.read())
        print("OK2 - keys:", list(data2.keys())[:5])
except Exception as e:
    print(f"Error2: {e}")
