f = open("WissamXpoHub_V3_Frontend_FIXED.html", encoding="utf-8")
html = f.read()
f.close()

# Increase timeout from 180000 to 480000 (8 minutes)
html = html.replace("TIMEOUT=180000", "TIMEOUT=480000")
html = html.replace("const TIMEOUT = 180000", "const TIMEOUT = 480000")
html = html.replace("timeout=180000", "timeout=480000")
html = html.replace("timeout: 180000", "timeout: 480000")
html = html.replace("Request timeout (180s)", "Request timeout (480s)")

# Also fix fetchWithTimeout if exists
html = html.replace("}, 180000)", "}, 480000)")
html = html.replace("180 ثانية", "480 ثانية")

open("WissamXpoHub_V3_Frontend_FIXED.html", "w", encoding="utf-8").write(html)

# Check
import re
timeouts = re.findall(r'(?:TIMEOUT|timeout)[^\n]{0,30}', html)
for t in set(timeouts):
    print(t.strip())
print("Done")
