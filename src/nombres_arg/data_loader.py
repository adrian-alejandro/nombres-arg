import os
import pandas as pd
from .config import NAMES_EXPORT, LASTNAMES_EXPORT

def _load_csv_as_list(filepath: str) -> list:
    """Helper function to load a CSV file as a list."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Processed data file not found: {filepath}")
    return pd.read_csv(filepath, header=None).squeeze().dropna().tolist()

# Preloaded constants
NAMES = _load_csv_as_list(NAMES_EXPORT)
LASTNAMES = _load_csv_as_list(LASTNAMES_EXPORT)
