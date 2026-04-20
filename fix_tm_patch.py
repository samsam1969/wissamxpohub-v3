import shutil
from datetime import datetime

f = open("services/claude_service.py", encoding="utf-8")
c = f.read()
f.close()
shutil.copy2("services/claude_service.py", f"services/claude_service_BACKUP_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py")

# Find the data fetch area and add trademap
old = """    # ── Layer 1a: Trade Map (2024 data — priority source)
    trademap_data = ""
    try:
        from services.trademap_service import fetch_trademap_data
        if hs_code and target_market and target_market not in ("__ALL__","European Union (EU-27)",""):
            trademap_data = fetch_trademap_data(hs_code, target_market)
    except Exception as e:
        trademap_data = f"[TradeMap unavailable: {e}]" """

if old in c:
    print("Already patched - checking merge...")
else:
    # Find Layer 1 Comtrade block and add trademap before it
    old2 = """    # ── Layer 1: Comtrade data
    real_data = ""
    try:
        from services.trade_data_service import fetch_real_trade_data
        if hs_code and target_market and target_market not in ("__ALL__","European Union (EU-27)",""):
            real_data = fetch_real_trade_data(hs_code, target_market)
    except Exception as e:
        real_data = f"[Comtrade unavailable: {e}]" """

    new2 = """    # ── Layer 1a: Trade Map (2024 data — priority)
    trademap_data = ""
    try:
        from services.trademap_service import fetch_trademap_data
        if hs_code and target_market and target_market not in ("__ALL__","European Union (EU-27)",""):
            trademap_data = fetch_trademap_data(hs_code, target_market)
    except Exception as e:
        trademap_data = f"[TradeMap unavailable: {e}]"

    # ── Layer 1b: Comtrade data
    real_data = ""
    try:
        from services.trade_data_service import fetch_real_trade_data
        if hs_code and target_market and target_market not in ("__ALL__","European Union (EU-27)",""):
            real_data = fetch_real_trade_data(hs_code, target_market)
    except Exception as e:
        real_data = f"[Comtrade unavailable: {e}]" """

    if old2 in c:
        c = c.replace(old2, new2, 1)
        print("OK1: trademap layer added before comtrade")
    else:
        # Find any real_data definition and add trademap before it
        idx = c.find("    real_data = \"\"\n    try:\n        from services.trade_data_service")
        if idx != -1:
            insert = """    # ── Layer 1a: Trade Map (2024 data)
    trademap_data = ""
    try:
        from services.trademap_service import fetch_trademap_data
        if hs_code and target_market and target_market not in ("__ALL__","European Union (EU-27)",""):
            trademap_data = fetch_trademap_data(hs_code, target_market)
    except Exception as e:
        trademap_data = f"[TradeMap: {e}]"

    """
            c = c[:idx] + insert + c[idx:]
            print("OK1b: trademap inserted")
        else:
            print("FAIL1: cannot find insertion point")

# Fix merge - add trademap_data
old_merge = """    # ── Merge all sources (Trade Map first = most recent)
    all_data = ""
    if trademap_data: all_data += trademap_data + "\\n\\n"
    if real_data:     all_data += real_data     + "\\n\\n"
    if pricing_data:  all_data += pricing_data  + "\\n\\n"
    if web_data:      all_data += web_data      + "\\n\\n"
    if cbi_data:      all_data += cbi_data      + "\\n\\n"
    all_data += confidence_block"""

old_merge2 = """    # ── Merge all sources
    all_data = ""
    if real_data:    all_data += real_data    + "\\n\\n"
    if pricing_data: all_data += pricing_data + "\\n\\n"
    if web_data:     all_data += web_data     + "\\n\\n"
    if cbi_data:     all_data += cbi_data     + "\\n\\n"
    all_data += confidence_block"""

if old_merge not in c:
    if old_merge2 in c:
        c = c.replace(old_merge2, """    # ── Merge all sources
    all_data = ""
    if trademap_data: all_data += trademap_data + "\\n\\n"
    if real_data:     all_data += real_data     + "\\n\\n"
    if pricing_data:  all_data += pricing_data  + "\\n\\n"
    if web_data:      all_data += web_data      + "\\n\\n"
    if cbi_data:      all_data += cbi_data      + "\\n\\n"
    all_data += confidence_block""", 1)
        print("OK2: merge updated with trademap")
    else:
        # Find and fix merge block
        idx_merge = c.find("all_data = \"\"")
        if idx_merge != -1:
            print("Found all_data at:", idx_merge)
            print(repr(c[idx_merge:idx_merge+300]))
else:
    print("OK: merge already correct")

open("services/claude_service.py", "w", encoding="utf-8").write(c)
print("Done - size:", len(c))
