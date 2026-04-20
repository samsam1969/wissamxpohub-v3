import sys, os
sys.path.insert(0, '.')
from dotenv import load_dotenv
load_dotenv()
from services.knowledge_service import supabase

profiles = supabase.table('user_profiles').select('*').execute()
plans = supabase.table('user_plans').select('*').execute()
print(f'Profiles: {len(profiles.data)}')
print(f'Plans: {len(plans.data)}')
for p in profiles.data:
    print(f'  - {p.get("email")} | {p.get("plan_type")}')
