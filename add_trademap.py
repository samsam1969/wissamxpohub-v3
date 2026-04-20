f = open("services/claude_service.py", encoding="utf-8")
c = f.read()
f.close()

# Add Trade Map as Layer 1 (replaces Comtrade for 2024)
old = """    # ── Layer 1: Comtrade data
    real_data = ""
    try:
        from services.trade_data_service import fetch_real_trade_data
        if hs_code and target_market and target_market not in ("__ALL__","European Union (EU-27)",""):
            real_data = fetch_real_trade_data(hs_code, target_market)
    except Exception as e:
        real_data = f"[Comtrade unavailable: {e}]" """

new = """    # ── Layer 1a: Trade Map (2024 data — priority source)
    trademap_data = ""
    try:
        from services.trademap_service import fetch_trademap_data
        if hs_code and target_market and target_market not in ("__ALL__","European Union (EU-27)",""):
            trademap_data = fetch_trademap_data(hs_code, target_market)
    except Exception as e:
        trademap_data = f"[TradeMap unavailable: {e}]"

    # ── Layer 1b: Comtrade (2020-2023 official data)
    real_data = ""
    try:
        from services.trade_data_service import fetch_real_trade_data
        if hs_code and target_market and target_market not in ("__ALL__","European Union (EU-27)",""):
            real_data = fetch_real_trade_data(hs_code, target_market)
    except Exception as e:
        real_data = f"[Comtrade unavailable: {e}]" """

if old in c:
    c = c.replace(old, new, 1)
    print("OK1: Trade Map layer added")
else:
    print("FAIL1")

# Add trademap_data to merged sources
old_merge = """    # ── Merge all sources
    all_data = ""
    if real_data:    all_data += real_data    + "\\n\\n"
    if pricing_data: all_data += pricing_data + "\\n\\n"
    if web_data:     all_data += web_data     + "\\n\\n"
    if cbi_data:     all_data += cbi_data     + "\\n\\n"
    all_data += confidence_block"""

new_merge = """    # ── Merge all sources (Trade Map first = most recent)
    all_data = ""
    if trademap_data: all_data += trademap_data + "\\n\\n"
    if real_data:     all_data += real_data     + "\\n\\n"
    if pricing_data:  all_data += pricing_data  + "\\n\\n"
    if web_data:      all_data += web_data      + "\\n\\n"
    if cbi_data:      all_data += cbi_data      + "\\n\\n"
    all_data += confidence_block"""

if old_merge in c:
    c = c.replace(old_merge, new_merge, 1)
    print("OK2: Trade Map added to merge")
else:
    print("FAIL2")

# Update confidence block
old_conf = """    conf_lines = []
    if real_data and "Comtrade" in real_data: conf_lines.append("بيانات التجارة: 90/100 [UN Comtrade رسمي]")
    if web_data and len(web_data) > 50:       conf_lines.append("بيانات الويب: 70/100 [بحث حديث]")
    conf_lines.append("الرسوم الجمركية: 95/100 [اتفاقية EU-مصر 0%]")
    conf_lines.append("التسعير: 72/100 [تقدير محسوب]")"""

new_conf = """    conf_lines = []
    if trademap_data and "TradeMap" in trademap_data: conf_lines.append("بيانات 2024: 88/100 [ITC Trade Map - preliminary]")
    if real_data and "Comtrade" in real_data:         conf_lines.append("بيانات 2020-2023: 92/100 [UN Comtrade رسمي]")
    if web_data and len(web_data) > 50:               conf_lines.append("بيانات الويب: 70/100 [بحث حديث]")
    conf_lines.append("الرسوم الجمركية: 95/100 [اتفاقية EU-مصر 0%]")
    conf_lines.append("التسعير: 72/100 [تقدير محسوب]")"""

if old_conf in c:
    c = c.replace(old_conf, new_conf, 1)
    print("OK3: confidence scores updated")
else:
    print("FAIL3")

open("services/claude_service.py", "w", encoding="utf-8").write(c)
print("Done - size:", len(c))
