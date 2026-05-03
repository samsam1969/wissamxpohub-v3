import sys
sys.path.insert(0, '.')
from dotenv import load_dotenv
load_dotenv()
from services.knowledge_service import add_knowledge, deactivate_knowledge, supabase

def list_entries():
    res = supabase.table("knowledge_base").select("id,category,title,priority,is_active").order("priority", desc=True).execute()
    print(f"\n{'#':<3} {'Category':<15} {'Pri':<5} {'Active':<8} Title")
    print("-"*80)
    for i, r in enumerate(res.data):
        print(f"{i+1:<3} {r['category']:<15} {r['priority']:<5} {str(r['is_active']):<8} {r['title'][:50]}")

def add_entry():
    print("\n=== اضافة بيانات جديدة ===")
    category  = input("category (shipping/pricing/regulations/market): ").strip()
    title     = input("title: ").strip()
    content   = input("content: ").strip()
    hs_code   = input("hs_code (Enter to skip): ").strip() or None
    market    = input("market (Enter to skip): ").strip() or None
    source    = input("source: ").strip() or None
    priority  = int(input("priority 1-10: ").strip() or "5")
    ok = add_knowledge(category, title, content, hs_code, market, source, priority)
    print("Done" if ok else "Failed")

def deactivate_entry():
    list_entries()
    id = input("\nEnter ID to deactivate: ").strip()
    ok = deactivate_knowledge(id)
    print("Done" if ok else "Failed")

while True:
    print("\n=== Knowledge Base Manager ===")
    print("1. List all")
    print("2. Add new")
    print("3. Deactivate")
    print("4. Exit")
    choice = input("Choice: ").strip()
    if choice == "1": list_entries()
    elif choice == "2": add_entry()
    elif choice == "3": deactivate_entry()
    elif choice == "4": break
