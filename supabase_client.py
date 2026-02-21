from supabase import create_client
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

print("SUPABASE_URL loaded:", bool(SUPABASE_URL))
print("SERVICE KEY loaded:", bool(SUPABASE_SERVICE_KEY))

if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
    raise Exception("Supabase environment variables not loaded")

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_SERVICE_KEY
)
