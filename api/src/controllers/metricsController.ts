import { Request, Response, NextFunction } from "express";
import {
  getSalesByAgeGroup,
  getSalesByRegion,
  getTopProducts,
} from "../services/metricsService.js";

export async function topProducts(
  req: Request,
  res: Response,
  next: NextFunction
) {
  try {
    const data = await getTopProducts();
    res.json(data);
  } catch (err) {
    next(err);
  }
}

export async function salesByRegion(
  req: Request,
  res: Response,
  next: NextFunction
) {
  try {
    const data = await getSalesByRegion();
    res.json(data);
  } catch (err) {
    next(err);
  }
}

export async function salesByAgeGroup(
  req: Request,
  res: Response,
  next: NextFunction
) {
  try {
    const data = await getSalesByAgeGroup();
    res.json(data);
  } catch (err) {
    next(err);
  }
}
