import sys
import os
import pytest
import pandas as pd

# Add the project root to sys.path so pytest can find src/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

# TEST MODULE-LEVEL CONSTANTS
# Import the constants from data_loader
from nombres_arg import NAMES, LASTNAMES

def test_names():
    assert isinstance(NAMES, list)  # Ensure it's a list
    assert len(NAMES) > 0  # Ensure it has data

def test_lastnames():
    assert isinstance(LASTNAMES, list)  # Ensure it's a list
    assert len(LASTNAMES) > 0  # Ensure it has data

# TEST LOAD FUNCTION
# Import the load function and the 
from nombres_arg.data_loader import _load_csv_as_list

def test_load_csv_as_list():
    """Test if _load_csv_as_list correctly loads a CSV file as a list."""
    sample_data = ["Juan", "Luis", "Alicia", "Maria"]
    
    # Create a temporary CSV file
    test_file = "test_names.csv"
    pd.Series(sample_data).to_csv(test_file, index=False, header=False)

    # Load it using _load_csv_as_list
    loaded_data = _load_csv_as_list(test_file)

    assert isinstance(loaded_data, list)
    assert loaded_data == sample_data  # Ensure contents match

    # Cleanup
    os.remove(test_file)
