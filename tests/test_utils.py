import pytest
import pandas as pd
from nombres_arg.utils import clean_column

def test_clean_column_basic():
    """Test basic text normalization and cleaning."""
    df = pd.DataFrame({"name": ["Jöhn", "María!", "PÉREZ ", "luc¡a"]})

    cleaned_names, data = clean_column(df, "name", split=False)

    assert isinstance(cleaned_names, list) # Ensure the first output is a list
    assert isinstance(data, pd.DataFrame) # Ensure the second output is a Pandas DataFrame
    assert "john" in cleaned_names  # Ensure Unicode normalization works
    assert "maria" in cleaned_names  # Ensure special character removal
    assert "perez" in cleaned_names  # Ensure spaces are stripped
    assert "lucia" in cleaned_names  # Ensure special character replacement
