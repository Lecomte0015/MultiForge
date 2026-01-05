import os
from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_SERVICE_ROLE_KEY") or os.environ.get("SUPABASE_ANON_KEY")

# On renomme la variable pour éviter le conflit
supabase_client: Client = None

if url and key:
    supabase_client = create_client(url, key)
else:
    print("⚠️ Warning: Supabase credentials not found in env.")