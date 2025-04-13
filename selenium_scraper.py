import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from supabase_client import add_product_with_health  # Supabase'e ekleme yapan modül
from openfoodfacts_api import get_health_data        # OpenFoodFacts'tan veri çeken modül

# Marketler yapılandırması
STORES = {
    "Lidl": {
        "name": "Lidl",
        "base": "https://www.lidl.es",
        "all_cats": "/es/todas-las-categorias/c10005018",
        "selector": ".product-grid-box",
        "price_selector": ".m-price__price",
        "title_selector": ".m-typo.m-typo--tiny"
    },
    "Carrefour": {
        "name": "Carrefour",
        "base": "https://www.carrefour.es",
        "all_cats": "/supermercado/categorias",
        "selector": ".ProductCard__root",
        "price_selector": ".price",
        "title_selector": ".product-card__title"
    },
    "Dia": {
        "name": "Dia",
        "base": "https://www.dia.es",
        "all_cats": "/compra-online/",
        "selector": ".product-item",
        "price_selector": ".price",
        "title_selector": ".product-title"
    },
    "Mercadona": {
        "name": "Mercadona",
        "base": "https://www.mercadona.es",
        "all_cats": "/supermercado",
        "selector": ".product-tile",
        "price_selector": ".price",
        "title_selector": ".product-name"
    },
    "ElCorteIngles": {
        "name": "El Corte Inglés",
        "base": "https://www.elcorteingles.es",
        "all_cats": "/supermercado",
        "selector": ".product-card",
        "price_selector": ".price",
        "title_selector": ".product-title"
    }
}

def get_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
    return webdriver.Chrome(options=options)

def scrape_store_products(store_key):
    store = STORES[store_key]
    url = store["base"] + store["all_cats"]
    print(f"🔍 {store['name']} sayfası yükleniyor: {url}")

    driver = get_driver()
    try:
        driver.get(url)
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, store["selector"]))
        )
        time.sleep(2)  # Ekstra bekleme (gerekirse artırılabilir)
        soup = BeautifulSoup(driver.page_source, "html.parser")
    except Exception as e:
        print(f"❌ {store['name']} sayfası yüklenirken hata: {e}")
        driver.quit()
        return []
    driver.quit()

    products = []
    for card in soup.select(store["selector"]):
        try:
            name_el = card.select_one(store["title_selector"])
            price_el = card.select_one(store["price_selector"])
            if not name_el or not price_el:
                continue

            name = name_el.get_text(strip=True)
            price_text = price_el.get_text(strip=True)
            price = float(price_text.replace("€", "").replace(",", "."))
            store_id = list(STORES.keys()).index(store_key) + 1

            products.append({
                "name": name,
                "price": price,
                "category": "general",
                "store_id": store_id
            })
        except Exception as e:
            print(f"[{store['name']}] Ürün ayrıştırma hatası: {e}")
    print(f"✅ {store['name']} için {len(products)} ürün bulundu.")
    return products

def run_scraper_and_save():
    all_products = []
    for key in STORES:
        products = scrape_store_products(key)
        all_products.extend(products)

    for product in all_products:
        name = product["name"]
        price = product["price"]
        category = product["category"]
        store_id = product["store_id"]

        health_info = get_health_data(name)
        health_score = health_info.get("health_score") if health_info else None
        nutrition_facts = health_info.get("nutrition_facts") if health_info else None

        product_id = add_product_with_health(
            name=name,
            price=price,
            category=category,
            store_id=store_id,
            health_score=health_score,
            nutrition_facts=nutrition_facts
        )
        if product_id:
            print(f"🟢 '{name}' eklendi (ID: {product_id}) | Health Score: {health_score}")
        else:
            print(f"🔴 '{name}' eklenemedi.")

if __name__ == "__main__":
    run_scraper_and_save()
