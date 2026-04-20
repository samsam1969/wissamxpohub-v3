f = open("services/claude_service.py", encoding="utf-8")
c = f.read()
f.close()

# Fix FOB defaults per product category
old_fob = """    # ── Layer 3: Pricing engine
    pricing_data = ""
    try:
        # Use average market price as base FOB (from Comtrade unit values if available)
        base_fob = 800  # USD/ton default for most Egyptian agricultural products
        if real_data and "Unit=$" in real_data:
            import re as _re
            uv_match = _re.search(r'Unit=\\$([\\d,]+)/ton', real_data)
            if uv_match:
                base_fob = int(uv_match.group(1).replace(",","")) * 0.45  # FOB ≈ 45% of CIF"""

new_fob = """    # ── Layer 3: Pricing engine
    pricing_data = ""
    try:
        # FOB defaults per product category (USD/ton)
        FOB_DEFAULTS = {
            "081110": 550,  # Frozen strawberries
            "081120": 600,  # Frozen raspberries
            "080510": 350,  # Fresh oranges
            "080410": 500,  # Dates
            "070200": 300,  # Tomatoes
            "070310": 250,  # Onions
            "100630": 400,  # Rice
        }
        base_fob = FOB_DEFAULTS.get((hs_code or "")[:6], 500)
        # Override with real Comtrade unit value if available
        if real_data and "Unit=$" in real_data:
            import re as _re
            uv_match = _re.search(r"Unit=\\$([\\d,]+)/ton", real_data)
            if uv_match:
                uv = int(uv_match.group(1).replace(",",""))
                # CIF → FOB: subtract freight+insurance (~15%)
                base_fob = int(uv * 0.85)"""

if old_fob in c:
    c = c.replace(old_fob, new_fob, 1)
    print("OK: FOB defaults fixed per product")
else:
    print("FAIL - not found")

open("services/claude_service.py", "w", encoding="utf-8").write(c)
print("Done")
