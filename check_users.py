import sys
sys.path.insert(0, '.')
from dotenv import load_dotenv
load_dotenv()
from services.knowledge_service import supabase

# Check user plan
res = supabase.table('user_plans').select('*').execute()
print("=== user_plans ===")
for r in res.data:
    print(r)

print("\n=== user_profiles ===")
res2 = supabase.table('user_profiles').select('user_id,email,plan_type,plan,credits_remaining').execute()
for r in res2.data:
    print(r)
