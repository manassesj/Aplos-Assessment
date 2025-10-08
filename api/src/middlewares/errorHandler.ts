import { Request, Response, NextFunction } from "express";
import { ApiError } from "../utils/ApiError.js";
import logger from "../utils/logger.js";

export function errorHandler(err: Error | ApiError, _req: Request, res: Response, _next: NextFunction) {
  const statusCode = err instanceof ApiError ? err.statusCode : 500;
  logger.error(`${err.name}: ${err.message}`);
  res.status(statusCode).json({ error: err.message });
}
