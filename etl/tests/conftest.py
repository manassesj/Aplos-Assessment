import pytest
import pandas as pd
from pathlib import Path

@pytest.fixture
def sample_raw_data():
    return pd.DataFrame({
        "id": [1, 2, 3, None],
        "value": [10, None, 30, 40],
        "category": ["A", "B", "B", None]
    })

@pytest.fixture
def tmp_processed_dir(tmp_path):
    path = tmp_path / "processed"
    path.mkdir()
    return path
