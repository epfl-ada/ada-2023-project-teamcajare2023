import pandas as pd
import pycountry
import pycountry_convert as pc
import swifter
import networkx as nx
import numpy as np
import plotly.graph_objects as go
from scipy import stats
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import spacy
nlp = spacy.load("en_core_web_lg")


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


def add_p_value_annotation(fig, array_columns, subplot=None, _format=dict(interline=0.07, text_height=1.07, color='black')):
    ''' Adds notations giving the p-value between two box plot data (t-test two-sided comparison)
    
    Parameters:
    ----------
    fig: figure
        plotly boxplot figure
    array_columns: np.array
        array of which columns to compare 
        e.g.: [[0,1], [1,2]] compares column 0 with 1 and 1 with 2
    subplot: None or int
        specifies if the figures has subplots and what subplot to add the notation to
    _format: dict
        format characteristics for the lines

    Returns:
    -------
    fig: figure
        figure with the added notation
    '''
    # Specify in what y_range to plot for each pair of columns
    y_range = np.zeros([len(array_columns), 2])
    for i in range(len(array_columns)):
        y_range[i] = [1.01+i*_format['interline'], 1.02+i*_format['interline']]

    # Get values from figure
    fig_dict = fig.to_dict()

    # Get indices if working with subplots
    if subplot:
        if subplot == 1:
            subplot_str = ''
        else:
            subplot_str =str(subplot)
        indices = [] #Change the box index to the indices of the data for that subplot
        for index, data in enumerate(fig_dict['data']):
            #print(index, data['xaxis'], 'x' + subplot_str)
            if data['xaxis'] == 'x' + subplot_str:
                indices = np.append(indices, index)
        indices = [int(i) for i in indices]
        print((indices))
    else:
        subplot_str = ''

    # Print the p-values
    for index, column_pair in enumerate(array_columns):
        if subplot:
            data_pair = [indices[column_pair[0]], indices[column_pair[1]]]
        else:
            data_pair = column_pair

        # Mare sure it is selecting the data and subplot you want
        #print('0:', fig_dict['data'][data_pair[0]]['name'], fig_dict['data'][data_pair[0]]['xaxis'])
        #print('1:', fig_dict['data'][data_pair[1]]['name'], fig_dict['data'][data_pair[1]]['xaxis'])

        # Get the p-value
        pvalue = stats.ttest_ind(
            fig_dict['data'][data_pair[0]]['y'],
            fig_dict['data'][data_pair[1]]['y'],
            equal_var=False,
        )[1]
        if pvalue >= 0.05:
            symbol = 'ns'
        elif pvalue >= 0.01: 
            symbol = '*'
        elif pvalue >= 0.001:
            symbol = '**'
        else:
            symbol = '***'
        # Vertical line
        fig.add_shape(type="line",
            xref="x"+subplot_str, yref="y"+subplot_str+" domain",
            x0=column_pair[0], y0=y_range[index][0], 
            x1=column_pair[0], y1=y_range[index][1],
            line=dict(color=_format['color'], width=2,)
        )
        # Horizontal line
        fig.add_shape(type="line",
            xref="x"+subplot_str, yref="y"+subplot_str+" domain",
            x0=column_pair[0], y0=y_range[index][1], 
            x1=column_pair[1], y1=y_range[index][1],
            line=dict(color=_format['color'], width=2,)
        )
        # Vertical line
        fig.add_shape(type="line",
            xref="x"+subplot_str, yref="y"+subplot_str+" domain",
            x0=column_pair[1], y0=y_range[index][0], 
            x1=column_pair[1], y1=y_range[index][1],
            line=dict(color=_format['color'], width=2,)
        )
        ## add text at the correct x, y coordinates
        ## for bars, there is a direct mapping from the bar number to 0, 1, 2...
        fig.add_annotation(dict(font=dict(color=_format['color'],size=14),
            x=(column_pair[0] + column_pair[1])/2,
            y=y_range[index][1]*_format['text_height'],
            showarrow=False,
            text=symbol,
            textangle=0,
            xref="x"+subplot_str,
            yref="y"+subplot_str+" domain"
        ))
    return fig

