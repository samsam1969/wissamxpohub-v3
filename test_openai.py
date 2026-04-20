import urllib.request, json, os
from dotenv import load_dotenv
load_dotenv()

key = os.getenv("OPENAI_API_KEY","")
print("Key prefix:", key[:20])

# Test basic API call first
payload = json.dumps({
    "model": "gpt-4o-mini",
    "messages": [{"role":"user","content":"say hello"}],
    "max_tokens": 10
}).encode()

req = urllib.request.Request(
    "https://api.openai.com/v1/chat/completions",
    data=payload,
    headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
)
try:
    with urllib.request.urlopen(req, timeout=15) as r:
        data = json.loads(r.read())
        print("API OK:", data["choices"][0]["message"]["content"])
except urllib.error.HTTPError as e:
    body = e.read().decode()
    print(f"Error {e.code}: {body[:300]}")
except Exception as e:
    print(f"Error: {e}")
