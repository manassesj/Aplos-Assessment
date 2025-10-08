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
        df = df.fillna(method="ffill")
        if "price" in df.columns:
            df = df[df["price"] > 0]
        logger.info(f"{df_name} cleaned successfully: {len(df)} rows")
        return df
    except Exception as e:
        logger.exception(f"Error cleaning {df_name}")
        raise DataCleaningError(f"Failed to clean {df_name}") from e

def main():
    try:
        customers = pd.read_csv(Config.CUSTOMERS_PATH)
        products = pd.read_csv(Config.PRODUCTS_PATH)
        sales = pd.read_csv(Config.SALES_PATH)

        customers_clean = clean_data(customers, "customers")
        products_clean = clean_data(products, "products")
        sales_clean = clean_data(sales, "sales")

        os.makedirs(Config.PROCESSED_DIR, exist_ok=True)
        customers_clean.to_csv(Config.CLEAN_CUSTOMERS_PATH, index=False)
        products_clean.to_csv(Config.CLEAN_PRODUCTS_PATH, index=False)
        sales_clean.to_csv(Config.CLEAN_SALES_PATH, index=False)

        logger.info("All datasets cleaned successfully.")
    except Exception as e:
        logger.exception("Data cleaning pipeline failed.")
        raise DataCleaningError(str(e)) from e

if __name__ == "__main__":
    main()
