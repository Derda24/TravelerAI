import time
import random
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Market URL'leri
market_urls = {
    "Lidl": "https://www.lidl.es/es/todas-las-categorias/c10005018",
    "Carrefour": "https://www.carrefour.es/supermercado/categorias",
    "Dia": "https://www.dia.es/compra-online/",
    "Mercadona": "https://www.mercadona.es/supermercado",
    "El Corte Inglés": "https://www.elcorteingles.es/supermercado"
}

# WebDriver ayarları
options = Options()
options.add_argument('--headless')  # Arka planda çalıştırma
options.add_argument('--disable-gpu')  # GPU'yu devre dışı bırak
options.add_argument('--no-sandbox')  # Sanbox modunu devre dışı bırak

# WebDriver başlatma
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Sayfa yüklenirken hata öncesi bekleme fonksiyonu
def wait_for_page_load(url):
    try:
        driver.get(url)
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        print(f"✅ Sayfa başarıyla yüklendi: {url}")
    except Exception as e:
        print(f"❌ {url} sayfası yüklenirken hata: {e}")

# Ürün verisi çekme
def extract_product_data():
    products = []
    try:
        # Sayfada ürünlerin bulunduğu alanı bulun
        product_elements = driver.find_elements(By.CSS_SELECTOR, '.product')  # Burada '.product' uygun CSS sınıfı olmalı
        for product_element in product_elements:
            name = product_element.find_element(By.CSS_SELECTOR, '.product-name').text
            price = product_element.find_element(By.CSS_SELECTOR, '.product-price').text
            products.append({'name': name, 'price': price})
        print("✅ Ürün verisi başarıyla çekildi.")
    except Exception as e:
        print(f"❌ Ürün verisi çekilirken hata: {e}")
    return products

# Fiyatları ve sağlık bilgilerini karşılaştır
def compare_prices_and_health():
    for market, url in market_urls.items():
        print(f"🔍 {market} sayfası yükleniyor: {url}")
        wait_for_page_load(url)
        products = extract_product_data()
        # Ürün verisini Supabase'e kaydetme (örnek bir fonksiyon)
        for product in products:
            # Burada veritabanına kaydetme kodu olmalı
            print(f"Ürün: {product['name']}, Fiyat: {product['price']}")
        time.sleep(random.uniform(2, 4))  # Sayfalar arasında rastgele bekleme

# Ana fonksiyon
def main():
    compare_prices_and_health()
    driver.quit()

if __name__ == "__main__":
    main()
