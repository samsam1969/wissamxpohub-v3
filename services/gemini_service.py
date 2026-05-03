"""
Gemini Service - Direct REST API (no SDK, no dependency conflicts)
"""
import requests
import os

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

def _call_gemini(prompt: str, max_tokens: int = 1000) -> str:
    """Direct REST call to Gemini API"""
    if not GEMINI_API_KEY:
        return ""
    try:
        response = requests.post(
            f"{GEMINI_URL}?key={GEMINI_API_KEY}",
            json={
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"maxOutputTokens": max_tokens, "temperature": 0.3}
            },
            timeout=30
        )
        if response.status_code == 200:
            data = response.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
        else:
            print(f"[Gemini] API error {response.status_code}: {response.text[:200]}")
            return ""
    except Exception as e:
        print(f"[Gemini] Request error: {e}")
        return ""

def gemini_prepare_data(raw_data: dict) -> str:
    """يلخّص البيانات الخام قبل Claude - أسرع وأرخص"""
    prompt = f"""You are a trade data analyst assistant.
Organize and summarize this raw trade data into clear structured bullet points.
Focus ONLY on: key numbers, trade volumes, price trends, top markets, growth %.
Be concise, factual, no opinions. Max 300 words.

Raw data:
{str(raw_data)[:6000]}
"""
    return _call_gemini(prompt, max_tokens=600)

def gemini_extract_market_info(product: str, market: str, raw_text: str) -> str:
    """يستخرج معلومات تجارية محددة من نص خام"""
    prompt = f"""Extract key trade information for exporting '{product}' to '{market}'.
From this text extract:
1. Import volumes or demand data
2. Price ranges (FOB/CIF)
3. Main competing countries
4. Key regulations or certifications needed
5. Growth trend (up/down/stable)

Text: {raw_text[:4000]}
Reply in structured bullet points only. Be brief."""
    return _call_gemini(prompt, max_tokens=500)

def gemini_quick_snapshot(product: str, market: str) -> str:
    """سنابشوت سريع لأي منتج/سوق"""
    prompt = f"""Quick export intelligence snapshot:
Product: {product} | Target Market: {market}
Provide:
- Demand level: High/Medium/Low
- Price range: USD/ton estimate  
- Top 3 competing countries
- 2 key certifications needed
- Opportunity score: X/10 + one-line reason
Be brief and factual."""
    return _call_gemini(prompt, max_tokens=400)

def test_gemini() -> str:
    """اختبار الاتصال"""
    result = _call_gemini("Reply exactly: Gemini REST API connected to WissamXpoHub V3 OK")
    if result:
        return f"✅ {result.strip()}"
    return "❌ Connection failed - check API key or quota"
