import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from src.metrics_generator import compute_metrics, MetricsGenerationError
from src.config import Config

@patch("src.metrics_generator.pd.read_csv")
@patch("src.metrics_generator.os.makedirs")
@patch("src.metrics_generator.pd.DataFrame.to_csv")
@patch("src.metrics_generator.logger")
def test_compute_metrics_success(mock_logger, mock_to_csv, mock_makedirs, mock_read_csv):
    customers_df = pd.DataFrame({
        "id": [1, 2],
        "region": ["North", "South"]
    })
    products_df = pd.DataFrame({
        "id": [10, 20],
        "category": ["Electronics", "Fashion"],
        "price": [100, 200]
    })
    sales_df = pd.DataFrame({
        "id": [100, 101],
        "customer_id": [1, 2],
        "product_id": [10, 20],
        "quantity": [2, 3]
    })

    mock_read_csv.side_effect = [customers_df, products_df, sales_df]

    compute_metrics()

    assert mock_read_csv.call_count == 3
    assert mock_makedirs.called
    assert mock_to_csv.call_count == 2
    mock_logger.info.assert_any_call("Metrics computed and saved successfully.")

@patch("src.metrics_generator.pd.read_csv", side_effect=Exception("CSV read error"))
@patch("src.metrics_generator.logger")
def test_compute_metrics_failure(mock_logger, mock_read_csv):
    with pytest.raises(MetricsGenerationError) as e:
        compute_metrics()
    assert "CSV read error" in str(e.value)
    mock_logger.exception.assert_called()
