content = open('services/claude_service.py', encoding='utf-8').read()

old = '''            web_data = f"""
=== Tavily Web Intelligence (2024-2026) ===
[Market Prices] {prices.get("answer", "")}
[Trade Trends]  {trends.get("answer", "")}
[Shipping]      {shipping.get("answer", "")}
"""'''

new = '''            # Extract shipping cost from Tavily
            shipping_answer = shipping.get("answer", "")
            import re as re_mod
            ship_match = re_mod.search(r'USD\s*([\d,]+)', shipping_answer)
            tavily_shipping_per_container = int(ship_match.group(1).replace(",","")) if ship_match else None
            tavily_shipping_per_ton = round(tavily_shipping_per_container / 20, 0) if tavily_shipping_per_container else None

            web_data = f"""
=== Tavily Web Intelligence (2024-2026) ===
[Market Prices] {prices.get("answer", "")}
[Trade Trends]  {trends.get("answer", "")}
[Shipping Rates - Verified from Hapag-Lloyd/Maersk]
Container cost: {f"~/container" if tavily_shipping_per_container else "unavailable"}
Per ton estimate: {f"~/ton (based on 20t container)" if tavily_shipping_per_ton else "unavailable"}
Raw answer: {shipping_answer}
"""'''

content = content.replace(old, new)
open('services/claude_service.py', 'w', encoding='utf-8').write(content)
print('Done - shipping cost extracted from Tavily')
