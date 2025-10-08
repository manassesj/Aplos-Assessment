import pytest
import pandas as pd
from unittest.mock import patch
from src.metrics_generator import compute_metrics, MetricsGenerationError

@patch("src.metrics_generator.read_json")
@patch("src.metrics_generator.os.makedirs")
@patch("src.metrics_generator.logger")
def test_compute_metrics_success(mock_logger, mock_makedirs, mock_read_json):
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

    mock_read_json.side_effect = [customers_df, products_df, sales_df]

    with patch.object(pd.DataFrame, "to_csv") as mock_to_csv:
        compute_metrics()

        assert mock_read_json.call_count == 3
        assert mock_makedirs.called
        assert mock_to_csv.call_count == 0
        mock_logger.info.assert_any_call("Metrics computed and saved successfully.")

@patch("src.metrics_generator.read_json", side_effect=Exception("JSON read error"))
@patch("src.metrics_generator.logger")
def test_compute_metrics_failure(mock_logger, mock_read_json):
    with pytest.raises(MetricsGenerationError) as e:
        compute_metrics()
    assert "JSON read error" in str(e.value)
    mock_logger.exception.assert_called()
