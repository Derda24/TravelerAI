from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from supabase import create_client, Client

# Supabase connection
url = "https://behwybmvebhrggxxkyqs.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJlaHd5Ym12ZWJocmdneHhreXFzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQwMjAwODYsImV4cCI6MjA1OTU5NjA4Nn0.ChkEGsaJaXidGKSkiTQ6msN0xuUS81zhzoex32gwjQ4"
supabase: Client = create_client(url, key)

# Selenium scraping setup
def get_selenium_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    return driver

# Add product to Supabase
def add_product(name, price, category, store_id):
    data = {
        "name": name,
        "price": price,
        "category": category,
        "store_id": store_id
    }
    response = supabase.table("products").insert(data).execute()
    return response

# Scrape categories from a website (example with Lidl)
def scrape_categories():
    driver = get_selenium_driver()
    driver.get("https://www.lidl.es/es/todas-las-categorias/c10005018")
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    category_links = soup.find_all("a", href=True)
    
    valid_links = []
    for link in category_links:
        href = link['href']
        if href.startswith("/es/") and "/c" in href:
            full_url = "https://www.lidl.es" + href
            if full_url not in valid_links:
                valid_links.append(full_url)

    driver.quit()
    return valid_links

# Scrape products from categories and add them to Supabase
def scrape_products_from_category(category_url):
    driver = get_selenium_driver()
    driver.get(category_url)
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, "product-grid-box")))
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    products = soup.find_all("div", class_="product-grid-box")

    for product in products:
        try:
            name = product.find("div", class_="product__title").get_text(strip=True)
            price = product.find("div", class_="price__main").get_text(strip=True).replace("€", "").replace(",", ".")
            category = category_url.split("/")[-1]
            store_id = 1  # Lidl store
            add_product(name, float(price), category, store_id)
        except Exception as e:
            print("Error adding product:", e)

    driver.quit()
