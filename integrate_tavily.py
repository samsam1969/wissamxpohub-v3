content = open('services/claude_service.py', encoding='utf-8').read()

old = '''    # -- Layer 2: OpenAI DeepSearch
    web_data = ""
    try:
        from services.deepsearch_service import get_market_intelligence
        if product and target_market:
            web_data = get_market_intelligence(product, hs_code or "", target_market)
    except Exception as e:
        web_data = ""'''

new = '''    # -- Layer 2: Tavily Web Intelligence (replaces OpenAI DeepSearch)
    web_data = ""
    tavily_sources = []
    try:
        from services.tavily_service import get_market_prices, get_trade_trends, get_shipping_rates
        if product and target_market:
            prices  = get_market_prices(product, hs_code or "", target_market)
            trends  = get_trade_trends(product, hs_code or "", target_market)
            shipping = get_shipping_rates(product, "Egypt", target_market)

            web_data = f"""
=== Tavily Web Intelligence (2024-2026) ===

[Market Prices 2024-2025]
{prices.get("answer", "")}

[Trade Trends 2024-2025]
{trends.get("answer", "")}

[Shipping Rates 2025-2026]
{shipping.get("answer", "")}
"""
            # Collect source URLs for citation
            for r in prices.get("results", []) + trends.get("results", []):
                if r.get("url") and r.get("score", 0) > 0.5:
                    tavily_sources.append({
                        "title": r.get("title", ""),
                        "url":   r.get("url", ""),
                        "score": r.get("score", 0)
                    })
    except Exception as e:
        web_data = f"[Tavily unavailable: {e}]"'''

content = content.replace(old, new)
open('services/claude_service.py', 'w', encoding='utf-8').write(content)
print('Done - Tavily integrated in Layer 2')
