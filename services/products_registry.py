# ═══════════════════════════════════════════════
# WissamXpoHub V3 - Master Product Registry
# ═══════════════════════════════════════════════
# الخضار والفاكهة المصرية فقط (طازجة + مجمدة + مجففة)
# قاعدة بيانات مركزية واحدة - أي تحديث يطبّق على الكل
# ═══════════════════════════════════════════════

PRODUCTS_REGISTRY = {
    # ═══ فاكهة طازجة (21) ═══
    "080510": {"name_en": "Fresh Oranges",         "name_ar": "برتقال طازج",      "category": "fruit_fresh",   "fob_usd_ton": 380,  "season": "Nov-Apr"},
    "080521": {"name_en": "Mandarins/Clementines", "name_ar": "يوسفي/كليمانتين", "category": "fruit_fresh",   "fob_usd_ton": 420,  "season": "Oct-Mar"},
    "080529": {"name_en": "Other Citrus",          "name_ar": "حمضيات أخرى",     "category": "fruit_fresh",   "fob_usd_ton": 400,  "season": "Year-round"},
    "080540": {"name_en": "Grapefruit",            "name_ar": "جريب فروت",        "category": "fruit_fresh",   "fob_usd_ton": 450,  "season": "Year-round"},
    "080550": {"name_en": "Lemons/Limes",          "name_ar": "ليمون",             "category": "fruit_fresh",   "fob_usd_ton": 400,  "season": "Year-round"},
    "080410": {"name_en": "Dates",                 "name_ar": "تمور مصرية",       "category": "fruit_fresh",   "fob_usd_ton": 850,  "season": "Year-round"},
    "080420": {"name_en": "Figs",                  "name_ar": "تين",               "category": "fruit_fresh",   "fob_usd_ton": 600,  "season": "Jul-Sep"},
    "080430": {"name_en": "Pineapples",            "name_ar": "أناناس",            "category": "fruit_fresh",   "fob_usd_ton": 800,  "season": "Year-round"},
    "080440": {"name_en": "Avocados",              "name_ar": "أفوكادو",           "category": "fruit_fresh",   "fob_usd_ton": 1500, "season": "Mar-Jul"},
    "080450": {"name_en": "Guava/Mango",           "name_ar": "جوافة/مانجو",      "category": "fruit_fresh",   "fob_usd_ton": 700,  "season": "Jun-Sep"},
    "080610": {"name_en": "Fresh Grapes",          "name_ar": "عنب طازج",          "category": "fruit_fresh",   "fob_usd_ton": 800,  "season": "Jun-Sep"},
    "080711": {"name_en": "Watermelons",           "name_ar": "بطيخ",               "category": "fruit_fresh",   "fob_usd_ton": 280,  "season": "Apr-Aug"},
    "080719": {"name_en": "Melons/Cantaloupe",     "name_ar": "شمام/كانتالوب",    "category": "fruit_fresh",   "fob_usd_ton": 350,  "season": "Apr-Sep"},
    "080810": {"name_en": "Apples",                "name_ar": "تفاح",               "category": "fruit_fresh",   "fob_usd_ton": 500,  "season": "Limited"},
    "080910": {"name_en": "Apricots",              "name_ar": "مشمش طازج",         "category": "fruit_fresh",   "fob_usd_ton": 600,  "season": "May-Jul"},
    "080930": {"name_en": "Peaches/Nectarines",    "name_ar": "خوخ/نكتارين",      "category": "fruit_fresh",   "fob_usd_ton": 500,  "season": "Jun-Aug"},
    "080940": {"name_en": "Plums",                 "name_ar": "برقوق",             "category": "fruit_fresh",   "fob_usd_ton": 550,  "season": "Jun-Aug"},
    "081010": {"name_en": "Fresh Strawberries",    "name_ar": "فراولة طازجة",     "category": "fruit_fresh",   "fob_usd_ton": 1400, "season": "Dec-Apr"},
    "081020": {"name_en": "Raspberries/Blackberries","name_ar": "توت أحمر/أسود",  "category": "fruit_fresh",   "fob_usd_ton": 2500, "season": "Niche"},
    "081030": {"name_en": "Currants",              "name_ar": "كشمش",               "category": "fruit_fresh",   "fob_usd_ton": 2200, "season": "Niche"},
    "081090": {"name_en": "Other Fresh Berries",   "name_ar": "توت طازج آخر",     "category": "fruit_fresh",   "fob_usd_ton": 1800, "season": "Niche"},

    # ═══ فاكهة مجمدة (3) ═══
    "081110": {"name_en": "Frozen Strawberries",   "name_ar": "فراولة مجمدة",     "category": "fruit_frozen",  "fob_usd_ton": 1200, "season": "Year-round"},
    "081120": {"name_en": "Frozen Raspberries",    "name_ar": "توت أحمر مجمد",    "category": "fruit_frozen",  "fob_usd_ton": 1400, "season": "Year-round"},
    "081190": {"name_en": "Other Frozen Fruits",   "name_ar": "فواكه مجمدة أخرى","category": "fruit_frozen",  "fob_usd_ton": 1100, "season": "Year-round"},

    # ═══ فاكهة مجففة (4) ═══
    "081310": {"name_en": "Dried Apricots",        "name_ar": "مشمش مجفف",         "category": "fruit_dried",   "fob_usd_ton": 3500, "season": "Year-round"},
    "081320": {"name_en": "Dried Prunes",          "name_ar": "برقوق مجفف",       "category": "fruit_dried",   "fob_usd_ton": 2800, "season": "Year-round"},
    "081340": {"name_en": "Mixed Dried Fruits",    "name_ar": "فواكه مجففة متنوعة","category": "fruit_dried",  "fob_usd_ton": 3200, "season": "Year-round"},
    "081350": {"name_en": "Dried Coconut",         "name_ar": "جوز هند مجفف",     "category": "fruit_dried",   "fob_usd_ton": 2000, "season": "Year-round"},

    # ═══ خضار طازجة (22) ═══
    "070200": {"name_en": "Tomatoes",              "name_ar": "طماطم",             "category": "veg_fresh",     "fob_usd_ton": 320,  "season": "Year-round"},
    "070310": {"name_en": "Onions",                "name_ar": "بصل",                "category": "veg_fresh",     "fob_usd_ton": 220,  "season": "Feb-Jul"},
    "070320": {"name_en": "Garlic",                "name_ar": "ثوم",                "category": "veg_fresh",     "fob_usd_ton": 380,  "season": "Mar-Jun"},
    "070390": {"name_en": "Leeks",                 "name_ar": "كراث",               "category": "veg_fresh",     "fob_usd_ton": 280,  "season": "Nov-Apr"},
    "070410": {"name_en": "Cauliflower/Broccoli",  "name_ar": "قرنبيط/بروكلي",    "category": "veg_fresh",     "fob_usd_ton": 420,  "season": "Nov-Apr"},
    "070490": {"name_en": "Cabbages",              "name_ar": "كرنب",               "category": "veg_fresh",     "fob_usd_ton": 350,  "season": "Nov-Apr"},
    "070511": {"name_en": "Lettuce (Cabbage)",     "name_ar": "خس",                 "category": "veg_fresh",     "fob_usd_ton": 380,  "season": "Nov-Apr"},
    "070519": {"name_en": "Other Lettuce",         "name_ar": "خس آخر",             "category": "veg_fresh",     "fob_usd_ton": 350,  "season": "Nov-Apr"},
    "070610": {"name_en": "Carrots/Turnips",       "name_ar": "جزر/لفت",           "category": "veg_fresh",     "fob_usd_ton": 250,  "season": "Nov-Apr"},
    "070690": {"name_en": "Beetroot",              "name_ar": "بنجر",               "category": "veg_fresh",     "fob_usd_ton": 280,  "season": "Nov-Apr"},
    "070700": {"name_en": "Cucumbers/Gherkins",    "name_ar": "خيار",               "category": "veg_fresh",     "fob_usd_ton": 350,  "season": "Oct-May"},
    "070810": {"name_en": "Fresh Peas",            "name_ar": "بازلاء طازجة",     "category": "veg_fresh",     "fob_usd_ton": 600,  "season": "Jan-Apr"},
    "070820": {"name_en": "Green Beans",           "name_ar": "فاصوليا خضراء",   "category": "veg_fresh",     "fob_usd_ton": 600,  "season": "Oct-May"},
    "070910": {"name_en": "Artichokes",            "name_ar": "خرشوف",             "category": "veg_fresh",     "fob_usd_ton": 800,  "season": "Nov-Apr"},
    "070920": {"name_en": "Asparagus",             "name_ar": "هليون",             "category": "veg_fresh",     "fob_usd_ton": 1200, "season": "Jan-May"},
    "070930": {"name_en": "Eggplant",              "name_ar": "باذنجان",           "category": "veg_fresh",     "fob_usd_ton": 380,  "season": "Oct-May"},
    "070940": {"name_en": "Celery",                "name_ar": "كرفس",               "category": "veg_fresh",     "fob_usd_ton": 450,  "season": "Nov-Apr"},
    "070951": {"name_en": "Mushrooms",             "name_ar": "مشروم",             "category": "veg_fresh",     "fob_usd_ton": 1500, "season": "Year-round"},
    "070960": {"name_en": "Peppers",               "name_ar": "فلفل",               "category": "veg_fresh",     "fob_usd_ton": 550,  "season": "Oct-May"},
    "070970": {"name_en": "Spinach",               "name_ar": "سبانخ",             "category": "veg_fresh",     "fob_usd_ton": 400,  "season": "Nov-Apr"},
    "070993": {"name_en": "Courgettes/Pumpkin",    "name_ar": "كوسا/قرع",         "category": "veg_fresh",     "fob_usd_ton": 320,  "season": "Oct-May"},
    "071090": {"name_en": "Other Fresh Vegetables","name_ar": "خضار طازجة أخرى", "category": "veg_fresh",     "fob_usd_ton": 380,  "season": "Year-round"},

    # ═══ خضار مجمدة (5) ═══
    "071010": {"name_en": "Frozen Potatoes",       "name_ar": "بطاطس مجمدة",       "category": "veg_frozen",    "fob_usd_ton": 380,  "season": "Year-round"},
    "071021": {"name_en": "Frozen Peas",           "name_ar": "بازلاء مجمدة",     "category": "veg_frozen",    "fob_usd_ton": 450,  "season": "Year-round"},
    "071022": {"name_en": "Frozen Beans",          "name_ar": "فاصوليا مجمدة",    "category": "veg_frozen",    "fob_usd_ton": 500,  "season": "Year-round"},
    "071040": {"name_en": "Frozen Sweet Corn",     "name_ar": "ذرة حلوة مجمدة",   "category": "veg_frozen",    "fob_usd_ton": 400,  "season": "Year-round"},
    "071080": {"name_en": "Mixed Frozen Vegetables","name_ar": "خضار مجمدة متنوعة","category": "veg_frozen",   "fob_usd_ton": 480,  "season": "Year-round"},
}


