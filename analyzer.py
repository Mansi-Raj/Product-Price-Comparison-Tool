import pandas as pd

def compare_prices(data):
    """Compares prices from different stores."""
    df = pd.DataFrame(data)
    if df.empty:
        return "No data to compare."

    # Find the minimum price
    min_price = df['price'].min()
    best_stores = df[df['price'] == min_price]['store'].tolist()

    if len(best_stores) == 1:
        return f"The best price is ${min_price:.2f} at {best_stores[0]}."
    else:
        stores_str = ", ".join(best_stores)
        return f"The best price is ${min_price:.2f} at {stores_str}."

def analyze_price_trends(data):
    """Analyzes price trends over time."""
    df = pd.DataFrame(data)
    if df.empty:
        return "No data to analyze."

    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    df = df.sort_index()

    # Calculate rolling mean (e.g., 7-day rolling average)
    df['rolling_avg'] = df['price'].rolling(window=7).mean()
    return df

# Example usage (for testing)
if __name__ == '__main__':
    # Sample data (replace with data from your database)
    data = [
        {'store': 'Amazon', 'price': 25.00, 'date': '2024-01-01'},
        {'store': 'Flipkart', 'price': 22.00, 'date': '2024-01-01'},
        {'store': 'Amazon', 'price': 24.00, 'date': '2024-01-08'},
        {'store': 'Flipkart', 'price': 23.00, 'date': '2024-01-08'},
    ]

    comparison_result = compare_prices(data)
    print("Price Comparison:", comparison_result)

    trend_analysis = analyze_price_trends(data)
    print("\nPrice Trend Analysis:")
    print(trend_analysis)
