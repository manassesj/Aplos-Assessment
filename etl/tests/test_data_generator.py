import pytest
import pandas as pd
from unittest.mock import patch
from src.data_generator import generate_customers, generate_products, generate_sales, DataGenerationError

def test_generate_customers_length():
    df = generate_customers(10)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 10
    assert all(col in df.columns for col in ["id", "name", "age", "region"])

def test_generate_products_length():
    df = generate_products(5)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 5
    assert all(col in df.columns for col in ["id", "category", "price", "supplier"])

def test_generate_sales_structure():
    customers = generate_customers(3)
    products = generate_products(3)
    df = generate_sales(customers, products, 6)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 6
    assert all(col in df.columns for col in ["id", "customer_id", "product_id", "date", "quantity"])
    assert df["customer_id"].isin(customers["id"]).all()
    assert df["product_id"].isin(products["id"]).all()

@patch("src.data_generator.pd.DataFrame.to_json")
@patch("src.data_generator.os.makedirs")
@patch("src.data_generator.logger")
def test_save_data_as_json(mock_logger, mock_makedirs, mock_to_json):
    df = pd.DataFrame({"id": [1, 2]})
    path = "dummy/path.json"
    from src.data_generator import save_data_as_json
    save_data_as_json(df, path)
    mock_makedirs.assert_called_once_with("dummy", exist_ok=True)
    mock_to_json.assert_called_once_with(path, orient="records", date_format="iso", indent=2)
    mock_logger.info.assert_called()

@patch("src.data_generator.save_data_as_json")
@patch("src.data_generator.generate_sales")
@patch("src.data_generator.generate_products")
@patch("src.data_generator.generate_customers")
@patch("src.data_generator.logger")
def test_main_success(mock_logger, mock_customers, mock_products, mock_sales, mock_save):
    mock_customers.return_value = pd.DataFrame({"id": [1]})
    mock_products.return_value = pd.DataFrame({"id": [1]})
    mock_sales.return_value = pd.DataFrame({"id": [1]})

    from src.data_generator import main
    main()

    assert mock_customers.called
    assert mock_products.called
    assert mock_sales.called
    assert mock_save.call_count == 3

    import pandas.testing as pdt
    calls = mock_save.call_args_list
    pdt.assert_frame_equal(calls[0].args[0], mock_customers.return_value)
    pdt.assert_frame_equal(calls[1].args[0], mock_products.return_value)
    pdt.assert_frame_equal(calls[2].args[0], mock_sales.return_value)

@patch("src.data_generator.generate_customers", side_effect=Exception("fail"))
def test_main_failure(mock_customers):
    from src.data_generator import main, DataGenerationError
    with pytest.raises(DataGenerationError):
        main()
