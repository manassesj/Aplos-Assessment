import dotenv from "dotenv";
dotenv.config();

export const DATA_DIR = process.env.DATA_DIR || "../etl/data/reports";
export const TOP_PRODUCTS_PATH = `${DATA_DIR}/top_products.json`;
export const REVENUE_BY_REGION_PATH = `${DATA_DIR}/revenue_by_region.json`;
