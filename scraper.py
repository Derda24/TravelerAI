from supabase import create_client, Client
from difflib import SequenceMatcher

# Supabase setup
SUPABASE_URL = "https://behwybmvebhrggxxkyqs.supabase.co"
SUPABASE_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJlaHd5Ym12ZWJocmdneHhreXFzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQwMjAwODYsImV4cCI6MjA1OTU5NjA4Nn0.ChkEGsaJaXidGKSkiTQ6msN0xuUS81zhzoex32gwjQ4"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_API_KEY)

# Map store IDs to names
STORE_NAMES = {
    1: "Lidl",
    2: "Carrefour",
    3: "Dia",
    4: "Mercadona",
    5: "El Corte Inglés"
}

# Normalize product names for matching
def normalize(text: str) -> str:
    return text.lower().replace(" ", "").replace("-", "").replace(",", "").replace(".", "")

# Compute similarity ratio
def similar(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()

# Compare products across all stores (optionally filter by category)
def compare_products(product_name: str, category: str = None) -> dict:
    # Build query
    query = supabase.table("products").select("*").eq("name", product_name)
    if category:
        query = query.eq("category", category)
    response = query.execute()

    products = getattr(response, "data", []) or []
    if not products:
        return {"message": f"No products found with the name: {product_name}"}

    # Group by store
    store_comparison = {}
    for p in products:
        sid = p.get("store_id")
        store_name = STORE_NAMES.get(sid, f"Store {sid}")
        entry = {"category": p.get("category"), "price": p.get("price")}
        store_comparison.setdefault(store_name, []).append(entry)

    # Now find best price per store
    # Optionally, you can compute overall cheapest here

    return store_comparison
