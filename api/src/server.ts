import app from "./app.js";
import { PORT } from "./config/index.js";
import logger from "./utils/logger.js";

app.listen(PORT, () => {
  logger.info(`Server running on port ${PORT}`);
});
