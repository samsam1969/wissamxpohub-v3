import shutil, re
from datetime import datetime

f = open("services/claude_service.py", encoding="utf-8")
content = f.read()
f.close()
shutil.copy2("services/claude_service.py", f"services/claude_service_BACKUP_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py")

# 1. Fix imports - add after existing imports
old_import = "load_dotenv()\nlogger = logging.getLogger(__name__)"
new_import = """load_dotenv()
logger = logging.getLogger(__name__)

# Layer 1: UN Comtrade
try:
    from services.trade_data_service import fetch_real_trade_data
    TRADE_DATA_AVAILABLE = True
except Exception as e:
    TRADE_DATA_AVAILABLE = False
    def fetch_real_trade_data(hs, country): return f"[Comtrade unavailable]"

# Layer 2: OpenAI DeepSearch
try:
    from services.deepsearch_service import get_market_intelligence
    DEEPSEARCH_AVAILABLE = True
except Exception as e:
    DEEPSEARCH_AVAILABLE = False
    def get_market_intelligence(p, h, c): return ""

# Layer 3: CBI scraper
try:
    from services.cbi_scraper_service import get_cbi_intelligence
    CBI_AVAILABLE = True
except Exception as e:
    CBI_AVAILABLE = False
    def get_cbi_intelligence(p, h, c): return ""
"""

if old_import in content:
    content = content.replace(old_import, new_import, 1)
    print("OK1: imports added")
else:
    print("FAIL1:", repr(content[content.find("load_dotenv"):content.find("load_dotenv")+60]))

# 2. Find the real_data fetch in get_export_advice and add layers
old_fetch = """    # Fetch REAL trade data from UN Comtrade
    real_data = ""
    if TRADE_DATA_AVAILABLE and hs_code and target_market"""

# Try alternate version
if old_fetch not in content:
    old_fetch = "    real_data = \"\"\n    if TRADE_DATA_AVAILABLE"

if old_fetch in content:
    # Find end of this block
    idx = content.find(old_fetch)
    end_idx = content.find("\n    # Parse depth", idx)
    if end_idx == -1:
        end_idx = content.find("\n    depth = ", idx)
    if end_idx == -1:
        end_idx = idx + 400

    old_block = content[idx:end_idx]
    new_block = """    # ── Layer 1: Comtrade (official numbers)
    real_data = ""
    if TRADE_DATA_AVAILABLE and hs_code and target_market not in ("__ALL__","European Union (EU-27)",""):
        try:
            real_data = fetch_real_trade_data(hs_code, target_market)
        except Exception as e:
            real_data = f"[Comtrade error: {e}]"

    # ── Layer 2: DeepSearch (recent 2024-2025)
    web_data = ""
    if DEEPSEARCH_AVAILABLE and product and target_market:
        try:
            web_data = get_market_intelligence(product, hs_code or "", target_market)
        except Exception as e:
            web_data = ""

    # ── Layer 3: CBI (full reports only)
    cbi_data = ""

    # ── Merge all sources
    all_data_sources = ""
    if real_data: all_data_sources += real_data + "\\n\\n"
    if web_data:  all_data_sources += web_data  + "\\n\\n"
"""
    content = content[:idx] + new_block + content[end_idx:]
    print("OK2: 3-layer fetch added")
else:
    print("FAIL2 - searching...")
    idx = content.find("real_data")
    print("real_data at:", idx, repr(content[idx:idx+100]))

# 3. Replace all_data_sources into prompts
content = content.replace(
    "{real_data_block}",
    "{all_data_sources}"
)
# Also update the variable name
content = content.replace(
    "real_data_block = all_data\n",
    "real_data_block = all_data_sources\n"
)
content = content.replace(
    'real_data_block = f"""\n\n{real_data if real_data else ""}\n\n""" if real_data else ""\n',
    "real_data_block = all_data_sources\n"
)
print("OK3: variable references updated")

open("services/claude_service.py", "w", encoding="utf-8").write(content)
print("Done - size:", len(content))
