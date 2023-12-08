import os 
import tarfile
import gzip
import urllib.request
import xml.etree.ElementTree as ET
from nltk.tree import Tree
import pandas as pd


# DATA PATH
current_directory = os.getcwd()
CORE_NLP_PATH = os.path.join(current_directory, 'corenlp')
CORE_NLP_GZ = CORE_NLP_PATH + "/corenlp_plot_summaries"
CORE_NLP_XML = CORE_NLP_PATH + "/corenlp_plot_summaries_xml"

# ------------------ Data loading ------------------ #

def load_corenlp_data(downloaded = True, tar_path = (CORE_NLP_PATH + "/corenlp_plot_summaries.tar")):
    """
    Load corenlp data from tar file indicated or downloads it from the web and puts all the files in xml format in a folder.
    
    param downloaded: boolean indicating if the data has been downloaded or not
    param tar_path: path to the tar file if downloaded is False
    """

    # Download data if not downloaded
    if not downloaded:
        coreNLP_filename = 'http://www.cs.cmu.edu/~ark/personas/data/corenlp_plot_summaries.tar'
        tar = tarfile.open(fileobj=urllib.request.urlopen(coreNLP_filename), mode="r") 
    else:
        tar = tarfile.open(tar_path, mode="r")

    tar.extractall(path=CORE_NLP_PATH) 
    tar.close()


    if not os.path.exists(CORE_NLP_XML):
        os.mkdir(CORE_NLP_XML)
        for filename in os.listdir(CORE_NLP_GZ):
            f = os.path.join(CORE_NLP_GZ, filename) 
            if os.path.isfile(f):
                # Open and store file as xml 
                with gzip.open(f, 'rb') as f_in:
                    gz_file = os.path.join(CORE_NLP_XML, filename)
                    with open(gz_file[:-3], 'wb') as f_out:
                        f_out.write(f_in.read())

# ------------------ Basic getters and printers ------------------ #

def get_movie_id(movie_xml):
    """
    Get the movie id from the movie xml file
    
    param movie_xml: path to the xml file
    return: movie id
    """
    return movie_xml.split('/')[-1].split('.')[0]


def get_tree(movie_xml, data_path = CORE_NLP_XML):
    """
    Get the tree from the movie xml file

    param movie_xml: path to the xml file
    param data_path: path to the folder containing the xml files
    return: xml tree
    """
    movie_path = os.path.join(data_path, movie_xml)
    tree = ET.parse(movie_path)
    return tree


def get_sentences(tree):
    """
    Get the CoreNLP parsed sentences from the tree

    param tree: xml tree
    return: list of sentences (string)
    """
    sentences = []
    for child in tree.iter():
        if child.tag == "parse":
            sentences.append(child.text)
    return sentences

def print_tree(sentence):
    """
    Print the tree of a sentence

    param sentence: parsed sentence to print (string)
    """
    tree = Tree.fromstring(sentence)
    tree.pretty_print()

# ------------------ Getters for character names ------------------ #

def get_characters(tree):
    """
    Get all of the characters in a movie from the xml tree. The characters are consecutive proper nouns (NNP) 
    with NER PERSON tags.
    
    param tree: xml tree
    return characters: list of characters
    """
    characters = []
    current_word = None
    is_proper_noun = False
    was_person = False
    character = ''
    for child in tree.iter():
        if child.tag == 'word':
            current_word = child.text
            is_proper_noun = True
        if child.tag == 'POS' and child.text == 'NNP':
            is_proper_noun = True
        if child.tag == 'NER' and child.text == 'PERSON' and is_proper_noun:
            if was_person: # Continue the character
                character += ' ' + current_word
            else: # Start the character
                character = current_word
                was_person = True
        if was_person and child.tag == 'POS' and child.text != 'NNP': # End the character
            characters.append(character)
            character = ''
            was_person = False
    return characters

def get_characters_from_xml(movie_xml, data_path = CORE_NLP_XML):
    """
    TO DO
    """

    return get_characters(get_tree(movie_xml, data_path))

def get_full_name(string, characters):
    ''' 
    Find the longest name of a given character in a list of character names. 

    param string: character name (partial or full)
    param characters: list of character names
    return full_name: longest name of character found in characters
    '''
    names = string.split(' ')
    max_length = 0
    for character in characters:
        char_names = character.split(' ')
        if set(names) <= set(char_names): 
            num_names = len(char_names)
            if num_names > max_length:
                max_length = num_names
                full_name = character
    return full_name

def get_full_names_dict(characters):
    """
    Get a dictionary mapping character names to their full names.

    param characters: list of character names
    return full_names_dict: dictionary mapping character names to their full names
    """
    
    full_names_dict = dict()
    for character in characters:
        full_name = get_full_name(character, characters)
        full_names_dict[character] = full_name
    return full_names_dict

