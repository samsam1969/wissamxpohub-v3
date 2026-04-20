f = open("services/trademap_service.py", encoding="utf-8")
c = f.read()
f.close()

# Add HS scope warning to format function
old_header = '''    lines = [
        "╔══════════════════════════════════════════════════════════════════╗",
        "║  ITC TRADE MAP — Real Data incl. 2024 (preliminary)            ║",
        f"║  HS:{hs} | {country} | {ft}                                    ║",
        "╚══════════════════════════════════════════════════════════════════╝",
        "[src:ITC Trade Map|trademap.org|USD thousand×1000]","",
    ]'''

new_header = '''    # HS scope descriptions
    HS_SCOPE = {
        "080410": "Dates, fresh or dried (HS 080410) — NOT avocado/mango",
        "080440": "Avocados, fresh or dried (HS 080440)",
        "080450": "Guavas, mangoes, mangosteens (HS 080450)",
        "081110": "Frozen strawberries ONLY (HS 081110)",
        "081120": "Frozen raspberries/blackberries (HS 081120)",
        "080510": "Fresh oranges (HS 080510)",
        "070200": "Tomatoes, fresh or chilled (HS 070200)",
        "070310": "Onions and shallots (HS 070310)",
    }
    scope_note = HS_SCOPE.get(hs, f"HS {hs} — verify product scope before analysis")

    lines = [
        "╔══════════════════════════════════════════════════════════════════╗",
        "║  ITC TRADE MAP — Real Data incl. 2024 (preliminary)            ║",
        f"║  HS:{hs} | {country} | {ft}                                    ║",
        "╚══════════════════════════════════════════════════════════════════╝",
        f"[src:ITC Trade Map|trademap.org|USD thousand×1000]",
        f"⚠️ SCOPE: {scope_note}",
        f"⚠️ DATA NOTE: Figures cover ALL products under HS {hs} — not a single product",
        "",
    ]'''

if old_header in c:
    c = c.replace(old_header, new_header, 1)
    print("OK: HS scope warning added")
else:
    print("FAIL")

open("services/trademap_service.py", "w", encoding="utf-8").write(c)
print("Done")
