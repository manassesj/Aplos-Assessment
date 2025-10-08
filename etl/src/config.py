import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.getenv("DATA_DIR", os.path.join(BASE_DIR, "../data"))
    LOG_DIR = os.getenv("LOG_DIR", os.path.join(BASE_DIR, "../logs"))
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    RAW_DIR = os.path.join(DATA_DIR, "raw")
    PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
    REPORTS_DIR = os.path.join(DATA_DIR, "reports")

    for path in [DATA_DIR, LOG_DIR, RAW_DIR, PROCESSED_DIR, REPORTS_DIR]:
        os.makedirs(path, exist_ok=True)

    NUM_CUSTOMERS = int(os.getenv("NUM_CUSTOMERS", 100))
    NUM_PRODUCTS = int(os.getenv("NUM_PRODUCTS", 50))
    NUM_SALES = int(os.getenv("NUM_SALES", 500))

    CUSTOMERS_PATH = os.path.join(RAW_DIR, "customers.csv")
    PRODUCTS_PATH = os.path.join(RAW_DIR, "products.csv")
    SALES_PATH = os.path.join(RAW_DIR, "sales.csv")

    CLEAN_CUSTOMERS_PATH_CSV = os.path.join(PROCESSED_DIR, "customers_clean.csv")
    CLEAN_PRODUCTS_PATH_CSV = os.path.join(PROCESSED_DIR, "products_clean.csv")
    CLEAN_SALES_PATH_CSV = os.path.join(PROCESSED_DIR, "sales_clean.csv")

    CLEAN_CUSTOMERS_PATH_JSON = os.path.join(PROCESSED_DIR, "customers_clean.json")
    CLEAN_PRODUCTS_PATH_JSON = os.path.join(PROCESSED_DIR, "products_clean.json")
    CLEAN_SALES_PATH_JSON = os.path.join(PROCESSED_DIR, "sales_clean.json")