# ═══════════════════════════════════════════════
# Helper Functions
# ═══════════════════════════════════════════════

def get_product(hs_code):
    return PRODUCTS_REGISTRY.get(hs_code, {})

def get_fob(hs_code, default=500):
    p = PRODUCTS_REGISTRY.get(hs_code, {})
    return p.get("fob_usd_ton", default)

def get_name(hs_code, lang="en"):
    p = PRODUCTS_REGISTRY.get(hs_code, {})
    return p.get(f"name_{lang}", f"Unknown ({hs_code})")

def is_registered(hs_code):
    return hs_code in PRODUCTS_REGISTRY

def all_hs_codes():
    return set(PRODUCTS_REGISTRY.keys())

def by_category(category):
    return {k: v for k, v in PRODUCTS_REGISTRY.items() if v.get("category") == category}

def get_fob_dict():
    return {k: v["fob_usd_ton"] for k, v in PRODUCTS_REGISTRY.items()}


if __name__ == "__main__":
    print(f"📊 Total registered products: {len(PRODUCTS_REGISTRY)}")
    categories = {}
    for hs, data in PRODUCTS_REGISTRY.items():
        cat = data["category"]
        categories[cat] = categories.get(cat, 0) + 1
    print()
    for cat, count in sorted(categories.items()):
        print(f"  {cat}: {count}")
