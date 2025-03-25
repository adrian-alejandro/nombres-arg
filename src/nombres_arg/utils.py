import pandas as pd
import re
from io import StringIO
import requests
import functools
from spacy.lang.es.stop_words import STOP_WORDS


def suppress_pandas_warning(func):
    """Decorator to temporarily suppress SettingWithCopyWarning in Pandas."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        with pd.option_context("mode.chained_assignment", None):
            return func(*args, **kwargs)
    return wrapper

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

@suppress_pandas_warning
def clean_column(data: pd.DataFrame, col_name: str, split: bool = False) -> tuple:
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
        r'(^|(?<=[a-z]))1(?=[a-z]|$)': 'i',
        r'(?<=[a-z])[0-9](?=[a-z]|$)': '',
        r'(?<=[0-9])o$': '°'
    }
    context_replacements = {re.compile(k): v for k, v in context_replacements.items()}
    data[col_name] = data[col_name].apply(lambda x: replace_text(x, context_replacements))

    # Direct replacement of special characters (including ¤, ?, £)
    direct_replacements = {
        '¡': 'i', '\x82': 'e', '¢': 'o', 'ύ': 'u', 'υ': 'u', 'µ': 'a', 'μ': 'a',
        '¤': 'a',  '£': 'e', r'\?': 'e', '2°': 'segundo'
    }
    direct_replacements = {re.compile(k): v for k, v in direct_replacements.items()}
    data[col_name] = data[col_name].apply(lambda x: replace_text(x, direct_replacements))

    # Remove other unwanted characters: .|_`: \xad { " \x90 \t ~
    pattern = re.compile(r'[.|_`:/{·+~\xad\x90\t¤"¿!]')
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
    
    # Remove words that are entirely non-alphabetic or numbers
    data[col_name] = data[col_name].str.replace(re.compile(r'^\W+$|^\d+$'), '', regex=True)

    # Remove stopwords and uni-character
    # It's not very thorough so it may need revision
    filter_sw = lambda x: ~((x.str.len() < 2) | (x.str.len() == 2) & (x.isin(STOP_WORDS)))
    data[col_name] = data[filter_sw(data[col_name])][col_name]

    # Drop NAs
    data.dropna(inplace=True)

    # Return unique values and data
    return (data[col_name].unique().tolist(), data)
