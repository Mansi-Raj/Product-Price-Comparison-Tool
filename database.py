import mysql.connector
from datetime import datetime

class DatabaseManager:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.cursor = self.connection.cursor()
            print("Database connection established.")
        except mysql.connector.Error as err:
            print(f"Error connecting to database: {err}")
            raise

    def disconnect(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()
            print("Database connection closed.")

    def create_table(self):
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS product_prices (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    product_name VARCHAR(255) NOT NULL,
                    store VARCHAR(255) NOT NULL,
                    price DECIMAL(10, 2) NOT NULL,
                    date DATETIME NOT NULL
                )
            """)
            self.connection.commit()
            print("Table 'product_prices' created (if it didn't exist).")
        except mysql.connector.Error as err:
            print(f"Error creating table: {err}")
            raise

    def insert_price(self, product_name, store, price):
        try:
            now = datetime.now()
            sql = "INSERT INTO product_prices (product_name, store, price, date) VALUES (%s, %s, %s, %s)"
            val = (product_name, store, price, now)
            self.cursor.execute(sql, val)
            self.connection.commit()
            print(f"Inserted price for {product_name} from {store}: {price} on {now}")
        except mysql.connector.Error as err:
            print(f"Error inserting data: {err}")
            raise

    def get_prices(self, product_name):
        try:
            sql = "SELECT store, price, date FROM product_prices WHERE product_name = %s ORDER BY date"
            val = (product_name,)
            self.cursor.execute(sql, val)
            results = self.cursor.fetchall()
            return results
        except mysql.connector.Error as err:
            print(f"Error fetching data: {err}")
            raise

    def get_min_price(self, product_name):
        try:
            sql = "SELECT store, MIN(price) FROM product_prices WHERE product_name = %s"
            val = (product_name,)
            self.cursor.execute(sql, val)
            result = self.cursor.fetchone()
            return result
        except mysql.connector.Error as err:
            print(f"Error fetching data: {err}")
            raise
# Example Usage (for testing) - replace with your actual credentials
if __name__ == '__main__':
    db_manager = DatabaseManager("localhost", "your_user", "your_password", "price_comparison") # Replace with your database credentials
    try:
        db_manager.connect()
        db_manager.create_table()
        # Example insertion
        # db_manager.insert_price("Example Product", "Amazon", 25.99)

        # Example retrieval
        prices = db_manager.get_prices("Example Product")
        if prices:
            for store, price, date in prices:
                print(f"Store: {store}, Price: {price}, Date: {date}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        db_manager.disconnect()
