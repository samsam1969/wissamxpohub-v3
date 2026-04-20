lines = open('services/claude_service.py', encoding='utf-8').readlines()

# Replace lines 338-345 (index 337-344) with Tavily layer
new_layer = '''    # -- Layer 2: Tavily Web Intelligence
    web_data = ""
    tavily_sources = []
    try:
        from services.tavily_service import get_market_prices, get_trade_trends, get_shipping_rates
        if product and target_market:
            prices   = get_market_prices(product, hs_code or "", target_market)
            trends   = get_trade_trends(product, hs_code or "", target_market)
            shipping = get_shipping_rates(product, "Egypt", target_market)
            web_data = f"""
=== Tavily Web Intelligence (2024-2026) ===
[Market Prices] {prices.get("answer", "")}
[Trade Trends]  {trends.get("answer", "")}
[Shipping]      {shipping.get("answer", "")}
"""
            for r in prices.get("results", []) + trends.get("results", []):
                if r.get("url") and r.get("score", 0) > 0.5:
                    tavily_sources.append({"name": r.get("title",""), "url": r.get("url",""), "type": "tavily"})
    except Exception as e:
        web_data = f"[Tavily unavailable: {e}]"
'''

lines[337:345] = [new_layer]
open('services/claude_service.py', 'w', encoding='utf-8').writelines(lines)
print('Done - Layer 2 replaced with Tavily')
