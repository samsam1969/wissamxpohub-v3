import urllib.request, urllib.parse, json

# Test raw API call
params = {
    "flowCode": "M",
    "reporterCode": "724",
    "cmdCode": "080410",
    "period": "2022",
    "partnerCode": "ALL",
    "breakdownMode": "classic",
    "customsCode": "C00",
    "motCode": "0",
    "includeDesc": "true",
}
url = "https://comtradeapi.un.org/public/v1/preview/C/A/HS?" + urllib.parse.urlencode(params)
print("URL:", url)
try:
    req = urllib.request.Request(url, headers={"User-Agent":"test"})
    with urllib.request.urlopen(req, timeout=15) as r:
        data = json.loads(r.read())
        print("OK - records:", len(data.get("data",[])))
        print("Sample:", str(data)[:300])
except urllib.error.HTTPError as e:
    print(f"HTTP {e.code}: {e.read().decode()[:300]}")
