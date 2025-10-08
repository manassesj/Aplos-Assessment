import fs from "fs/promises";
import path from "path";
import { DATA_DIR } from "../config/paths.js";
import logger from "../utils/logger.js";
import { ApiError } from "../utils/ApiError.js";

export interface MetricRecord {
  [key: string]: string | number;
}

async function readJsonFile(fileName: string): Promise<MetricRecord[]> {
  try {
    const filePath = path.join(DATA_DIR, fileName);
    const data = await fs.readFile(filePath, "utf-8");
    return JSON.parse(data);
  } catch (err) {
    logger.error(`Failed to read file ${fileName}: ${(err as Error).message}`);
    throw new ApiError(`Unable to read ${fileName}`, 500);
  }
}

export const getTopProducts = async (): Promise<MetricRecord[]> =>
  await readJsonFile("top_products.json");
export const getSalesByRegion = async (): Promise<MetricRecord[]> =>
  await readJsonFile("revenue_by_region.json");
export const getSalesByAgeGroup = async (): Promise<MetricRecord[]> =>
  await readJsonFile("revenue_by_age_group.json");
