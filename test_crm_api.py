import sys
sys.path.insert(0, '.')
from dotenv import load_dotenv
load_dotenv()

# Test the CRM endpoint directly
import requests

# First get a token - we need to test the API
print("Testing /api/admin/crm/users endpoint...")
r = requests.get('http://localhost:4000/api/admin/crm/users')
print(f"Status without token: {r.status_code}")
print(f"Response: {r.text[:200]}")
