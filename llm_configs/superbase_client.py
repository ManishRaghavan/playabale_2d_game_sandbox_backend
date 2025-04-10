from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env file if running locally

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Missing Supabase credentials. Check SUPABASE_URL and SUPABASE_KEY.")

def supabase_client_setup():
    superbase_client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    return superbase_client