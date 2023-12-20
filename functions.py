import pandas as pd
import pycountry
import pycountry_convert as pc
import swifter
import networkx as nx

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

def exact_match(columns, row1, row2):
    """
    Check if two rows are an exact match on specified columns.

    Parameters:
    - columns (list): List of column names to consider for the match.
    - control_row (pd.Series): Row from the control group.
    - treatment_row (pd.Series): Row from the treatment group.

    Returns:
    - bool: True if the rows are an exact match on the specified columns, False otherwise.
    """

    for col in columns:
        if row1[col] != row2[col] :
            return False
    
    return True

def numpy_helper(df, cols):
    '''
    Convert a DataFrame with N rows and a list of M columns to a np.array of dimension (NxM).

    Parameters:
    - df (pd.DataFrame): Input DataFrame with N rows.
    - cols (list): List of column names to be included in the resulting array.

    Returns:
    - np.array: np.array of dimension (NxM).
    '''

    array = df[cols].to_numpy(copy = True, dtype= float) 
    return array

def find_main_char(cast):
    """
    Find the main character in the cast list based on the minimum cast_id.

    Parameters:
    - cast (list): A list of dictionaries representing the cast.

    Returns:
    - tuple: A tuple containing the main character details (character, actor, gender, cast_id).
    - None: If the input list is empty.
    """
    if not cast:
        return None
    
    # Find the minimum cast_id
    min_id = min(el['cast_id'] for el in cast)


    # Find the details of the main character with the minimum cast_id
    main_char, main_actor, main_gender, main_cast = next(
        (el['character'], el['name'], el['gender'], el['cast_id']) for el in cast if el['cast_id'] == min_id
    )

    return main_char, main_actor, main_gender, main_cast

def create_pairs (columns, df1, df2):
    """
    Create maximal matching pairs of rows from df1 and df2 based on the exact_match_columns.

    Parameters:
    - columns (list): List of column names to consider for the match.

    Returns:
    - pairs: A list of the paired rows, represented by their indexes in df1 and df2 respectively.
    """
    # Create an empty undirected graph
    G = nx.Graph()

    i = 0
    n = len(df1)
    # Loop through all the pairs of instances
    for df1_id, df1_row in df1.iterrows():
        i = i+1
        print(f'Row {i} out of {n}')
        for df2_id, df2_row in df2.iterrows():
        
            # Add an edge between the two instances if same track and same score before
            if exact_match(columns,  df1_row, df2_row):
                G.add_edge(df1_id, df2_id)

    print('loop finished')
    # Generate and return the maximum weight matching on the generated graph
    return nx.maximal_matching(G)

def create_bins_of_5_years(df):
   
    # Create bins for every 5 years starting from the minimum release year to the maximum release year
    min_year = int(df['ReleaseYear'].min())
    max_year = int(df['ReleaseYear'].max())
    bins = list(range(min_year, max_year + 6, 5))  # Adding 6 to include the upper bound

    # Create labels for the bins
    labels = [f'{start}-{start+4}' for start in bins[:-1]]

    # Use pd.cut to categorize release years into bins
    df['ReleaseYearBin'] = pd.cut(df['ReleaseYear'], bins=bins, labels=labels, include_lowest=True)
    return df