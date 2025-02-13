import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def visualize_price_trends(df, product_name):
    """Visualizes price trends over time."""
    if df.empty:
        print("No data to visualize.")
        return

    plt.figure(figsize=(12, 6))

    # Plot prices for each store
    for store in df['store'].unique():
        store_data = df[df['store'] == store]
        plt.plot(store_data['date'], store_data['price'], marker='o', linestyle='-', label=store)

    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.title(f"Price Trends for {product_name}")
    plt.grid(True)
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def visualize_price_comparison(df, product_name, date):
    """Visualizes price comparison across stores for a specific date."""
    if df.empty:
        print("No data to visualize.")
        return

    df = df[df['date'] == date]
    if df.empty:
        print(f"No data for {date} to visualize.")
        return

    plt.figure(figsize=(8, 6))
    plt.bar(df['store'], df['price'], color='skyblue')
    plt.xlabel("Store")
    plt.ylabel("Price")
    plt.title(f"Price Comparison for {product_name} on {date}")
    plt.grid(axis='y')
    plt.tight_layout()
    plt.show()

# Example usage (for testing)
if __name__ == '__main__':
    # Sample data (replace with data from your database)
    data = [
        {'store': 'Amazon', 'price': 25.00, 'date': '2024-01-01'},
        {'store': 'Flipkart', 'price': 22.00, 'date': '2024-01-01'},
        {'store': 'Amazon', 'price': 24.00, 'date': '2024-01-08'},
        {'store': 'Flipkart', 'price': 23.00, 'date': '2024-01-08'},
    ]

    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])

    visualize_price_trends(df, "Example Product")
    visualize_price_comparison(df, "Example Product", pd.to_datetime('2024-01-01'))
