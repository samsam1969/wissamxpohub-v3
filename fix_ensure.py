content = open('services/credits_service.py', encoding='utf-8').read()

old = '''async def ensure_user_profile(user_id: str, email: str):
    get_user_profile(user_id, email)
    supabase.table("user_profiles").update({
        "last_login": datetime.utcnow().isoformat()
    }).eq("user_id", user_id).execute()'''

new = '''async def ensure_user_profile(user_id: str, email: str):
    get_user_profile(user_id, email)
    supabase.table("user_profiles").update({
        "last_login": datetime.utcnow().isoformat()
    }).eq("user_id", user_id).execute()
    
    # Always ensure user_plans exists
    plan_res = supabase.table("user_plans").select("user_id").eq("user_id", user_id).execute()
    if not plan_res.data:
        supabase.table("user_plans").insert({
            "user_id": user_id,
            "plan_type": "free",
            "reports_used": 0,
            "reports_limit": 1,
            "price_egp": 0
        }).execute()
        print(f"Created user_plans for {email}")'''

content = content.replace(old, new)
open('services/credits_service.py', 'w', encoding='utf-8').write(content)
print('Done - ensure_user_profile fixed')
