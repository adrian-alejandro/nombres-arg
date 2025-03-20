import pandas as pd
import re
from io import StringIO
import requests


def unicode_normalization(series: pd.Series) -> pd.Series:
    return series.str.normalize('NFKD').str.replace(r'[\u0300-\u036F]', '', regex=True)

def replace_text(text: str, replacement_patterns: dict) -> str:
    for pattern, replacement in replacement_patterns.items():
        text = pattern.sub(replacement, text)
    return text

def pull_data_from_url(url: str, usecols=None) -> pd.DataFrame:
    """Function that pulls data from a URL.
    The optional argument usecols is for fetching only the necessary columns, as not 
    all columns may be needed for the analysis and they impact in processing time. 
    """
    try:
        data = pd.read_csv(url, usecols=usecols)
    except:
        response = requests.get(url, verify=False)
        data = StringIO(response.text)
        data = pd.read_csv(data, usecols=usecols)
    return data

def clean_column(data: pd.DataFrame, col_name: str, split: bool = False):
    # Drop NAs
    data = data.dropna()
    # Keep original column
    data[f"{col_name}_original"] = data[col_name]
    # Unicode normalization & lower for standardization
    data[col_name] = unicode_normalization(data[col_name]).str.lower()
    # Context-sensitive replacements of characters
    context_replacements = {
        # Undefined character ¤
        r'(?<=[e])¤(?=[u])': 's',
        r'(?<=[aeiou])¤(?=[aeiou])': 'ñ',
        r'(?<=[n])¤(?=[o])': 'i',
        r'(?<=[i])¤$': 'a',
        # Undefined character ?
        r'(?<=[lr])¤(?=[aeiou]|$)': '',
        r'(?<=[v])\?(?=[n])': 'a',
        r'(?<=[ltm])\?(?=[n]|$)': 'i',
        # Undefined character £
        r'(?<=[as])£(?=[ls])': 'u',
        # Special character °
        r'(?<=[a-z])°$': '',
        r'(?<=[1-9]) °$': '°',
        # Special cases with numbers between letters:
        r'o0\b': 'o',
        r'(?<=[a-z])[03](?=[a-z]|$)': 'o', 
        r'0(?=[a-z])': 'o',
        r'(?<=[a-z])1(?=[a-z]|$)': 'i',
        r'(?<=[a-z])[389](?=[a-z]|$)': '',
        r'(?<=[0-9])o$': '°'
    }
    context_replacements = {re.compile(k): v for k, v in context_replacements.items()}
    data[col_name] = data[col_name].apply(lambda x: replace_text(x, context_replacements))

    # Direct replacement of special characters (including ¤, ?, £)
    direct_replacements = {
        '¡': 'i', '\x82': 'e', '¢': 'o', 'ύ': 'u', 'υ': 'u', 'µ': 'a',
        '¤': 'a',  '£': 'e', r'\?': 'e'
    }
    direct_replacements = {re.compile(k): v for k, v in direct_replacements.items()}
    data[col_name] = data[col_name].apply(lambda x: replace_text(x, direct_replacements))

    # Remove other unwanted characters: .|_`: \xad { " \x90 \t ~
    pattern = re.compile(r'[.|_`:/{·\+~\xad\x90\t¤"]')
    data[col_name] = data[col_name].str.replace(pattern, '',regex=True)
    
    # Remove commas from names (longer cases correspond to two names))
    remove_commas = lambda x: x.replace(',', '') if len(x) < 10 else x.replace(',', ' ')
    data[col_name] = data[col_name].apply(remove_commas)
    
    # Split and explode compound names
    if split:
       # First three splits remove registry comments/remarks
       # Last split breaks compound name into its constituents
       data[col_name] = data[col_name].astype(str).str.split('(').str[0]\
                                                .str.split('Presunto').str[0]\
                                                .str.split('Fallecido').str[0]\
                                                .str.split(' ')
       data = data.explode(col_name).reset_index(drop=True)
    
    # Remove leading & trailing spaces, commas and hyphens
    data[col_name] = data[col_name].str.strip()\
                                    .str.strip(',')\
                                    .str.strip("'")\
                                    .str.strip("-")
    
    # Replace empty rows with NA and drop NAs
    data[col_name] = data[col_name].apply(lambda x: None if x == '' else x, 1)
    data.dropna(inplace=True)

    # Return unique values and data
    return (data[col_name].unique().tolist(), data)
