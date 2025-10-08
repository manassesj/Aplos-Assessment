import pandas as pd
import os
from .config import Config
from .utils.logger import get_logger
from .utils.exceptions import MetricsGenerationError

logger = get_logger(__name__)

def read_json(path, df_name):
    try:
        df = pd.read_json(path, orient="records", lines=True)  
        logger.info(f"{df_name} loaded successfully: {len(df)} rows")
        return df
    except Exception as e:
        logger.exception(f"Error reading JSON {df_name}")
        raise MetricsGenerationError(f"Failed to read JSON {df_name}: {e}") from e

def compute_metrics():
    try:
        logger.info("Computing business metrics...")

        customers = read_json(Config.CLEAN_CUSTOMERS_PATH_JSON, "customers")
        products = read_json(Config.CLEAN_PRODUCTS_PATH_JSON, "products")
        sales = read_json(Config.CLEAN_SALES_PATH_JSON, "sales")

        merged = sales.merge(customers, left_on="customer_id", right_on="id") \
                      .merge(products, left_on="product_id", right_on="id", suffixes=("_cust", "_prod"))

        merged["revenue"] = merged["quantity"] * merged["price"]

        revenue_by_region = merged.groupby("region")["revenue"].sum().reset_index()

        top_products = merged.groupby("category")["revenue"].sum().sort_values(ascending=False).reset_index()

        bins = [0, 24, 34, 44, 54, 64, 100]
        labels = ["<25", "25-34", "35-44", "45-54", "55-64", "65+"]
        merged["age_group"] = pd.cut(merged["age"], bins=bins, labels=labels, right=True)
        revenue_by_age_group = merged.groupby("age_group")["revenue"].sum().reset_index()

        # Ensure reports directory exists
        os.makedirs(Config.REPORTS_DIR, exist_ok=True)

        revenue_by_region.to_json(
            os.path.join(Config.REPORTS_DIR, "revenue_by_region.json"),
            orient="records", lines=False, indent=4
        )
        top_products.to_json(
            os.path.join(Config.REPORTS_DIR, "top_products.json"),
            orient="records", lines=False, indent=4
        )
        revenue_by_age_group.to_json(
            os.path.join(Config.REPORTS_DIR, "revenue_by_age_group.json"),
            orient="records", lines=False, indent=4
        )

        logger.info("Metrics computed and saved successfully.")

    except Exception as e:
        logger.exception("Error computing metrics.")
        raise MetricsGenerationError(str(e)) from e

if __name__ == "__main__":
    compute_metrics()
