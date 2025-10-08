import pytest
from unittest.mock import patch

@patch("src.main.run_metrics_computation")
@patch("src.main.run_data_cleaning")
@patch("src.main.run_data_generation")
@patch("src.main.logger")
def test_run_pipeline_success(mock_logger, mock_generate, mock_clean, mock_metrics):
    from src.main import run_pipeline

    run_pipeline()

    mock_generate.assert_called_once()
    mock_clean.assert_called_once()
    mock_metrics.assert_called_once()
    assert mock_logger.info.call_count == 2

@patch("src.main.run_metrics_computation")
@patch("src.main.run_data_cleaning")
@patch("src.main.run_data_generation", side_effect=Exception("Generation failed"))
@patch("src.main.logger")
def test_run_pipeline_generation_failure(mock_logger, mock_generate, mock_clean, mock_metrics):
    from src.main import run_pipeline
    with pytest.raises(SystemExit) as e:
        run_pipeline()
    assert e.type == SystemExit
    assert e.value.code == 1
    mock_generate.assert_called_once()
    mock_clean.assert_not_called()
    mock_metrics.assert_not_called()
    assert mock_logger.exception.called

@patch("src.main.run_metrics_computation")
@patch("src.main.run_data_cleaning", side_effect=Exception("Cleaning failed"))
@patch("src.main.run_data_generation")
@patch("src.main.logger")
def test_run_pipeline_cleaning_failure(mock_logger, mock_generate, mock_clean, mock_metrics):
    from src.main import run_pipeline
    with pytest.raises(SystemExit) as e:
        run_pipeline()
    assert e.type == SystemExit
    assert e.value.code == 1
    mock_generate.assert_called_once()
    mock_clean.assert_called_once()
    mock_metrics.assert_not_called()
    assert mock_logger.exception.called

@patch("src.main.run_metrics_computation", side_effect=Exception("Metrics failed"))
@patch("src.main.run_data_cleaning")
@patch("src.main.run_data_generation")
@patch("src.main.logger")
def test_run_pipeline_metrics_failure(mock_logger, mock_generate, mock_clean, mock_metrics):
    from src.main import run_pipeline
    with pytest.raises(SystemExit) as e:
        run_pipeline()
    assert e.type == SystemExit
    assert e.value.code == 1
    mock_generate.assert_called_once()
    mock_clean.assert_called_once()
    mock_metrics.assert_called_once()
    assert mock_logger.exception.called
