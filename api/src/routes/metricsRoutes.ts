import { Router } from "express";
import {
  salesByAgeGroup,
  salesByRegion,
  topProducts,
} from "../controllers/metricsController.js";

const router = Router();

router.get("/top-products", topProducts);
router.get("/sales-by-region", salesByRegion);
router.get("/sales-by-age-group", salesByAgeGroup);

export default router;
