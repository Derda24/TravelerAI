import requests

def get_health_data(product_name):
    """
    OpenFoodFacts API üzerinden verilen ürün adına ait sağlık verilerini çeker.
    """
    try:
        url = "https://world.openfoodfacts.org/cgi/search.pl"
        params = {
            "search_terms": product_name,
            "search_simple": 1,
            "action": "process",
            "json": 1
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if data.get("count", 0) > 0 and data.get("products"):
                # İlk ürünü temsilci olarak seçiyoruz.
                product = data["products"][0]
                # OpenFoodFacts ürünlerinde nutriscore_score, nutriments gibi alanlar olabilir.
                health_score = product.get("nutriscore_score")
                nutrition_facts = product.get("nutriments")
                return {"health_score": health_score, "nutrition_facts": nutrition_facts}
        else:
            print(f"OpenFoodFacts API error: Status code {response.status_code}")
    except Exception as e:
        print(f"OpenFoodFacts API exception for '{product_name}': {e}")
    return None
