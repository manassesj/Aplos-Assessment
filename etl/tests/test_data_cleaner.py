import pytest
import pandas as pd
from unittest.mock import patch
from src.data_cleaner import clean_data, main
from src.utils.exceptions import DataCleaningError

def test_clean_data_removes_duplicates_and_fills_na():
    df = pd.DataFrame({
        "id": [1, 1, 2],
        "name": ["Alice", None, "Bob"],
        "price": [10, 10, 20]
    })
    cleaned = clean_data(df, "test_df")
    assert len(cleaned) == 3
    assert cleaned.iloc[0]["name"] == "Alice"
    assert all(cleaned["price"] > 0)

def test_clean_data_filters_out_negative_prices():
    df = pd.DataFrame({
        "id": [1, 2, 3],
        "price": [10, -5, 0]
    })
    cleaned = clean_data(df, "test_prices")
    assert len(cleaned) == 1
    assert cleaned["price"].iloc[0] == 10

def test_clean_data_raises_data_cleaning_error_on_exception():
    with patch("src.data_cleaner.logger") as mock_logger:
        df = None
        with pytest.raises(DataCleaningError):
            clean_data(df, "broken_df")
        mock_logger.exception.assert_called_once()

@patch("src.data_cleaner.pd.read_csv")
@patch("src.data_cleaner.clean_data")
@patch("src.data_cleaner.os.makedirs")
def test_main_success(mock_makedirs, mock_clean, mock_read_csv, tmp_path):
    df_mock = pd.DataFrame({"a": [1, 2]})
    mock_read_csv.return_value = df_mock
    mock_clean.return_value = df_mock

    class DummyConfig:
        CUSTOMERS_PATH = tmp_path / "customers.csv"
        PRODUCTS_PATH = tmp_path / "products.csv"
        SALES_PATH = tmp_path / "sales.csv"
        PROCESSED_DIR = tmp_path / "processed"
        CLEAN_CUSTOMERS_PATH = tmp_path / "processed" / "clean_customers.csv"
        CLEAN_PRODUCTS_PATH = tmp_path / "processed" / "clean_products.csv"
        CLEAN_SALES_PATH = tmp_path / "processed" / "clean_sales.csv"

    DummyConfig.PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    with patch("src.data_cleaner.Config", DummyConfig):
        main()

    assert mock_read_csv.call_count == 3
    assert mock_clean.call_count == 3
    mock_makedirs.assert_called_once()

@patch("src.data_cleaner.pd.read_csv", side_effect=Exception("File not found"))
def test_main_raises_data_cleaning_error_on_failure(mock_read_csv):
    with pytest.raises(DataCleaningError):
        main()
