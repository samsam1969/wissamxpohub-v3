import os, sys, re
sys.path.insert(0, r"C:\Users\DELL\Desktop\wissamxpohub-backend")
from dotenv import load_dotenv
load_dotenv()

# الـ anon key موجود في الـ .env
supabase_url = os.getenv("SUPABASE_URL", "")
service_key  = os.getenv("SUPABASE_SERVICE_KEY", "")

# نجيب الـ anon key من الـ .env لو موجود
anon_key = os.getenv("SUPABASE_ANON_KEY", "")

print(f"SUPABASE_URL: {supabase_url}")
print(f"SERVICE_KEY:  {service_key[:30]}..." if service_key else "SERVICE_KEY: MISSING")
print(f"ANON_KEY:     {anon_key[:30]}..." if anon_key else "ANON_KEY: MISSING")

# نطبع محتوى الـ .env كامل
env_path = r"C:\Users\DELL\Desktop\wissamxpohub-backend\.env"
if os.path.exists(env_path):
    with open(env_path, 'r') as f:
        for line in f:
            if 'SUPABASE' in line:
                print(f"ENV: {line.strip()[:80]}")
