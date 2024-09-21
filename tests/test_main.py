from src import read_data


def test_read_data():
    df = read_data()
    assert df is not None
    assert len(df) > 0
    assert df.columns.tolist() == ["symbol", "date", "price_type", "price"]
