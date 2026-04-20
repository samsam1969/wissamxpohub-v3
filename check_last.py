import sys
sys.path.insert(0, '.')
from dotenv import load_dotenv
load_dotenv()
from services.knowledge_service import supabase

res = supabase.table('knowledge_base').select('id,title,content').order('created_at', desc=True).limit(1).execute()
if res.data:
    r = res.data[0]
    print(f"ID: {r['id']}")
    print(f"Title: {r['title']}")
    print(f"Content preview: {r['content'][:100]}")
