from supabase import create_client, Client
import json

URL = "https://behwybmvebhrggxxkyqs.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJlaHd5Ym12ZWJocmdneHhreXFzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQwMjAwODYsImV4cCI6MjA1OTU5NjA4Nn0.ChkEGsaJaXidGKSkiTQ6msN0xuUS81zhzoex32gwjQ4"  # Kendi anon key’inizi girin.
supabase: Client = create_client(URL, KEY)

def add_product_with_health(name: str, price: float, category: str, store_id: int, health_score, nutrition_facts):
    # Ürünü ekle
    result = supabase.table("products").insert({
        "name": name,
        "price": price,
        "category": category,
        "store_id": store_id
    }).execute()
    
    if not result.data:
        print(f"[Error] Ürün eklemede sorun: {result.error}")
        return None

    product_id = result.data[0]["id"]
    print(f"[Info] Ürün eklendi, id: {product_id}")

    # Health data ekle; veri varsa ekle, yoksa geç
    if health_score is not None and nutrition_facts:
        health_result = supabase.table("health_data").insert({
            "product_id": product_id,
            "health_score": health_score,
            "nutrition_facts": json.dumps(nutrition_facts)
        }).execute()
        if not health_result.data:
            print(f"[Error] Health verisi eklemede sorun: {health_result.error}")
        else:
            print(f"[Info] Health verisi eklendi: {health_result.data[0]}")
    else:
        print(f"[Info] Health verisi eklenmedi (veri bulunamadı ya da boş).")
    
    return result.data[0]
