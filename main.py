from selenium_scraper import scrape_market_data
from supabase_integration import save_to_supabase

def main():
    print("Starting the scraping process...")
    data = scrape_market_data()
    print(f"Data received ({len(data)} items):", data)

    print("Saving data in Supabase...")
    save_to_supabase(data)
    print("Data successfully recorded.")

if __name__ == "__main__":
    main()
