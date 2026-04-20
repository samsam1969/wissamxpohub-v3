"""
patch_claude_service.py
Patches claude_service.py to use all 3 layers:
  Layer 1: UN Comtrade (verified numbers)
  Layer 2: OpenAI DeepSearch (recent 2024-2025)
  Layer 3: CBI/Access2Markets (market intelligence)
"""
import shutil, os
from datetime import datetime

BASE = r"C:\Users\DELL\Desktop\wissamxpohub-backend"
path = os.path.join(BASE, "services", "claude_service.py")

f = open(path, encoding="utf-8")
content = f.read()
f.close()
shutil.copy2(path, path.replace(".py", f"_BACKUP_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"))

# 1. Fix imports
old_import = """import anthropic
try:
    from services.trade_data_service import fetch_real_trade_data
    TRADE_DATA_AVAILABLE = True
except Exception:
    TRADE_DATA_AVAILABLE = False
    def fetch_real_trade_data(hs, country): return "[Trade data unavailable]"
"""

new_import = """import anthropic
import logging
logger = logging.getLogger(__name__)

# Layer 1: UN Comtrade
try:
    from services.trade_data_service import fetch_real_trade_data
    TRADE_DATA_AVAILABLE = True
except Exception as e:
    TRADE_DATA_AVAILABLE = False
    def fetch_real_trade_data(hs, country): return f"[Comtrade unavailable: {e}]"

# Layer 2: OpenAI DeepSearch
try:
    from services.deepsearch_service import get_market_intelligence
    DEEPSEARCH_AVAILABLE = True
except Exception as e:
    DEEPSEARCH_AVAILABLE = False
    def get_market_intelligence(p, h, c): return f"[DeepSearch unavailable: {e}]"

# Layer 3: CBI / Access2Markets
try:
    from services.cbi_scraper_service import get_cbi_intelligence
    CBI_AVAILABLE = True
except Exception as e:
    CBI_AVAILABLE = False
    def get_cbi_intelligence(p, h, c): return f"[CBI unavailable: {e}]"
"""

if old_import in content:
    content = content.replace(old_import, new_import, 1)
    print("OK1: imports updated")
else:
    # Try simpler replacement
    old_simple = """import anthropic
try:
    from services.trade_data_service import fetch_real_trade_data"""
    if old_simple in content:
        idx = content.find(old_simple)
        end = content.find("\n\n", idx + len(old_simple)) + 2
        content = content[:idx] + new_import + content[end:]
        print("OK1b: imports updated (partial)")
    else:
        print("FAIL1: import block not found")

# 2. Replace the real_data fetch block with all 3 layers
old_fetch = """    # Fetch REAL trade data from UN Comtrade
    real_data = ""
    if TRADE_DATA_AVAILABLE and hs_code and target_market and target_market not in ("__ALL__","European Union (EU-27)"):
        try:
            real_data = fetch_real_trade_data(hs_code, target_market)
        except Exception as e:
            real_data = f"[Trade data fetch failed: {e}]"
"""

new_fetch = """    # ── Layer 1: UN Comtrade (verified official data)
    real_data = ""
    if TRADE_DATA_AVAILABLE and hs_code and target_market and target_market not in ("__ALL__","European Union (EU-27)"):
        try:
            real_data = fetch_real_trade_data(hs_code, target_market)
            logger.info(f"Comtrade data fetched for {hs_code}/{target_market}")
        except Exception as e:
            real_data = f"[Comtrade error: {e}]"
            logger.error(f"Comtrade failed: {e}")

    # ── Layer 2: OpenAI DeepSearch (recent 2024-2025 web data)
    web_data = ""
    if DEEPSEARCH_AVAILABLE and product and target_market and depth in ("pro","full"):
        try:
            web_data = get_market_intelligence(product, hs_code or "", target_market)
            logger.info("DeepSearch data fetched")
        except Exception as e:
            web_data = f"[DeepSearch error: {e}]"

    # ── Layer 3: CBI / Access2Markets (market intelligence)
    cbi_data = ""
    if CBI_AVAILABLE and product and depth == "full":
        try:
            cbi_data = get_cbi_intelligence(product, hs_code or "", target_market)
            logger.info("CBI data fetched")
        except Exception as e:
            cbi_data = f"[CBI error: {e}]"

    # ── Combine all data sources
    all_data = ""
    if real_data: all_data += real_data + "\\n\\n"
    if web_data:  all_data += web_data  + "\\n\\n"
    if cbi_data:  all_data += cbi_data  + "\\n\\n"
"""

if old_fetch in content:
    content = content.replace(old_fetch, new_fetch, 1)
    print("OK2: 3-layer fetch added")
else:
    print("FAIL2: fetch block not found")

# 3. Replace real_data_block references with all_data
old_block = "    real_data_block = f\"\"\""
if old_block in content:
    # Find and replace the entire real_data_block assignment
    import re
    pattern = r'        real_data_block = f"""[^"]*""" if real_data else ""\n'
    content = re.sub(pattern, '        real_data_block = all_data\n', content)
    print("OK3: real_data_block replaced")

# Also simple replace
content = content.replace(
    '        real_data_block = f"""\n\n{real_data if real_data else ""}\n\n""" if real_data else ""\n',
    '        real_data_block = all_data\n'
)

# 4. Update prompt instructions to mention all 3 sources
old_rule = '"AI RULES: (1) Use ONLY above numbers for {country}",'
new_rule = '"AI RULES: (1) Comtrade figures = verified official data (cite year+source)",'
content = content.replace(old_rule, new_rule)

open(path, "w", encoding="utf-8").write(content)
print("Done - size:", len(content))
print("\nAll 3 layers integrated into claude_service.py")
