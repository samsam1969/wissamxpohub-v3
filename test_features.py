import sys
sys.path.insert(0, '.')
from dotenv import load_dotenv
load_dotenv()
from services.credits_service import has_feature, get_user_plan

user_id = 'ac79451c-68d9-4c2e-9768-5a84580bcff9'
plan = get_user_plan(user_id)
print("Plan:", plan)
print("has buyers:", has_feature(user_id, 'buyers'))
print("has scanner:", has_feature(user_id, 'scanner'))
print("has blog:", has_feature(user_id, 'blog'))
print("has ai_report:", has_feature(user_id, 'ai_report'))
