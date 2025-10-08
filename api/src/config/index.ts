import dotenv from "dotenv";
import path from "path";

dotenv.config();

export const PORT = process.env.PORT || 3000;
export const DATA_DIR =
  process.env.DATA_DIR || path.resolve(__dirname, "../../data");
