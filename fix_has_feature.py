content = open('services/credits_service.py', encoding='utf-8').read()

old = '''def has_feature(user_id: str, feature: str) -> bool:
    plan = get_user_plan(user_id)
    plan_type = plan.get("plan_type", "free")
    sub_end = plan.get("sub_end")
    if sub_end and datetime.strptime(str(sub_end), "%Y-%m-%d").date() < date.today():
        return feature in PLAN_FEATURES.get("free", [])
    return feature in PLAN_FEATURES.get(plan_type, [])'''

new = '''def has_feature(user_id: str, feature: str) -> bool:
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
    return feature in allowed'''

content = content.replace(old, new)
open('services/credits_service.py', 'w', encoding='utf-8').write(content)
print('Done - has_feature fixed')
