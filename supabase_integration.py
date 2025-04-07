from supabase import create_client, Client

# Supabase bağlantısı
url = "https://behwybmvebhrggxxkyqs.supabase.co"  # 🔁 Buraya kendi Supabase URL'ni yaz
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJlaHd5Ym12ZWJocmdneHhreXFzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQwMjAwODYsImV4cCI6MjA1OTU5NjA4Nn0.ChkEGsaJaXidGKSkiTQ6msN0xuUS81zhzoex32gwjQ4"               # 🔁 Buraya kendi Supabase API Key'ini yaz
supabase: Client = create_client(url, key)

# Ürün eklemek
def add_product(name, price, category, store_id):
    data = {
        "name": name,
        "price": price,
        "category": category,
        "store_id": store_id
    }
    response = supabase.table("products").insert(data).execute()
    return response

# Sağlık verisi eklemek
def add_health_data(product_id, nutrition_facts, health_score):
    data = {
        "product_id": product_id,
        "nutrition_facts": nutrition_facts,
        "health_score": health_score
    }
    response = supabase.table("health_data").insert(data).execute()
    return response

# 🚀 Örnek kullanım
if __name__ == "__main__":
    # Yeni ürün ekleme
    product_response = add_product("Elma", 1.25, "Meyve", 1)
    print("Ürün eklendi:", product_response.data)

    # Sağlık verisi ekleme (product_id'yi yukarıdan al)
    if product_response.data:
        product_id = product_response.data[0]["id"]
        health_response = add_health_data(product_id, {"kalori": 52, "lif": 2.4}, 8.5)
        print("Sağlık verisi eklendi:", health_response.data)
