import express from "express";
import router from "./routes/metricsRoutes.js";
import { errorHandler } from "./middlewares/errorHandler.js";

const app = express();

app.use(express.json());
app.use("/api", router);
app.use(errorHandler);

export default app;
