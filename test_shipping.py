import os, sys
sys.path.insert(0, '.')
from dotenv import load_dotenv
load_dotenv()
from services.tavily_service import get_shipping_rates

r = get_shipping_rates("dates", "Port Said Egypt", "Helsinki Finland")
print("Answer:", r.get("answer", "")[:300])
for res in r.get("results", []):
    print(f"- {res['title']}: {res['url']}")
