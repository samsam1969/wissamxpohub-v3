from google import genai
import os

_client = None

def get_client():
    global _client
    if _client is None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not set")
        _client = genai.Client(api_key=api_key)
    return _client

FLASH = "gemini-2.0-flash"

def gemini_prepare_data(raw_data: dict) -> str:
    """يلخّص البيانات الخام قبل Claude - أسرع وأرخص"""
    try:
        client = get_client()
        prompt = f"""You are a trade data analyst assistant.
Organize and summarize this raw trade data into clear structured bullet points.
Focus ONLY on: key numbers, trade volumes, price trends, top markets, growth %.
Be concise, factual, no opinions. Max 300 words.

Raw data:
{str(raw_data)[:8000]}
"""
        response = client.models.generate_content(model=FLASH, contents=prompt)
        return response.text or ""
    except Exception as e:
        print(f"[Gemini] prepare_data error: {e}")
        return ""

def gemini_extract_market_info(product: str, market: str, raw_text: str) -> str:
    """يستخرج معلومات تجارية محددة من نص خام"""
    try:
        client = get_client()
        prompt = f"""Extract key trade information for exporting '{product}' to '{market}'.
From this text extract:
1. Import volumes or demand data
2. Price ranges (FOB/CIF)
3. Main competing countries
4. Key regulations or certifications needed
5. Growth trend (up/down/stable)

Text: {raw_text[:5000]}

Reply in structured bullet points only. Be brief."""
        response = client.models.generate_content(model=FLASH, contents=prompt)
        return response.text or ""
    except Exception as e:
        print(f"[Gemini] extract error: {e}")
        return ""

def gemini_quick_snapshot(product: str, market: str) -> str:
    """سنابشوت سريع لأي منتج/سوق للاستعلامات البسيطة"""
    try:
        client = get_client()
        prompt = f"""Quick export intelligence snapshot:
Product: {product}
Target Market: {market}

Provide:
- Demand level: High/Medium/Low
- Price range: USD/ton estimate
- Top 3 competing countries
- 2 key certifications needed
- Opportunity score: X/10 + one-line reason

Be brief and factual."""
        response = client.models.generate_content(model=FLASH, contents=prompt)
        return response.text or ""
    except Exception as e:
        print(f"[Gemini] snapshot error: {e}")
        return ""

def test_gemini() -> str:
    """اختبار الاتصال"""
    try:
        client = get_client()
        response = client.models.generate_content(
            model=FLASH,
            contents="Reply exactly: Gemini connected to WissamXpoHub V3 OK"
        )
        return f"✅ {response.text}"
    except Exception as e:
        return f"❌ {e}"
