import os
import json
import pandas as pd
import pytest
from src.data_cleaner import clean_data, save_as_json, main
from src.config import Config
from src.utils.exceptions import DataCleaningError

@pytest.fixture
def sample_data():
    return pd.DataFrame({
        "id": [1, 2, 2, 3],
        "name": ["Alice", "Bob", "Bob", "Charlie"],
        "price": [10, 0, 0, 30],
        "quantity": [1, 2, 2, 3]
    })

def test_clean_data_removes_duplicates_and_invalid_prices(sample_data):
    cleaned = clean_data(sample_data, "test")
    # duplicates removed
    assert cleaned.shape[0] == 2
    # price > 0
    assert (cleaned["price"] > 0).all()

def test_save_as_json_creates_file(tmp_path, sample_data):
    path = tmp_path / "test.json"
    save_as_json(sample_data, str(path))
    assert os.path.exists(path)
    with open(path, "r") as f:
        lines = f.readlines()
        assert len(lines) == len(sample_data)

def test_main_creates_cleaned_json(tmp_path, monkeypatch):
    data = [{"id": 1, "name": "Alice", "price": 10, "quantity": 1}]
    customers_path = tmp_path / "customers.json"
    products_path = tmp_path / "products.json"
    sales_path = tmp_path / "sales.json"

    for path in [customers_path, products_path, sales_path]:
        with open(path, "w") as f:
            json.dump(data, f)

    monkeypatch.setattr(Config, "CUSTOMERS_PATH", str(customers_path))
    monkeypatch.setattr(Config, "PRODUCTS_PATH", str(products_path))
    monkeypatch.setattr(Config, "SALES_PATH", str(sales_path))
    monkeypatch.setattr(Config, "CLEAN_CUSTOMERS_PATH_JSON", str(tmp_path / "customers_clean.json"))
    monkeypatch.setattr(Config, "CLEAN_PRODUCTS_PATH_JSON", str(tmp_path / "products_clean.json"))
    monkeypatch.setattr(Config, "CLEAN_SALES_PATH_JSON", str(tmp_path / "sales_clean.json"))

    main()

    assert os.path.exists(Config.CLEAN_CUSTOMERS_PATH_JSON)
    assert os.path.exists(Config.CLEAN_PRODUCTS_PATH_JSON)
    assert os.path.exists(Config.CLEAN_SALES_PATH_JSON)

    for path in [Config.CLEAN_CUSTOMERS_PATH_JSON,
                 Config.CLEAN_PRODUCTS_PATH_JSON,
                 Config.CLEAN_SALES_PATH_JSON]:
        df = pd.read_json(path, lines=True)
        assert not df.empty
        assert (df["price"] > 0).all()