def create_wordcloud(cluster, clusters_df, colormap):
    '''
    Plot wordclouds showing the most frequent words in each category for the given cluster number.
    param cluster: the cluster number
    '''

    agent_verbs = clusters_df[clusters_df["cluster"] == cluster]['Agent verbs'].tolist()
    agent_verbs = [item for sublist in agent_verbs for item in sublist]
    agent_verbs_lemma = [nlp(verb)[0].lemma_ for verb in agent_verbs]

    patient_verbs = clusters_df[clusters_df["cluster"] == cluster]['Patient verbs'].tolist()
    patient_verbs = [item for sublist in patient_verbs for item in sublist]
    patient_verbs_lemma = [nlp(verb)[0].lemma_ for verb in patient_verbs]

    attributes = clusters_df[clusters_df["cluster"] == cluster]['Attributes'].tolist()
    attributes = [item for sublist in attributes for item in sublist]
    attributes_lemma = [nlp(attribute)[0].lemma_ for attribute in attributes]

    # create wordclouds for each category
    agent_verbs_cloud = WordCloud(background_color="white", max_words=100, width=800, height=400, colormap=colormap).generate(' '.join(agent_verbs_lemma))
    patient_verbs_cloud = WordCloud(background_color="white", max_words=100, width=800, height=400, colormap=colormap).generate(' '.join(patient_verbs_lemma))
    attributes_cloud = WordCloud(background_color="white", max_words=100, width=800, height=400, colormap=colormap).generate(' '.join(attributes_lemma))

    # Plotting the WordClouds
    plt.figure(figsize=(12, 6))

    plt.suptitle(('Cluster ' + str(cluster)), fontsize=20)

    plt.subplot(3, 1, 1)
    plt.imshow(agent_verbs_cloud, interpolation='bilinear')
    plt.title('Agent verbs', color='black', fontsize=16)
    plt.axis('off')

    plt.subplot(3, 1, 2)
    plt.imshow(patient_verbs_cloud, interpolation='bilinear')
    plt.title('Patient verbs', color='black', fontsize=16)
    plt.axis('off')

    plt.subplot(3, 1, 3)
    plt.imshow(attributes_cloud, interpolation='bilinear')
    plt.title('Attributes', color='black', fontsize=16)
    plt.axis('off')

    plt.show()

def create_corrected_wordcloud(cluster, clusters_df, outliers_agent_verbs, outliers_patient_verbs, outliers_attributes, colormap):
    '''
    Plot wordclouds showing the most frequent words in each category for the given cluster number.
    The wordclouds are corrected in the sense that we remove the "general" words that appear very frequently in each category 
    to focus on the words that are more specific to the cluster.
    param cluster: the cluster number
    '''
    
    agent_verbs = clusters_df[clusters_df["cluster"] == cluster]['Agent verbs'].tolist()
    agent_verbs = [item for sublist in agent_verbs for item in sublist]
    agent_verbs = [word for word in agent_verbs if word not in outliers_agent_verbs]
    agent_verbs_lemma = [nlp(verb)[0].lemma_ for verb in agent_verbs]
    agent_verbs_lemma = [word for word in agent_verbs_lemma if word not in outliers_agent_verbs]

    patient_verbs = clusters_df[clusters_df["cluster"] == cluster]['Patient verbs'].tolist()
    patient_verbs = [item for sublist in patient_verbs for item in sublist]
    patient_verbs_lemma = [nlp(verb)[0].lemma_ for verb in patient_verbs]
    patient_verbs_lemma = [word for word in patient_verbs_lemma if word not in outliers_patient_verbs]

    attributes = clusters_df[clusters_df["cluster"] == cluster]['Attributes'].tolist()
    attributes = [item for sublist in attributes for item in sublist]
    attributes_lemma = [nlp(attribute)[0].lemma_ for attribute in attributes]
    attributes_lemma = [word for word in attributes_lemma if word not in outliers_attributes]

    # create wordclouds for each category
    agent_verbs_cloud = WordCloud(background_color="white", max_words=100, width=800, height=400, colormap=colormap).generate(' '.join(agent_verbs_lemma))
    patient_verbs_cloud = WordCloud(background_color="white", max_words=100, width=800, height=400, colormap=colormap).generate(' '.join(patient_verbs_lemma))
    attributes_cloud = WordCloud(background_color="white", max_words=100, width=800, height=400, colormap=colormap).generate(' '.join(attributes_lemma))

    # Plotting the WordClouds
    plt.figure(figsize=(12, 6))

    plt.suptitle(('Cluster ' + str(cluster)), fontsize=20)

    plt.subplot(3, 1, 1)
    plt.imshow(agent_verbs_cloud, interpolation='bilinear')
    plt.title('Agent verbs', color='black', fontsize=16)
    plt.axis('off')

    plt.subplot(3, 1, 2)
    plt.imshow(patient_verbs_cloud, interpolation='bilinear')
    plt.title('Patient verbs', color='black', fontsize=16)
    plt.axis('off')

    plt.subplot(3, 1, 3)
    plt.imshow(attributes_cloud, interpolation='bilinear')
    plt.title('Attributes', color='black', fontsize=16)
    plt.axis('off')

    plt.show()
