from selenium_scraper import scrape_market_data
from supabase_integration import save_to_supabase

def main():
    print("Starting the scraping process...")
    data = scrape_market_data()  # Scraping işlemi
    print(f"Data received: {data}")

    print("Saving data in Supabase...")
    save_to_supabase(data)  # Verileri Supabase'e kaydetme
    print("Data successfully recorded.")

if __name__ == "__main__":
    main()
