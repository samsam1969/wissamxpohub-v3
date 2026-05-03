import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SERVICE_KEY")
)

def verify_token(request):
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return None
    token = auth_header.split(" ")[1]
    try:
        result = supabase.auth.get_user(token)
        if result and result.user:
            return {
                "sub":   result.user.id,
                "email": result.user.email
            }
        return None
    except Exception as e:
        print(f"Auth error: {e}")
        return None
