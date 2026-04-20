import os, sys
sys.path.insert(0, '.')
from dotenv import load_dotenv
load_dotenv()
from services.tavily_service import get_shipping_rates, get_market_prices

print("=== TEST 1: Shipping Rates ===")
r = get_shipping_rates("dates", "Port Said Egypt", "Helsinki Finland")
print("Answer:", r.get("answer", "")[:200])
print("Results:", len(r.get("results", [])))

print("\n=== TEST 2: Market Prices ===")
r2 = get_market_prices("dates", "080410", "Finland")
print("Answer:", r2.get("answer", "")[:200])
print("Results:", len(r2.get("results", [])))
