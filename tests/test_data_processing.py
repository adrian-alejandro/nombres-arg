import pytest
import pandas as pd
from nombres_arg.data_processing import NameDataProcessor
from nombres_arg.config import NAMES_COLUMN, LASTNAMES_COLUMN

def test_process_data():
    """Test if NameDataProcessor correctly processes names and last names."""
    processor = NameDataProcessor()

    # Create sample DataFrames
    processor.names_data = pd.DataFrame({NAMES_COLUMN: ["Juän", "Ana", "Carl0s"]})
    processor.lastnames_data = pd.DataFrame({LASTNAMES_COLUMN: ["Gómez", "Pérez ", "Férnandez"]})

    # Run processing
    processor.process_data()

    assert isinstance(processor.unique_names, pd.Series) # Ensure unique names is a Pandas Series
    assert isinstance(processor.unique_lastnames, pd.Series) # Ensure unique lastnames is a Pandas Series
    assert "juan" in processor.unique_names.tolist()  # Check normalization
