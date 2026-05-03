"""
deepsearch_service.py
OpenAI Responses API with web_search_preview tool.
Fetches recent 2024-2025 market data not in Comtrade yet.
"""
import os, json, logging
from dotenv import load_dotenv
load_dotenv()
logger = logging.getLogger(__name__)

OPENAI_KEY = os.getenv("OPENAI_API_KEY","")

def deep_search(query: str, max_results: int = 5) -> str:
    """Search the web for recent trade/market data using OpenAI."""
    if not OPENAI_KEY or OPENAI_KEY == "sk-your-key-here":
        return "[DeepSearch unavailable: no OPENAI_API_KEY]"
    try:
        import urllib.request, urllib.parse
        payload = json.dumps({
            "model": "gpt-4o-mini",
            "tools": [{"type": "web_search_preview"}],
            "input": query,
            "max_output_tokens": 1500
        }).encode("utf-8")
        req = urllib.request.Request(
            "https://api.openai.com/v1/responses",
            data=payload,
            headers={
                "Authorization": f"Bearer {OPENAI_KEY}",
                "Content-Type": "application/json"
            }
        )
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.loads(r.read().decode("utf-8"))
            # Extract text from response
            output = data.get("output", [])
            texts = []
            for item in output:
                if item.get("type") == "message":
                    for c in item.get("content", []):
                        if c.get("type") == "output_text":
                            texts.append(c.get("text",""))
            return "\n".join(texts) if texts else "[No results]"
    except Exception as e:
        logger.error(f"DeepSearch error: {e}")
        return f"[DeepSearch error: {e}]"

def get_market_intelligence(product: str, hs_code: str, country: str) -> str:
    """Get recent 2024-2025 market data for a product+country."""
    queries = [
        f"{product} import market {country} 2024 2025 statistics price trends",
        f"Egypt {product} export {country} {hs_code} 2024 news",
        f"{product} {country} importers buyers market outlook 2025",
    ]
    results = []
    for q in queries[:2]:  # Limit to 2 searches to save cost
        result = deep_search(q)
        if result and "unavailable" not in result and "error" not in result.lower():
            results.append(f"Search: {q}\nResult: {result[:800]}")
    if not results:
        return "[No recent web data found]"
    lines = [
        "╔══════════════════════════════════════════════════════╗",
        "║  RECENT WEB DATA (OpenAI DeepSearch 2024-2025)      ║",
        "║  Source: Live web search — not official statistics  ║",
        "╚══════════════════════════════════════════════════════╝",
        "",
    ]
    lines.extend(results)
    lines += [
        "",
        "⚠️ Web data is indicative. Cross-check with official sources.",
        "══════════════════════════════════════════════════════",
    ]
    return "\n".join(lines)
