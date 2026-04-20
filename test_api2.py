import urllib.request, urllib.parse, json

# Test without partnerCode
params = {
    "flowCode": "M",
    "reporterCode": "724",
    "cmdCode": "080410",
    "period": "2022",
    "breakdownMode": "classic",
    "includeDesc": "true",
}
url = "https://comtradeapi.un.org/public/v1/preview/C/A/HS?" + urllib.parse.urlencode(params)
print("URL:", url)
try:
    req = urllib.request.Request(url, headers={"User-Agent":"test"})
    with urllib.request.urlopen(req, timeout=15) as r:
        data = json.loads(r.read())
        records = data.get("data",[])
        print("OK - records:", len(records))
        if records:
            print("Keys:", list(records[0].keys()))
            print("Sample:", records[0])
except urllib.error.HTTPError as e:
    body = e.read().decode()
    print(f"HTTP {e.code}: {body[:300]}")
