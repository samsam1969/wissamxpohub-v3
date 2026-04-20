import urllib.request
url = "http://localhost:4000/ExportIntelligence.html"
try:
    r = urllib.request.urlopen(url)
    print("Already exists:", r.status)
except:
    print("Need to create")
