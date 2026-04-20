import os
from supabase import create_client, Client
from dotenv import load_dotenv
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

def search_knowledge_base(hs_code: str = None, market: str = None, category: str = None, limit: int = 10) -> str:
    try:
        query = supabase.table("knowledge_base").select("*").eq("is_active", True)
        if hs_code:
            query = query.or_(f"hs_code.eq.{hs_code},hs_code.is.null")
        if market:
            query = query.or_(f"market.ilike.%{market}%,market.is.null")
        if category:
            query = query.eq("category", category)
        results = query.order("priority", desc=True).limit(limit).execute()
        if not results.data:
            return ""
        kb_text = "=== قاعدة البيانات الداخلية (بيانات محدثة - أولوية عالية) ===\n"
        for row in results.data:
            kb_text += f"\n[{row['category']}] {row['title']}\n"
            kb_text += f"{row['content']}\n"
            if row.get('source'):
                kb_text += f"المصدر: {row['source']} | "
            if row.get('valid_from'):
                kb_text += f"تاريخ البيانات: {row['valid_from']}\n"
            kb_text += "---\n"
        return kb_text
    except Exception as e:
        return f"[KB Error: {e}]"

def add_knowledge(category: str, title: str, content: str,
                  hs_code: str = None, market: str = None,
                  source: str = None, priority: int = 5,
                  subcategory: str = None) -> bool:
    try:
        supabase.table("knowledge_base").insert({
            "category": category,
            "subcategory": subcategory,
            "hs_code": hs_code,
            "market": market,
            "title": title,
            "content": content,
            "source": source,
            "priority": priority,
            "is_active": True
        }).execute()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def update_knowledge(id: str, content: str, source: str = None) -> bool:
    try:
        update_data = {"content": content, "updated_at": "NOW()"}
        if source:
            update_data["source"] = source
        supabase.table("knowledge_base").update(update_data).eq("id", id).execute()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def deactivate_knowledge(id: str) -> bool:
    try:
        supabase.table("knowledge_base").update({"is_active": False}).eq("id", id).execute()
        return True
    except Exception as e:
        return False
