filepath = r"C:\Users\DELL\Desktop\wissamxpohub-backend\services\claude_service.py"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

import re

print("=" * 60)
print("AUDIT — Pricing Engine Quality Check")
print("=" * 60)

# 1. Reefer freight rates
print("\n[1] REEFER FREIGHT RATES (per ton):")
for country in ["Germany", "Netherlands", "Spain", "France", "Italy"]:
    m = re.search(rf'"{country}"\s*:\s*(\d+)', content)
    if m:
        val = int(m.group(1))
        old_range = "$70-95" if country in ["Spain","Italy","Netherlands"] else "$85-100"
        new_range = "$115-180"
        status = "✅ FIXED" if val >= 100 else "❌ STILL OLD"
        print(f"  {country:15} = ${val}/ton  {status}")

# 2. Port charges
print("\n[2] PORT CHARGES:")
m = re.search(r'port_charges\s*=\s*(\d+)', content)
if m:
    val = int(m.group(1))
    status = "✅ FIXED" if val >= 50 else "❌ STILL OLD ($35)"
    print(f"  port_charges = ${val}/ton  {status}")

# 3. Insurance
print("\n[3] INSURANCE RATE:")
m = re.search(r'insurance\s*=\s*[^*]+\*\s*([\d.]+)', content)
if m:
    val = float(m.group(1))
    pct = val * 100
    status = "✅ FIXED (1%)" if val >= 0.01 else "⚠️ Low (0.8%)"
    print(f"  insurance = {pct}%  {status}")

# 4. FOB defaults
print("\n[4] FOB DEFAULTS LINKAGE:")
if "get_fob_dict()" in content:
    print("  ✅ Linked to products_registry")
else:
    print("  ❌ NOT linked - using hardcoded values")

# 5. Tavily new functions
print("\n[5] TAVILY ENHANCED PIPELINE:")
funcs = ["get_regulations", "get_competitors", "get_fob_price_egypt"]
for f in funcs:
    if f in content:
        print(f"  ✅ {f}")
    else:
        print(f"  ❌ {f} NOT integrated")

# 6. CAGR distinction
print("\n[6] CAGR TYPE DISTINCTION (Volume vs Value):")
if "CAGR_volume" in content or "حجم النمو" in content or "volume CAGR" in content:
    print("  ✅ CAGR types distinguished")
else:
    print("  ⚠️ CAGR distinction NOT in prompt - يحتاج إضافة")

# 7. Tavily content size
tavily_path = r"C:\Users\DELL\Desktop\wissamxpohub-backend\services\tavily_service.py"
with open(tavily_path, 'r', encoding='utf-8') as f:
    tav = f.read()
print("\n[7] TAVILY CONTENT LIMIT:")
m = re.search(r"\[:(\d+)\]", tav)
if m:
    val = int(m.group(1))
    status = "✅ FIXED" if val >= 1000 else "❌ Still 500"
    print(f"  Content limit: {val} chars  {status}")

print("\n" + "=" * 60)
