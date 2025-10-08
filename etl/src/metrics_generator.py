# src/metrics_generator.py
import pandas as pd
import os
from .config import Config
from .utils.logger import get_logger
from .utils.exceptions import MetricsGenerationError

logger = get_logger(__name__)

def compute_metrics():
    try:
        logger.info("Computing business metrics...")
        customers = pd.read_csv(Config.CLEAN_CUSTOMERS_PATH)
        products = pd.read_csv(Config.CLEAN_PRODUCTS_PATH)
        sales = pd.read_csv(Config.CLEAN_SALES_PATH)

        merged = sales.merge(customers, left_on="customer_id", right_on="id") \
                      .merge(products, left_on="product_id", right_on="id", suffixes=("_cust", "_prod"))

        merged["revenue"] = merged["quantity"] * merged["price"]

        revenue_by_region = merged.groupby("region")["revenue"].sum().reset_index()
        top_products = merged.groupby("category")["revenue"].sum().sort_values(ascending=False).reset_index()

        os.makedirs(Config.REPORTS_DIR, exist_ok=True)
        revenue_by_region.to_csv(os.path.join(Config.REPORTS_DIR, "revenue_by_region.csv"), index=False)
        top_products.to_csv(os.path.join(Config.REPORTS_DIR, "top_products.csv"), index=False)

        logger.info("Metrics computed and saved successfully.")
    except Exception as e:
        logger.exception("Error computing metrics.")
        raise MetricsGenerationError(str(e)) from e

if __name__ == "__main__":
    compute_metrics()
