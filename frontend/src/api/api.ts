import axios from "axios";
import type { MetricRecord } from "../models/metrics";

const BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:5000/api";
const TIMEOUT = Number(import.meta.env.VITE_API_TIMEOUT) || 5000;

const api = axios.create({
  baseURL: BASE_URL,
  timeout: TIMEOUT,
});

const log = (message: string, data?: any) => {
  console.log(`[API] ${message}`, data ?? "");
};

const handleError = (error: any, endpoint: string) => {
  console.error(`[API] Error fetching ${endpoint}:`, error);
  throw new Error(
    error?.response?.data?.message || `Failed to fetch data from ${endpoint}`
  );
};

export const getTopProducts = async (): Promise<MetricRecord[]> => {
  try {
    const res = await api.get("/top-products");
    log("Top products fetched", res.data);
    return res.data.map((p: any) => ({
      name: p.category,
      value: p.revenue,
    }));
  } catch (err) {
    handleError(err, "/top-products");
  }
  return [];
};

export const getSalesByRegion = async (): Promise<MetricRecord[]> => {
  try {
    const res = await api.get("/sales-by-region");
    log("Sales by region fetched", res.data);
    return res.data.map((r: any) => ({
      name: r.region,
      value: r.revenue,
    }));
  } catch (err) {
    handleError(err, "/sales-by-region");
  }
  return [];
};

export const getSalesByAgeGroup = async (): Promise<MetricRecord[]> => {
  try {
    const res = await api.get("/sales-by-age-group");
    log("Sales by age group fetched", res.data);
    return res.data.map((a: any) => ({
      name: a.age_group,
      value: a.revenue,
    }));
  } catch (err) {
    handleError(err, "/sales-by-age-group");
  }
  return [];
};
