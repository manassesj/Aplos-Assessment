import pandas as pd
from faker import Faker
import random
import os
from datetime import datetime
from .config import Config
from .utils.logger import get_logger
from .utils.exceptions import DataGenerationError

fake = Faker()
logger = get_logger(__name__)

def generate_customers(n):
    customers = []
    for i in range(1, n + 1):
        customers.append({
            "id": i,
            "name": fake.name(),
            "age": random.randint(18, 70),
            "region": random.choice(["North", "South", "East", "West"])
        })
    return pd.DataFrame(customers)

def generate_products(n):
    categories = ["Electronics", "Fashion", "Groceries", "Home", "Sports"]
    products = []
    for i in range(1, n + 1):
        products.append({
            "id": i,
            "category": random.choice(categories),
            "price": round(random.uniform(10, 2000), 2),
            "supplier": fake.company()
        })
    return pd.DataFrame(products)

def generate_sales(customers, products, n):
    sales = []
    for i in range(1, n + 1):
        sales.append({
            "id": i,
            "customer_id": random.choice(customers["id"].tolist()),
            "product_id": random.choice(products["id"].tolist()),
            "date": fake.date_between(start_date="-1y", end_date="today").isoformat(),
            "quantity": random.randint(1, 5)
        })
    return pd.DataFrame(sales)

def save_data_as_json(df, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_json(path, orient="records", date_format="iso", indent=2)
    logger.info(f"Saved data: {path} ({len(df)} rows)")

def main():
    try:
        logger.info("Starting data generation stage...")
        customers = generate_customers(Config.NUM_CUSTOMERS)
        products = generate_products(Config.NUM_PRODUCTS)
        sales = generate_sales(customers, products, Config.NUM_SALES)

        save_data_as_json(customers, Config.CUSTOMERS_PATH.replace(".csv", ".json"))
        save_data_as_json(products, Config.PRODUCTS_PATH.replace(".csv", ".json"))
        save_data_as_json(sales, Config.SALES_PATH.replace(".csv", ".json"))

        logger.info("Data generation completed successfully.")
    except Exception as e:
        logger.exception("Error generating data")
        raise DataGenerationError(str(e)) from e

if __name__ == "__main__":
    main()
