import pandas as pd
import os
from .config import Config
from .utils.logger import get_logger
from .utils.exceptions import DataCleaningError

logger = get_logger(__name__)

def clean_data(df, df_name):
    try:
        logger.info(f"Cleaning {df_name}...")
        df = df.drop_duplicates()
        df = df.ffill()
        if "price" in df.columns:
            df = df[df["price"] > 0]
        logger.info(f"{df_name} cleaned successfully: {len(df)} rows")
        return df
    except Exception as e:
        logger.exception(f"Error cleaning {df_name}")
        raise DataCleaningError(f"Failed to clean {df_name}") from e

def save_as_json(df, path):
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        df.to_json(path, orient="records", lines=True)
        logger.info(f"Saved cleaned data as JSON: {path} ({len(df)} rows)")
    except Exception as e:
        logger.exception(f"Error saving JSON {path}")
        raise DataCleaningError(f"Failed to save JSON {path}") from e

def main():
    try:
        logger.info("Starting data cleaning pipeline...")

        customers_path = Config.CUSTOMERS_PATH.replace(".csv", ".json")
        products_path = Config.PRODUCTS_PATH.replace(".csv", ".json")
        sales_path = Config.SALES_PATH.replace(".csv", ".json")

        for path in [customers_path, products_path, sales_path]:
            if not os.path.exists(path):
                raise DataCleaningError(f"File not found: {path}")

        customers = pd.read_json(customers_path)
        products = pd.read_json(products_path)
        sales = pd.read_json(sales_path)

        customers_clean = clean_data(customers, "customers")
        products_clean = clean_data(products, "products")
        sales_clean = clean_data(sales, "sales")

        save_as_json(customers_clean, Config.CLEAN_CUSTOMERS_PATH_JSON)
        save_as_json(products_clean, Config.CLEAN_PRODUCTS_PATH_JSON)
        save_as_json(sales_clean, Config.CLEAN_SALES_PATH_JSON)


        logger.info("All datasets cleaned and saved as JSON successfully.")

    except Exception as e:
        logger.exception("Data cleaning pipeline failed.")
        raise DataCleaningError(str(e)) from e

if __name__ == "__main__":
    main()