def get_full_names_list(characters):
    """
    Get a list of the full names of the characters in a movie.

    param characters: list of character names
    return full_names: list of full names of the characters in a movie
    """

    full_names = []
    for character in characters:
        full_name = get_full_name(character, characters)
        if full_name not in full_names:
            full_names.append(full_name)
    return full_names

# ------------------ Processing number of mentions ------------------ #

def get_mentions(movie_xml, data_path = CORE_NLP_XML):
    """
    Get the number of times the character of a movie are mentioned in the plot summary.
    
    param movie_xml: path to the xml file
    return character_mentions: dictionary mapping characters to the number of times they are mentioned
    """

    tree = get_tree(movie_xml, data_path)
    characters = get_characters(tree)

    # get a dictionary mapping characters to the number of times they are mentioned
    character_mentions = dict()
    for character in characters:
        full_name = get_full_name(character, characters)
        if full_name in character_mentions:
            character_mentions[full_name] += 1
        else:
            character_mentions[full_name] = 1
    return character_mentions


def sort_by_mention(movie_xml, data_path = CORE_NLP_XML):
    """
    Sort the characters of a movie by the number of times they are mentioned in the plot summary.

    param movie_xml: path to the xml file
    return sorted_mentions: list of characters sorted by the number of times they are mentioned
    """

    character_mentions = get_mentions(movie_xml, data_path)
    sorted_mentions = sorted(character_mentions.items(), key=lambda x: x[1], reverse=True)
    return sorted_mentions


# the main character is defined as the most mentioned character in the plot summary
# this definition might not be sufficient
def get_main_character(movie_xml, data_path = CORE_NLP_XML):
    """
    Get the main character of a movie from the xml file

    param movie_xml: path to the xml file
    return: main character full name (string)
    """

    sorted_mentions = sort_by_mention(movie_xml, data_path)
    if len(sorted_mentions) == 0:
        return None 
    return sorted_mentions[0][0]

# ------------------ Extracting agent verbs, patient verbs and attributes ------------------ #

def get_verbs_noun_adjectives(movie_xml, data_path = CORE_NLP_XML):
    """
    Get the verbs, common nouns and adjectives in a movie plot from the xml file 
    containing the CoreNLP parsed sentences.

    param movie_xml: path to the xml file
    return: verbs (list), nouns (list)
    """

    verbs = []
    nouns = []
    adjectives = []
    tree = get_tree(movie_xml, data_path)
    for child in tree.iter():
        if child.tag == 'word':
            current_word = child.text
        if child.tag == "POS" and child.text.startswith('VB'):
            verbs.append(current_word)
        elif child.tag == "POS" and (child.text == 'NN' or child.text == 'NNS'):
            nouns.append(current_word)
        if child.tag == "POS" and child.text.startswith('JJ'):
            adjectives.append(current_word)
    
    return verbs, nouns, adjectives

def get_dependencies(movie_xml, data_path = CORE_NLP_XML):
    """
    Get the dependencies of a movie from the xml file containing the CoreNLP parsed sentences.

    param movie_xml: path to the xml file
    return: dependencies (list of tuples)
    """

    tree = get_tree(movie_xml, data_path)
    dependencies = []
    for child in tree.iter():
        if child.tag == 'collapsed-ccprocessed-dependencies':
            for dep in child:
                dependencies.append((dep[0].text, dep[1].text, dep.attrib['type']))
    return dependencies

def filter_dependencies(dependencies, characters):
    """ 
    Given a list of dependencies, filter out the ones that are not relevant to the list of characters.
    param dependencies: list of dependencies (tuples)
    param characters: dictionary mapping character names to their full names
    """

    character_governor_dependencies = []
    character_dependent_dependencies = []
    for dependency in dependencies:
        if dependency[0] in characters:
            full_name1 = characters[dependency[0]]
        else:
            full_name1 = None
        if dependency[1] in characters:
            full_name2 = characters[dependency[1]]
        else:
            full_name2 = None

        # keep dependencies that refer to only one character
        if full_name1 is not None and full_name2 is None:
            character_governor_dependencies.append((full_name1, dependency[1], dependency[2]))
        elif full_name1 is None and full_name2 is not None:
            character_dependent_dependencies.append((dependency[0], full_name2, dependency[2]))
    
    return character_governor_dependencies, character_dependent_dependencies

