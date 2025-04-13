from supabase import create_client, Client

# Supabase connection
URL = "https://behwybmvebhrggxxkyqs.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJlaHd5Ym12ZWJocmdneHhreXFzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQwMjAwODYsImV4cCI6MjA1OTU5NjA4Nn0.ChkEGsaJaXidGKSkiTQ6msN0xuUS81zhzoex32gwjQ4"   # ← replace with your anon key
supabase: Client = create_client(URL, KEY)

def save_to_supabase(data):
    """
    data: list of dicts, each with keys name, price, category, store_id
    """
    if not data:
        print("No data to save.")
        return
    resp = supabase.table("products").insert(data).execute()
    print("Supabase response:", getattr(resp, "data", resp))
    return resp
def add_product(name: str, price: float, category: str, store_id: int):
    return supabase.table("products").insert({
        "name": name,
        "price": price,
        "category": category,
        "store_id": store_id
    }).execute()