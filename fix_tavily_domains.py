content = open('services/tavily_service.py', encoding='utf-8').read()

old = '''            "include_domains": [
                "trademap.org", "comtrade.un.org",
                "freightos.com", "worldbank.org",
                "access2markets.ec.europa.eu",
                "cbi.eu", "eurostat.ec.europa.eu"
            ]'''

new = '''            "include_domains": [
                "trademap.org", "comtrade.un.org",
                "worldbank.org", "access2markets.ec.europa.eu",
                "cbi.eu", "eurostat.ec.europa.eu",
                "intracen.org", "unctad.org"
            ]'''

content = content.replace(old, new)

# Fix shipping domains separately
old2 = '''def get_shipping_rates(product: str, origin: str, destination: str) -> dict:
    query = f"shipping freight rates {product} {origin} to {destination} 2025 2026 USD per ton"
    return search_trade_data(query, max_results=3)'''

new2 = '''def get_shipping_rates(product: str, origin: str, destination: str) -> dict:
    query = f"sea freight cost refrigerated container {origin} to {destination} 2025 USD per container"
    try:
        import requests as req
        res = req.post("https://api.tavily.com/search", json={
            "api_key": TAVILY_API_KEY,
            "query": query,
            "search_depth": "advanced",
            "max_results": 3,
            "include_answer": True,
            "include_domains": [
                "freightos.com", "xeneta.com",
                "drewry.co.uk", "clarksons.com",
                "hapag-lloyd.com", "maersk.com",
                "ship-technology.com", "hellenicshippingnews.com"
            ]
        }, timeout=15)
        data = res.json()
        return {
            "answer": data.get("answer", ""),
            "results": [
                {
                    "title":   r.get("title", ""),
                    "url":     r.get("url", ""),
                    "content": r.get("content", "")[:500],
                    "score":   r.get("score", 0)
                }
                for r in data.get("results", [])
            ]
        }
    except Exception as e:
        return {"answer": "", "results": [], "error": str(e)}'''

content = content.replace(old2, new2)
open('services/tavily_service.py', 'w', encoding='utf-8').write(content)
print('Done - Tavily domains updated')
