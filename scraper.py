import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from openfoodfacts import API

from supabase_client import add_product_with_health

# Market bilgileriniz
STORES = {
    "Lid1": {
        "name": "Lidl",
        "base": "https://www.lidl.es",
        "all_cats": "/es/todas-las-categorias/c10005018",
        "selector": ".product-grid-box"
    },
    "Carrefour": {
        "name": "Carrefour",
        "base": "https://www.carrefour.es",
        "all_cats": "/supermercado/categorias",
        "selector": ".ProductCard__root"
    },
    "Dia":  {
        "name": "Dia",
        "base": "https://www.dia.es",
        "all_cats": "/supermercado/categorias",
        "selector": ".product-item"  # örnek, siteye göre güncelle\n      },

    },
    "Mercadon": {
        "name": "Mercadona",
        "base": "https://www.mercadona.es",
        "all_cats": "/supermercado/categorias",
        "selector": ".product-tile"  # örnek, siteye göre güncelle\n      },

    },
    "ElCorteIngles": {
        "name": "ElCorteInglés",
        "base": "https://www.elcorteingles.es",
        "all_cats": "/supermercado/categorias",
        "selector": ".product-card"  # örnek, siteye göre güncelle\n      },  
    },
}
# OpenFoodFacts API – user_agent parametresi eklenmiş
api = API(user_agent="MarketScraperBot/1.0 (vturlu.dpointgroup@gmail.com)")

def get_driver():
    opts = Options()
    # Geliştirme sırasında headless mod kapalı olabilir; hata ayıklamak için yorumdan çıkarın.
    opts.add_argument("--headless")
    opts.add_argument("--window-size=1920,1080")
    return webdriver.Chrome(options=opts)

def get_health_data(product_name):
    try:
        results = api.product.search(product_name, page_size=1)
        if results["count"] == 0:
            print(f"[❌] OpenFoodFacts: {product_name} verisi bulunamadı.")
            return None, {}
        food = results["products"][0]
        nutr = food.get("nutriments", {})
        # Örnek sağlık skoru hesaplama (isteğe bağlı olarak güncellenebilir)
        score = 100
        try:
            sugar = float(nutr.get("sugars_100g", 0))
            fat = float(nutr.get("fat_100g", 0))
        except Exception:
            sugar, fat = 0, 0
        if sugar > 10:
            score -= 20
        if fat > 10:
            score -= 20
        return score, nutr
    except Exception as e:
        print(f"[⚠️] OpenFoodFacts hata: {e}")
        return None, {}

def scrape_store(store_id: int):
    s = STORES[store_id]
    drv = get_driver()
    drv.get(s["base"] + s["all_cats"])
    # Sayfanın tamamen yüklenmesini bekleyelim (örneğin tüm kategori linklerini barındıran <a> etiketlerinin yüklenmesi)
    WebDriverWait(drv, 15).until(EC.presence_of_element_located((By.TAG_NAME, "a")))
    soup = BeautifulSoup(drv.page_source, "html.parser")
    
    # Kategori linklerini topla ("/c" içerenler)
    cats = set()
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("/") and "/c" in href:
            cats.add(s["base"] + href)
    print(f"[{s['name']}] {len(cats)} category found")
    
    for url in cats:
        drv.get(url)
        try:
            WebDriverWait(drv, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, s["selector"]))
            )
        except Exception:
            print(f"[!] Kategori yüklenemedi: {url}")
            continue
        time.sleep(2)
        ps = BeautifulSoup(drv.page_source, "html.parser")
        items = ps.select(s["selector"])
        print(f"  → {len(items)} ürün: {url.split('/')[-1]}")
        for p in items:
            try:
                name_elem = p.select_one(".product__title, .ProductCard__title")
                price_elem = p.select_one(".price__main, .ProductCard__price")
                if not name_elem or not price_elem:
                    continue
                name = name_elem.get_text(strip=True)
                price_txt = price_elem.get_text()
                price = float(price_txt.replace("€", "").replace(",", "."))
                category = url.split("/")[-1]
                
                # Ürünü Supabase'e ekle ve eklenen kaydı al
                inserted = add_product_with_health(name, price, category, store_id, None, {})
                if inserted:
                    # OpenFoodFacts'tan veri çek ve health_data ekle
                    health_score, nutrition = get_health_data(name)
                    # Eğer ek güncelleme gerekiyorsa (örneğin health_data'yı eklemek için) bunu supabase_client içindeki fonksiyonla halledebilirsiniz.
                    # Bu örnekte add_product_with_health() eklenmeden önce health verisini alıp ekleyebilirsiniz:
                    # Burada, ürün eklenmişse, health_data'yı Supabase'e eklemek için ek bir çağrı yapıyoruz.
                    from supabase_client import supabase  # tekrar import edilebilir veya fonksiyon içine alınabilir
                    if health_score is not None:
                        supabase.table("health_data").insert({
                            "product_id": inserted["id"],
                            "health_score": health_score,
                            "nutrition_facts": json.dumps(nutrition)
                        }).execute()
                        print(f"[✅] {name} için sağlık verisi eklendi. Skor: {health_score}")
                    else:
                        print(f"[❌] {name} için sağlık verisi eklenemedi.")
                else:
                    print(f"[❌] {name} eklenemedi!")
            except Exception as e:
                print(f"  → Ürün ekleme hatası: {e}")
                continue
    drv.quit()

if __name__ == "__main__":
    for sid in STORES:
        print(f"=== {STORES[sid]['name']} kazınıyor ===")
        scrape_store(sid)
    