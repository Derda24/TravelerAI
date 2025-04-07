from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from supabase import create_client, Client

# Supabase bağlantısı
url = "https://behwybmvebhrggxxkyqs.supabase.co"   # kendi URL
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJlaHd5Ym12ZWJocmdneHhreXFzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQwMjAwODYsImV4cCI6MjA1OTU5NjA4Nn0.ChkEGsaJaXidGKSkiTQ6msN0xuUS81zhzoex32gwjQ4"               # 🔁 Buraya kendi Supabase API Key'ini yaz"               # kendi key
supabase: Client = create_client(url, key)

# Ürün ekleme fonksiyonu
def add_product(name, price, category, store_id):
    data = {
        "name": name,
        "price": price,
        "category": category,
        "store_id": store_id
    }
    response = supabase.table("products").insert(data).execute()
    return response

# Selenium ayarları
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=options)

# Lidl İspanya sayfası
driver.get("https://www.lidl.es/es/carniceria/c10000757")
time.sleep(5)

# Sayfa içeriğini al ve ayrıştır
soup = BeautifulSoup(driver.page_source, "html.parser")
products = soup.find_all("div", class_="product-grid-box")

for product in products:
    try:
        name = product.find("div", class_="product__title").get_text(strip=True)
        price = product.find("div", class_="price__main").get_text(strip=True).replace("€", "").replace(",", ".")
        category = "Carniceria"
        store_id = 1  # örnek olarak 1 (Lidl)

        result = add_product(name, float(price), category, store_id)
        print("Eklendi:", name, result.status_code)
    except Exception as e:
        print("Hata:", e)

driver.quit()
