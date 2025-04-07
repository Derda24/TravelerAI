from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from supabase import create_client, Client

# Supabase bağlantısı
url = "https://behwybmvebhrggxxkyqs.supabase.co"   # kendi Supabase URL
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJlaHd5Ym12ZWJocmdneHhreXFzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQwMjAwODYsImV4cCI6MjA1OTU5NjA4Nn0.ChkEGsaJaXidGKSkiTQ6msN0xuUS81zhzoex32gwjQ4"               # kendi Supabase anon key"               # kendi Supabase anon key
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

# Lidl İspanya sayfası (örnek: İçecekler bölümü)
driver.get("https://www.lidl.es/es/bebidas/c10000912")

# Sayfanın tamamen yüklenmesini bekle (örneğin, ürünlerin bulunduğu div yüklendiğinde)
try:
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "product-grid-box"))
    )
    print("Sayfa tamamen yüklendi.")
except Exception as e:
    print(f"Sayfa yüklenirken hata oluştu: {e}")

time.sleep(5)  # Ekstra bir süre bekleyelim

# Sayfa içeriğini al ve ayrıştır
html = driver.page_source
print("Sayfa içeriği çekildi.")
soup = BeautifulSoup(html, "html.parser")

# Sayfa içeriğini yazdır (HTML'nin doğru olduğundan emin olmak için)
print(soup.prettify())

# Tüm ürünleri ara
products = soup.find_all("div", class_="product-grid-box")
print("Bulunan ürün sayısı:", len(products))

# Ürünleri Supabase'e ekle
for product in products:
    try:
        name = product.find("div", class_="product__title").get_text(strip=True)
        price = product.find("div", class_="price__main").get_text(strip=True).replace("€", "").replace(",", ".")
        category = "Bebidas"  # Bu sayfaya göre kategori içecek
        store_id = 1  # Lidl = 1

        result = add_product(name, float(price), category, store_id)
        print("Eklendi:", name, result.status_code)
    except Exception as e:
        print("Hata:", e)

driver.quit()
