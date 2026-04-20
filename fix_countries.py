# Fix 1: Add Cyprus to ITC_CODES in trademap_service.py
f = open("services/trademap_service.py", encoding="utf-8")
c = f.read()
f.close()

old = '    "Hungary":348,'
new = '    "Hungary":348,\n    "Cyprus":196,\n    "Malta":470,\n    "Luxembourg":442,\n    "Croatia":191,\n    "Slovenia":705,\n    "Slovakia":703,\n    "Lithuania":440,\n    "Latvia":428,\n    "Estonia":233,\n    "Ireland":372,'
c = c.replace(old, new, 1)
open("services/trademap_service.py", "w", encoding="utf-8").write(c)
print("OK1: Cyprus + more countries added to Trade Map")

# Fix 2: Add Cyprus to trade_data_service.py
f2 = open("services/trade_data_service.py", encoding="utf-8")
c2 = f2.read()
f2.close()
old2 = '    "Hungary": 348,'
new2 = '    "Hungary": 348,\n    "Cyprus": 196,\n    "Malta": 470,\n    "Luxembourg": 442,\n    "Croatia": 191,\n    "Ireland": 372,\n    "Lithuania": 440,\n    "Latvia": 428,\n    "Estonia": 233,\n    "Slovakia": 703,\n    "Slovenia": 705,'
c2 = c2.replace(old2, new2, 1)
open("services/trade_data_service.py", "w", encoding="utf-8").write(c2)
print("OK2: Cyprus + more countries added to Comtrade")

# Fix 3: Add Cyprus to pricing engine + fix FOB for dates
f3 = open("services/claude_service.py", encoding="utf-8")
c3 = f3.read()
f3.close()

# Add Cyprus VAT
old_vat = '    VAT = {\n        "Germany": 7.0, "Netherlands": 9.0, "France": 5.5,\n        "Belgium": 6.0, "Italy": 4.0, "Spain": 4.0,\n        "Poland": 5.0,  "Austria": 10.0, "Sweden": 12.0,\n    }'
new_vat = '    VAT = {\n        "Germany": 7.0, "Netherlands": 9.0, "France": 5.5,\n        "Belgium": 6.0, "Italy": 4.0, "Spain": 4.0,\n        "Poland": 5.0,  "Austria": 10.0, "Sweden": 12.0,\n        "Cyprus": 5.0, "Malta": 5.0, "Ireland": 4.8,\n        "Denmark": 0.0, "Finland": 14.0, "Portugal": 6.0,\n        "Greece": 13.0, "Luxembourg": 3.0, "Czech Republic": 10.0,\n        "Romania": 9.0, "Hungary": 18.0, "Bulgaria": 20.0,\n    }'
if old_vat in c3:
    c3 = c3.replace(old_vat, new_vat, 1)
    print("OK3: Cyprus VAT added")

# Add Cyprus freight
old_freight = '    FREIGHT = {\n        "Netherlands": 85,  "Germany": 95,   "France": 90,\n        "Belgium": 88,      "Italy": 75,      "Spain": 70,\n        "Poland": 110,      "Austria": 105,   "Sweden": 115,\n    }'
new_freight = '    FREIGHT = {\n        "Netherlands": 85,  "Germany": 95,   "France": 90,\n        "Belgium": 88,      "Italy": 75,      "Spain": 70,\n        "Poland": 110,      "Austria": 105,   "Sweden": 115,\n        "Cyprus": 65,       "Greece": 60,     "Malta": 70,\n        "Ireland": 120,     "Denmark": 100,   "Finland": 120,\n        "Portugal": 80,     "Romania": 95,    "Bulgaria": 85,\n        "Czech Republic": 105, "Hungary": 100, "Luxembourg": 95,\n    }'
if old_freight in c3:
    c3 = c3.replace(old_freight, new_freight, 1)
    print("OK4: Cyprus freight added")

# Fix FOB defaults - add more products
old_fob = '        FOB_DEFAULTS = {\n            "081110": 550,  # Frozen strawberries\n            "081120": 600,  # Frozen raspberries\n            "080510": 350,  # Fresh oranges\n            "080410": 500,  # Dates\n            "070200": 300,  # Tomatoes\n            "070310": 250,  # Onions\n            "100630": 400,  # Rice\n        }'
new_fob = '        FOB_DEFAULTS = {\n            "081110": 550,  # Frozen strawberries\n            "081120": 600,  # Frozen raspberries\n            "081190": 580,  # Other frozen fruit\n            "080510": 350,  # Fresh oranges\n            "080520": 380,  # Mandarins\n            "080410": 480,  # Dates\n            "080440": 600,  # Avocados\n            "070200": 300,  # Tomatoes\n            "070310": 250,  # Onions\n            "070320": 300,  # Garlic\n            "100630": 400,  # Rice\n            "160414": 1200, # Tuna\n            "090111": 2500, # Coffee\n        }'
if old_fob in c3:
    c3 = c3.replace(old_fob, new_fob, 1)
    print("OK5: FOB defaults expanded")

open("services/claude_service.py", "w", encoding="utf-8").write(c3)
print("All fixes done")
