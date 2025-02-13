import requests
from bs4 import BeautifulSoup
import re

def scrape_amazon(url, product_name):
    """Scrapes price and information from Amazon."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract price (adjust selectors based on actual Amazon page structure)
        price_element = soup.find("span", class_="a-offscreen")
        if price_element:
            price_text = price_element.get_text()
            price = float(re.sub(r'[^\d\.]', '', price_text))
        else:
            price = None

        # Extract product name
        name_element = soup.find("span", id="productTitle")
        if name_element:
            name = name_element.get_text().strip()
        else:
            name = product_name

        return {"store": "Amazon", "product_name": name, "price": price}

    except requests.exceptions.RequestException as e:
        print(f"Error during request: {e}")
        return None
    except Exception as e:
        print(f"Error scraping Amazon: {e}")
        return None

def scrape_flipkart(url, product_name):
    """Scrapes price from Flipkart (example)."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Adjust selectors based on Flipkart's page structure
        price_element = soup.find("div", class_="_30jeq3 _16Jk6d")
        if price_element:
            price_text = price_element.get_text()
            price = float(re.sub(r'[^\d\.]', '', price_text))
        else:
            price = None
        name_element = soup.find("div", class_="_4rR01T")
        if name_element:
            name = name_element.get_text().strip()
        else:
            name = product_name
        return {"store": "Flipkart", "product_name": name, "price": price}

    except requests.exceptions.RequestException as e:
        print(f"Error during request: {e}")
        return None
    except Exception as e:
        print(f"Error scraping Flipkart: {e}")
        return None

# Example Usage (for testing):
if __name__ == '__main__':
    amazon_url = "https://www.amazon.com/dp/B07X2R6KYM" # Replace with an actual Amazon product URL
    flipkart_url = "https://www.flipkart.com/apple-iphone-14-128-gb-midnight/p/itmca73b560820c3"  # Replace with an actual Flipkart product URL
    amazon_data = scrape_amazon(amazon_url, "Test Product")
    flipkart_data = scrape_flipkart(flipkart_url, "Test Product")

    if amazon_data:
        print("Amazon:", amazon_data)
    if flipkart_data:
        print("Flipkart:", flipkart_data)
