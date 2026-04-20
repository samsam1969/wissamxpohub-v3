import os
from supabase import create_client, Client
from datetime import datetime, date
from dotenv import load_dotenv
load_dotenv()

supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_SERVICE_KEY"))

PLANS = {
    'free':     {'limit': 1,   'price': 0},
    'starter':  {'limit': 5,   'price': 299},
    'pro':      {'limit': 25,  'price': 599},
    'agency':   {'limit': 100, 'price': 1490},
}

PLAN_FEATURES = {
    'free':    ['ai_report'],
    'starter': ['ai_report', 'blog', 'scanner', 'history'],
    'pro':     ['ai_report', 'blog', 'scanner', 'history', 'buyers'],
    'agency':  ['ai_report', 'blog', 'scanner', 'history', 'buyers', 'admin'],
}

def get_user_profile(user_id: str, email: str = "") -> dict:
    res = supabase.table("user_profiles").select("*").eq("user_id", user_id).execute()
    if res.data:
        return res.data[0]
    supabase.table("user_profiles").insert({
        "user_id": user_id, "email": email,
        "plan": "free", "plan_type": "free",
        "credits_remaining": 1,
        "sub_status": "active",
        "sub_start": str(date.today()),
    }).execute()
    supabase.table("user_plans").insert({
        "user_id": user_id, "plan_type": "free",
        "reports_used": 0, "reports_limit": 1, "price_egp": 0
    }).on_conflict("user_id").execute()
    return get_user_profile(user_id, email)

def get_user_plan(user_id: str) -> dict:
    res = supabase.table("user_plans").select("*").eq("user_id", user_id).execute()
    if res.data:
        return res.data[0]
    return {"plan_type": "free", "reports_used": 0, "reports_limit": 1}

def has_feature(user_id: str, feature: str) -> bool:
    plan = get_user_plan(user_id)
    plan_type = plan.get("plan_type", "free")
    
    # Check subscription expiry
    sub_end = plan.get("sub_end")
    if sub_end:
        try:
            if datetime.strptime(str(sub_end)[:10], "%Y-%m-%d").date() < date.today():
                plan_type = "free"
        except:
            pass
    
    # Check report limit for ai_report feature
    if feature == "ai_report":
        used = plan.get("reports_used", 0)
        limit = plan.get("reports_limit", 1)
        if used >= limit:
            return False
    
    allowed = PLAN_FEATURES.get(plan_type, [])
    return feature in allowed

async def ensure_user_profile(user_id: str, email: str):
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
        print(f"Created user_plans for {email}")
    
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
        print(f"Created user_plans for {email}")

async def get_user_credits(user_id: str) -> int:
    plan = get_user_plan(user_id)
    return plan["reports_limit"] - plan["reports_used"]

async def deduct_credit(user_id: str) -> int:
    plan = get_user_plan(user_id)
    used = plan["reports_used"]
    limit = plan["reports_limit"]
    plan_type = plan.get("plan_type", "free")

    sub_end = plan.get("sub_end")
    if sub_end and datetime.strptime(str(sub_end), "%Y-%m-%d").date() < date.today():
        raise Exception("انتهى اشتراكك — جدّد للاستمرار.")

    if used >= limit:
        wa_msg = f"مرحباً، أريد ترقية باقتي من {plan_type} — وصلت للحد الأقصى"
        wa_link = f"https://wa.me/201116415272?text={wa_msg}"
        raise Exception(
            f"وصلت للحد الأقصى ({limit}) تقارير لباقة {plan_type}. "
            f"للترقية: {wa_link}"
        )

    new_used = used + 1
    supabase.table("user_plans").update({
        "reports_used": new_used
    }).eq("user_id", user_id).execute()

    supabase.table("user_profiles").update({
        "total_reports": supabase.table("user_profiles").select("total_reports").eq("user_id", user_id).execute().data[0].get("total_reports", 0) + 1
    }).eq("user_id", user_id).execute()

    return limit - new_used

async def get_plan_info(user_id: str) -> dict:
    plan = get_user_plan(user_id)
    return {
        "plan_type":        plan.get("plan_type", "free"),
        "reports_used":     plan.get("reports_used", 0),
        "reports_limit":    plan.get("reports_limit", 1),
        "reports_remaining": plan.get("reports_limit", 1) - plan.get("reports_used", 0),
        "price_egp":        plan.get("price_egp", 0),
        "features":         PLAN_FEATURES.get(plan.get("plan_type", "free"), [])
    }

def save_report_history(user_id: str, email: str, product: str, hs_code: str, market: str, summary: str = ""):
    try:
        supabase.table("report_history").insert({
            "user_id": user_id, "email": email,
            "product": product, "hs_code": hs_code,
            "market": market, "report_type": "full",
            "report_summary": summary[:500] if summary else ""
        }).execute()
    except Exception as e:
        print(f"History save error: {e}")

def reset_monthly_credits():
    from datetime import datetime
    if datetime.today().day == 1:
        supabase.table("user_plans").update({"reports_used": 0}).neq("plan_type", "agency").execute()
        print("Monthly reset done")