def get_verbs_attributes(character_governor_dependencies, character_dependent_dependencies,
                         verbs, nouns, adjectives):
    """
    Given the dependencies in a movie plot where characters are governors or dependents,
    get the agent verbs, patient verbs and attributes associated with each character.

    param character_governor_dependencies: list of dependencies where characters are governors
    param character_dependent_dependencies: list of dependencies where characters are dependents
    param verbs: list of verbs in the movie plot
    param nouns: list of nouns in the movie plot

    return agent_verbs: dictionary mapping characters to their agent verbs
    return patient_verbs: dictionary mapping characters to their patient verbs
    return attributes: dictionary mapping characters to their attributes
    """
        
    agent_verbs = dict()
    patient_verbs = dict()
    attributes = dict()

    # iterate through the dependencies where characters are dependents
    for dependency in character_dependent_dependencies:
        if (dependency[2] == "nsubj" or dependency[2] == "agent") and dependency[0] in verbs:
            if dependency[0] in agent_verbs:
                agent_verbs[dependency[1]].append(dependency[0])
            else:
                agent_verbs[dependency[1]] = [dependency[0]]
        
        elif (dependency[2] == "dobj" or dependency[2] == "nsubjpass" \
            or dependency[2] == "iobj" or dependency[2].startswith("prep_")) \
                and dependency[0] in verbs:
            if dependency[1] in patient_verbs:
                patient_verbs[dependency[1]].append(dependency[0])
            else:
                patient_verbs[dependency[1]] = [dependency[0]]
        
        elif (dependency[2] == "nsubj" or dependency[2] == "apppos") \
            and (dependency[0] in nouns or dependency[0] in adjectives):
            if dependency[1] in attributes:
                attributes[dependency[1]].append(dependency[0])
            else:
                attributes[dependency[1]] = [dependency[0]]

    # iterate through the dependencies where characters are governors
    for dependency in character_governor_dependencies:
        if (dependency[2] == "nsubj" or dependency[2] == "apppos" or  dependency[2] == "amod" \
            or dependency[2] == "nn") and (dependency[1] in nouns or dependency[1] in adjectives):
            if dependency[0] in attributes:
                attributes[dependency[0]].append(dependency[1])
            else:
                attributes[dependency[0]] = [dependency[1]]
    
    return agent_verbs, patient_verbs, attributes

def get_list_movie(movie_xml, data_path = CORE_NLP_XML):
    """
    Get a list containing the agent verbs, patient verbs and attributes of each character in a movie, 
    the number of mentions in the plot and whether they are the main character.

    param movie_xml: path to the xml file

    return: list of dictionaries containing the agent verbs, patient verbs and attributes of each character 
            in a movie and the movie id, the number of mentions in the plot and whether they are the main character.
    """

    tree = get_tree(movie_xml, data_path)
    movie_id = get_movie_id(movie_xml)

    characters = get_characters(tree)
    characters_list = get_full_names_list(characters)
    characters_dict = get_full_names_dict(characters)

    verbs, nouns, adjectives = get_verbs_noun_adjectives(movie_xml, data_path)

    dependencies = get_dependencies(movie_xml, data_path)
    character_governor_dependencies, character_dependent_dependencies = filter_dependencies(dependencies, characters_dict)
    agent_verbs, patient_verbs, attributes = get_verbs_attributes(character_governor_dependencies, 
                                                                  character_dependent_dependencies,
                                                                  verbs, nouns, adjectives)    
    
    mentions = get_mentions(movie_xml, data_path)
    main_char = get_main_character(movie_xml, data_path)

    lst = []
    for character in characters_list:
        if character in agent_verbs:
            agent_verbs_string = ', '.join(agent_verbs[character])
            agent_verbs_list = set(agent_verbs_string.split(",")) #set removes duplicates in the list
        else:
            agent_verbs_list = []
        if character in patient_verbs:
            patient_verbs_string = ', '.join(patient_verbs[character])
            patient_verbs_list = set(patient_verbs_string.split(","))
        else:
            patient_verbs_list = []
        if character in attributes:
            attributes_string = ', '.join(attributes[character])
            attributes_list = set(attributes_string.split(","))
        else:
            attributes_list = []
        
        lst.append({'WikiMovieID': movie_id,'CharacterName': character, 'Agent verbs': agent_verbs_list, 
                        'Patient verbs': patient_verbs_list, 'Attributes': attributes_list, 
                        'Mentions': mentions[character], 'MainCharacter': character == main_char})
        
    return lst

def get_df_movie(movie_xml, data_path = CORE_NLP_XML):
    """
    Get a dataframe containing the agent verbs, patient verbs and attributes of each character in a movie.

    param movie_xml: path to the xml file
    
    return: dataframe containing the agent verbs, patient verbs and attributes of each character 
            in a movie and the movie id.
    """
    
    lst = get_list_movie(movie_xml, data_path)
    df = pd.DataFrame(lst)
    return df