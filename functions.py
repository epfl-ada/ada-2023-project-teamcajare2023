import pandas as pd
import pycountry
import pycountry_convert as pc
import swifter

from functools import lru_cache


def convert_date(date_string):
    """
    Convert a date string to a pandas datetime object.

    Parameters:
    - date_string (str): The input date string to be converted.

    Returns:
    - pd.Timestamp: A pandas datetime object representing the converted date.

    Raises:
    - ValueError: If the input date string cannot be converted using any of the specified formats.
    """
    try:
        return pd.to_datetime(date_string, format='%Y-%m-%d')
    except ValueError:
        try:
            return pd.to_datetime(date_string, format='%Y-%m')
        except ValueError:
            try:
                return pd.to_datetime(date_string, format='%Y')
            except ValueError:
                return pd.to_datetime(date_string, format='%Y-%m-%d %H:%M:%S.%f')  
            
            
@lru_cache(maxsize=None)
def findCountry(country_name):
    """
    Find the ISO alpha-2 country code for a given country name.

    Parameters:
    - country_name (str): The name of the country.

    Returns:
    - str: The ISO alpha-2 country code if found, or 'not found' if the country is not found.
    """
    try:
        return pycountry.countries.search_fuzzy(country_name)[0].alpha_2
    except:
        return ('not found')
    

def bulkFindCountries(country_names):
    """
    Perform a bulk search to find ISO alpha-2 country codes for a list of country names.

    Parameters:
    - country_names (list): A list of country names.

    Returns:
    - list: A list of ISO alpha-2 country codes corresponding to the provided country names.
    """
    return [findCountry(name) for name in country_names]


def process_countries(countries):
    """
    Process a list of country codes, filtering out any occurrences of 'not found'.

    Parameters:
    - countries (list or str): A list of country codes or a single country code.

    Returns:
    - list or None: If input is a list, returns a filtered list with valid country codes.
                    If input is a single country code, returns the code of valid, else None.
                    If input is 'not found' or None, returns None.
    """
    if isinstance(countries, list):
        valid_countries = [country for country in countries if (country != 'not found')]
        return valid_countries if valid_countries else None
    else:
        return countries if countries != 'not found' else None


def percent_missing_strdict(data): 
    '''
    Count the number of missing values in a Series containing str-like dictionnaries
    
    Parameters:
    - data (pandas.core.series.Series): The input Series to count the missing values
    
    Returns:
    - float: The percentage of missing values in the Series
    '''
    N = len(data)
    missing_values = [1 if len(row) == 0 else 0 for i, row in enumerate(data)]
    percent_missing=(sum(missing_values)/N)*100
    return(percent_missing)