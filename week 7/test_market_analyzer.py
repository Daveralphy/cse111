import pytest
import pandas as pd
from os import path
from market_analyzer import read_market_data, calculate_statistics

CSV_FILE = path.join(path.dirname(__file__), "producer-prices-nga.csv")

def test_read_market_data():
    """Test that the CSV file is read correctly into a DataFrame."""
    df = read_market_data(CSV_FILE)
    assert isinstance(df, pd.DataFrame), "read_market_data must return a pandas DataFrame."
    assert len(df) > 0, "DataFrame should not be empty."
    expected_cols = ['date', 'commodity', 'price', 'unit']
    for col in expected_cols:
        assert col in df.columns, f"Missing column: {col}"

def test_calculate_statistics():
    """Test that statistics are calculated correctly."""
    df = read_market_data(CSV_FILE)
    sample = df.head(3)
    stats = calculate_statistics(sample)
    assert isinstance(stats, pd.Series), "calculate_statistics must return a pandas Series."
    assert 'count' in stats.index and 'mean' in stats.index, "Statistics must include count and mean."
    assert stats['count'] == 3, f"Expected 3 rows, got {stats['count']}."

def test_missing_price_column():
    """Test that function handles missing 'price' column properly."""
    df = pd.DataFrame({'commodity': ['Rice', 'Beans']})
    stats = calculate_statistics(df)
    assert isinstance(stats, pd.DataFrame), "When 'price' is missing, must return an empty DataFrame."
    assert stats.empty, "Expected empty DataFrame when 'price' column is missing."

if __name__ == "__main__":
    pytest.main(["-v", "--tb=line", "-rN", __file__])