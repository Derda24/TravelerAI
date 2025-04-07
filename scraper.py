import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Tarayıcı ayarları
options = uc.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# User-Agent (güncel)
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

# Driver başlat
driver = uc.Chrome(options=options, use_subprocess=True)

# Web sitesine git
driver.get("https://www.lidl.es/es/carniceria/c10000757")

# Bot olmadığını gösteren işaretçi: biraz bekleme
time.sleep(10)

try:
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CLASS_NAME, "product__title"))
    )
    print("✅ Sayfa yüklendi")
except Exception as e:
    print("❌ Yükleme hatası:", e)

time.sleep(5)
driver.quit()
