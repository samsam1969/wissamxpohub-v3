import os, requests

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
TAVILY_URL = "https://api.tavily.com/search"

def search_trade_data(query: str, max_results: int = 5) -> dict:
    try:
        res = requests.post(TAVILY_URL, json={
            "api_key": TAVILY_API_KEY,
            "query": query,
            "search_depth": "advanced",
            "max_results": max_results,
            "include_answer": True,
            "include_domains": [
                "trademap.org", "comtrade.un.org",
                "worldbank.org", "access2markets.ec.europa.eu",
                "cbi.eu", "eurostat.ec.europa.eu",
                "intracen.org", "unctad.org"
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
        return {"answer": "", "results": [], "error": str(e)}

def get_shipping_rates(product: str, origin: str, destination: str) -> dict:
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
        return {"answer": "", "results": [], "error": str(e)}

def get_market_prices(product: str, hs_code: str, market: str) -> dict:
    query = f"{product} HS {hs_code} import price {market} 2024 2025 market data USD"
    return search_trade_data(query, max_results=5)

def get_trade_trends(product: str, hs_code: str, market: str) -> dict:
    query = f"{product} HS {hs_code} exports {market} trade statistics 2024 2025"
    return search_trade_data(query, max_results=5)
