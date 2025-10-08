import sys
from src.data_generator import main as generate_data
from src.data_cleaner import main as clean_data
from src.metrics_generator import compute_metrics
from src.utils.logger import get_logger
from src.utils.exceptions import DataGenerationError, DataCleaningError, MetricsGenerationError

logger = get_logger(__name__)

def run_data_generation():
    try:
        logger.info("Starting data generation stage...")
        generate_data()
        logger.info("Data generation stage completed successfully.")
    except DataGenerationError as e:
        logger.error(f"Data generation failed: {e}")
        raise

def run_data_cleaning():
    try:
        logger.info("Starting data cleaning stage...")
        clean_data()
        logger.info("Data cleaning stage completed successfully.")
    except DataCleaningError as e:
        logger.error(f"Data cleaning failed: {e}")
        raise

def run_metrics_computation():
    try:
        logger.info("Starting metrics computation stage...")
        compute_metrics()  # now reads JSON cleaned files
        logger.info("Metrics computation stage completed successfully.")
    except MetricsGenerationError as e:
        logger.error(f"Metrics computation failed: {e}")
        raise

def run_pipeline():
    logger.info("ETL pipeline starting...")
    try:
        run_data_generation()
        run_data_cleaning()
        run_metrics_computation()
        logger.info("ETL pipeline completed successfully.")
    except (DataGenerationError, DataCleaningError, MetricsGenerationError) as e:
        logger.exception("ETL pipeline failed.")
        sys.exit(1)
    except Exception as e:
        logger.exception(f"Unexpected error in ETL pipeline: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_pipeline()
