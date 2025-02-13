import time
import scraper
import database
import analyzer
import visualizer
import schedule

# Database Configuration
DB_HOST = "localhost"
DB_USER = "root"  
DB_PASSWORD = "Mansi@113"  
DB_NAME = "price_comparison"

# Scraping Targets
PRODUCTS = {
    "Product 1": {
        "amazon": "https://www.amazon.in/All-new-Echo/dp/B085FY9NK8/ref=s9_acsd_al_ot_c2_x_2_t?_encoding=UTF8&pf_rd_m=A21TJRUUN4KGV&pf_rd_s=merchandised-search-4&pf_rd_r=A0S31AVN79MC2DF9BPPN&pf_rd_p=f0de0514-61a4-4975-8ce9-62854b6441ea&pf_rd_t=&pf_rd_i=14156834031",  
        "flipkart": "https://www.flipkart.com/alexa-amazon-echo-4th-gen-premium-sound-powered-dolby-assistant-smart-speaker/p/itmb27bcafb030cc?pid=ACCH4N5D9HGZ7GXF&lid=LSTACCH4N5D9HGZ7GXFVX6NKJ&marketplace=FLIPKART&store=0pm%2F0o7&srno=b_1_2&otracker=browse&fm=organic&iid=en_RVCYV0E8y1dzJcNQNah852uhZVfJBrdMJe7-FlBmygQRC9NCjuohz8XSbl7bWLcIC3-F5r-8_gghbjru65o-uQ%3D%3D&ppt=sp&ppn=productListView&ssid=cmhf4u2fy80000001739431661931"
    },
}


def scrape_and_store():
    """Scrapes product prices and stores them in the database."""
    db_manager = database.DatabaseManager(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)
    try:
        db_manager.connect()
        db_manager.create_table()

        for product_name, urls in PRODUCTS.items():
            for store, url in urls.items():
                if store == "amazon":
                    data = scraper.scrape_amazon(url, product_name)
                elif store == "flipkart":
                    data = scraper.scrape_flipkart(url, product_name)
                else:
                    print(f"Unsupported store: {store}")
                    continue

                if data:
                    db_manager.insert_price(data['product_name'], data['store'], data['price'])

    except Exception as e:
        print(f"An error occurred during scraping and storing: {e}")
    finally:
        db_manager.disconnect()


def analyze_and_visualize(product_name):
    """Analyzes price data and generates visualizations."""
    db_manager = database.DatabaseManager(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)
    try:
        db_manager.connect()
        prices = db_manager.get_prices(product_name)

        if prices:
            # Convert the list of tuples to a list of dictionaries
            data = [{'store': row[0], 'price': row[1], 'date': row[2]} for row in prices]

            # Price Comparison
            comparison_result = analyzer.compare_prices(data)
            print(f"Price Comparison for {product_name}: {comparison_result}")

            # Price Trend Analysis
            df = analyzer.analyze_price_trends(data)

            # Visualization
            visualizer.visualize_price_trends(df, product_name)

        else:
            print(f"No price data found for {product_name}.")

    except Exception as e:
        print(f"An error occurred during analysis and visualization: {e}")
    finally:
        db_manager.disconnect()


def main():
    """Main function to schedule scraping and analysis."""
    # Schedule scraping (e.g., every day at midnight)
    schedule.every().day.at("00:00").do(scrape_and_store)

    # Run initial scrape
    scrape_and_store()

    # Run analysis and visualization for each product
    for product_name in PRODUCTS.keys():
        analyze_and_visualize(product_name)

    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute


if __name__ == "__main__":
    main()
