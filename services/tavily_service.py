import os, requests
from datetime import datetime

TAVILY_API_KEY = os.getenv('TAVILY_API_KEY')
TAVILY_URL = 'https://api.tavily.com/search'

def _tavily_search(query, domains=None, max_results=7, depth='advanced'):
    try:
        payload = {
            'api_key': TAVILY_API_KEY,
            'query': query,
            'search_depth': depth,
            'max_results': max_results,
            'include_answer': True,
        }
        # فقط نضيف domains لو صغيرة وموثوقة
        if domains and len(domains) <= 5:
            payload['include_domains'] = domains
        res = requests.post(TAVILY_URL, json=payload, timeout=20)
        data = res.json()
        results = []
        for r in data.get('results', []):
            results.append({
                'title':   r.get('title', ''),
                'url':     r.get('url', ''),
                'content': r.get('content', '')[:1200],
                'score':   r.get('score', 0)
            })
        return {'answer': data.get('answer', ''), 'results': results, 'query': query}
    except Exception as e:
        return {'answer': '', 'results': [], 'error': str(e)}

def search_trade_data(query, max_results=7):
    return _tavily_search(query, None, max_results)

def get_market_prices(product, hs_code, market):
    year = datetime.now().year
    q1 = f'{product} HS {hs_code} import price {market} {year} EUR USD per ton market data'
    q2 = f'Egyptian {product} FOB export price 2024 2025 USD ton'
    r1 = _tavily_search(q1, None, 5)
    r2 = _tavily_search(q2, None, 4)
    answers = [x for x in [r1.get('answer',''), r2.get('answer','')] if x]
    return {
        'answer': ' | '.join(answers)[:1000],
        'results': r1.get('results',[])[:4] + r2.get('results',[])[:3]
    }

def get_trade_trends(product, hs_code, market):
    year = datetime.now().year
    q = f'{product} HS {hs_code} Egypt exports {market} statistics {year-1} {year} growth volume'
    return _tavily_search(q, None, 7)

def get_shipping_rates(product, origin, destination):
    year = datetime.now().year
    q1 = f'sea freight Port Said Egypt {destination} container cost {year} USD'
    q2 = f'Egypt {destination} shipping rate reefer container {year}'
    r1 = _tavily_search(q1, ['freightos.com','globy.com','searates.com'], 4)
    if not r1.get('answer'):
        r1 = _tavily_search(q2, None, 4)
    return r1

def get_regulations(product, hs_code, market):
    year = datetime.now().year
    q = f'{product} EU import requirements {market} {year} certificates food safety standards'
    return _tavily_search(q, None, 6)

def get_competitors(product, hs_code, market):
    q = f'{product} top exporters {market} 2023 2024 market share countries comparison Egypt'
    return _tavily_search(q, None, 6)

def get_fob_price_egypt(product, hs_code):
    year = datetime.now().year
    q = f'Egypt {product} export price FOB {year} USD per ton current'
    return _tavily_search(q, None, 5)