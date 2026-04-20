import sys
sys.path.insert(0, '.')
from dotenv import load_dotenv
load_dotenv()
from services.knowledge_service import supabase

supabase.table('knowledge_base').delete().eq('id', '590008a5-33c8-48b5-9ed6-2d255d336a0c').execute()
print('Done - deleted')
