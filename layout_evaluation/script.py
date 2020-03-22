#!/usr/bin/python3

import os
import re
import sys
import pandas as pd
from io import StringIO
import matplotlib.pyplot as plt


def main():
    # load the blocks from config.txt and parse them into dataframes
    df_layouts, df_keys, df_bigrams, df_penalties = parse_config(load_config())

    # as some letters are not present in all layouts, they can be manually removed from the bigrams list
    letters_to_ignore = 'êàçâîô/äñößü'
    # iterate over the dataframe to remove the letters
    for row in df_bigrams.itertuples():
        drop = False
        for c in letters_to_ignore:
            if str(c) in row.Index:
                drop = True
        if drop:
            df_bigrams = df_bigrams.drop(row.Index)
    
    # this prints letters present in bigrams but not in a layout
    # letters absent from a layout do not count in the grade
    # differences between layouts skew the results
    df_missing_letters = check_missing_letters(df_layouts, df_bigrams)
    if 'Missing letters' in df_missing_letters:
        print('Some letters are missing from some layouts, skewing the results:')
        print(df_missing_letters)
    
    # generate a dataframe of the weights per bigram per layout
    df_bigram_weight = bigram_weight(df_layouts, df_keys, df_bigrams, df_penalties)
    
    # get the results
    df_results = layout_results(df_bigrams, df_bigram_weight)

    # add average column with arbitrary coefs per language
    # df_results['Personal average'] = df_results.en * 0.5 + df_results.fr * 0.3 + df_results.es * 0.2

    # sort the results
    df_results = df_results.sort_values(by=['en'], ascending=True)

    # remove results from personal corpus, they are only for comparison and clutter the results
    del df_results['en_perso']
    del df_results['fr_perso']

    print(df_results)
    
    # to plot with pandas
    plt.style.use('ggplot') # seaborn-whitegrid or ggplot
    df_results.plot(kind='bar', title='Grades per layout (lower is better)', figsize=(12,8), rot=45, width=0.8)
    plt.show()


def load_config():
    """
    Load the config file and outputs its content as a list of tuples (title, block)
    """
    
    # load the whole file into a str
    filepath = os.path.join(os.path.dirname(os.path.realpath('__file__')), 'config.txt')
    filehandle = open(filepath)
    filetext = filehandle.read()
    
    # remove the comments from the file
    filetext = removeComments(filetext)
    
    # find all the paragraphs
    parts = re.findall(r'\[(.*?)\]', filetext)
    
    # to cut into blocks
    parts_location = []
    blocks = []
    # find the paragraphs location, put it in a tuple (start, end) of title
    for t in parts:
        part_location = filetext.find('[' + t + ']')
        parts_location.append((part_location, filetext.find('\n', part_location) + 1))
    # put paragraphs into blocks list
    for i in range(len(parts_location)):
        if i < len(parts_location) - 1:
            blocks.append(filetext[parts_location[i][1]:parts_location[i + 1][0]])
        else:
            blocks.append(filetext[parts_location[i][1]:])
    
    # remove blank lines from the blocks
    for i in range(len(blocks)):
        blocks[i] = os.linesep.join([s for s in blocks[i].splitlines() if s])
    
    # return the blocks
    output = []
    for i in range(len(blocks)):
        output.append((parts[i], blocks[i]))
    return output


def parse_config(blocks):
    """
    Takes the list of tuples (title, block), and outputs the dataframes
    """
    
    # check that all the needed configuration is present
    blocks_needed = ['keys', 'weights', 'penalties', 'layouts']
    blocks_available = []
    for t in blocks:
        blocks_available.append(t[0])
    for t in blocks_needed:
        if t not in blocks_available:
            print('Missing block from config file: ' + t)
            sys.exit()
    
    # find the location of the keys in the blocks list
    for i in range(len(blocks)):
        if blocks[i][0] == 'keys':
            break
    # create list of keys
    keys = blocks[i][1].split()
    
    # find the location of the weights in the blocks list
    for i in range(len(blocks)):
        if blocks[i][0] == 'weights':
            break
    # convert weights to float
    weights_list = blocks[i][1].split()
    weights_list = [float(num) for num in weights_list]
    # create DataFrame of key weights
    df_keys = pd.DataFrame(weights_list, index=keys, columns=['weights'])
    # add columns finger and row
    df_keys['finger'] = None
    df_keys['keyrow'] = None
    # assign a letter per key corresponding to which finger is used
    for row in df_keys.itertuples():
        # pinky
        if row.Index[1:] in ['01', '02', '08', '09', '15', '16', '22', '23']:
            df_keys.at[row.Index, 'finger'] = 'p'
        # ring
        elif row.Index[1:] in ['03', '10', '17', '24']:
            df_keys.at[row.Index, 'finger'] = 'r'
        # middle
        elif row.Index[1:] in ['04', '11', '18', '25']:
            df_keys.at[row.Index, 'finger'] = 'm'
        # index
        elif row.Index[1:] in ['05', '06', '07', '12', '13', '14', '19', '20', '21', '26', '27', '28']:
            df_keys.at[row.Index, 'finger'] = 'i'
    # assign a number per key corresponding to which row it is
    for row in df_keys.itertuples():
        if row.Index[1:] in ['01', '02', '03', '04', '05', '06', '07']:
            df_keys.at[row.Index, 'keyrow'] = 1
        elif row.Index[1:] in ['08', '09', '10', '11', '12', '13', '14']:
            df_keys.at[row.Index, 'keyrow'] = 2
        elif row.Index[1:] in ['15', '16', '17', '18', '19', '20', '21']:
            df_keys.at[row.Index, 'keyrow'] = 3
        elif row.Index[1:] in ['22', '23', '24', '25', '26', '27', '28']:
            df_keys.at[row.Index, 'keyrow'] = 4
    # df_keys is a dataframe of the keys definition (base weight, finger, and row)

    # find the location of the layouts in the blocks list
    for i in range(len(blocks)):
        if blocks[i][0] == 'layouts':
            break
    # create DataFrame of layouts
    df_layouts = create_df_layouts(keys, blocks[i][1])
    # df_layouts is a dataframe of all predefined layouts to evaluate
    
    # dataframe of bigrams by language
    df_bigrams = pd.read_csv(os.path.join(os.path.dirname(os.path.realpath('__file__')), 'stats.csv'), header=0, sep=',', index_col=0)
    # df_bigrams is a dataframe of all possible bigrams (aa, ab…) with their probability per language

    # find the location of the penalties in the blocks list
    for i in range(len(blocks)):
        if blocks[i][0] == 'penalties':
            break
    df_penalties = pd.read_csv(StringIO(blocks[i][1]), sep=',', header=0, index_col=0, skipinitialspace=True)
    # df_penalties is a dataframe of the penalties to add to bigrams, by finger and row jump

    return df_layouts, df_keys, df_bigrams, df_penalties


def check_missing_letters(df_layouts, df_bigrams):
    """
    Return a list of letters present in bigrams but missing from each layout
    """
    # create empty dataframe
    df_missing_letters = pd.DataFrame(index=df_layouts.keys())
    
    # get the list of bigrams
    bigram_list = list(df_bigrams.index.values)
    # iterate to compile list of letters
    letters_list = []
    for i in bigram_list:
        if i[0] not in letters_list:
            letters_list.append(i[0])
        if i[1] not in letters_list:
            letters_list.append(i[1])
    
    # iterate over the layouts
    for layout in df_missing_letters.itertuples():
        # iterate over letters
        missing_letters = ""
        for i in letters_list:
            if i not in df_layouts[layout.Index].values:
                missing_letters = missing_letters + i
        if missing_letters != '':
            df_missing_letters.at[layout.Index, 'Missing letters'] = missing_letters
    
    return df_missing_letters

def create_df_layouts(keys_list, layouts_str):
    """ Takes keys and layouts string and outputs DataFrame of layouts"""
    # cuts the text into blocks by >>
    data = list(filter(None, layouts_str.split('>>')))
    # puts names and layouts in 2 lists
    layouts_names = []
    layouts_list = []
    for t in data:
        splitted = t.split('\n', maxsplit=1)
        layouts_names.append(splitted[0])
        layouts_list.append(splitted[1].split())
    # create the dataframe
    return pd.DataFrame(list(zip(*layouts_list)), index=keys_list, columns=layouts_names)


def weight(bigram, layout, df_layouts, df_keys, df_penalties):
    """
    Returns the calculated weight of a bigram, for a given layout
    """
    
    # check that the bigram keys exist in the layout, otherwise return 0
    if (bigram[0] not in df_layouts[layout].values) or (bigram[1] not in df_layouts[layout].values):
        return 0.0

    # find the keys of each letter
    key1 = df_layouts.loc[df_layouts[layout] == bigram[0]].index[0]
    key2 = df_layouts.loc[df_layouts[layout] == bigram[1]].index[0]
    # get the weights, fingers, and keyrows
    weight1 = df_keys.at[key1, 'weights']
    finger1 = df_keys.at[key1, 'finger']
    keyrow1 = df_keys.at[key1, 'keyrow']
    weight2 = df_keys.at[key2, 'weights']
    finger2 = df_keys.at[key2, 'finger']
    keyrow2 = df_keys.at[key2, 'keyrow']

    # penalty exists only if same hand, and not same letter
    penalty = 0.0
    if (key1[0] == key2[0]) and (bigram[0] != bigram[1]):
        # define the row jump (column name in df_penalties)
        if(abs(keyrow1 - keyrow2) == 0):
            rowjump = "same_row"
        elif(abs(keyrow1 - keyrow2) == 1):
            rowjump = "row_jump1"
        elif(abs(keyrow1 - keyrow2) == 2):
            rowjump = "row_jump2"
        else:
            sys.exit('Penalty for line jump not defined')
        
        penalty = df_penalties.at[finger1 + finger2, rowjump]
    
    return weight1 + weight2 + penalty


def bigram_weight(df_layouts, df_keys, df_bigrams, df_penalties):
    """
    Create a dafaframe of the weight per bigram and layout
    """
    # create the empty dataframe
    df_bigram_weight = pd.DataFrame(index=df_bigrams.index.values, columns=df_layouts.keys())
    
    # iterate over the whole dataframe to compute the weights
    # iterating isn't efficient but I don't know better
    for column in df_bigram_weight:
        for row in df_bigram_weight.itertuples():
            df_bigram_weight.at[row.Index, column] = weight(row.Index, column, df_layouts, df_keys, df_penalties)

    return df_bigram_weight


def layout_results(df_bigrams, df_bigram_weight):
    """
    Generate dataframe of results (grade per layout per language)
    """
    # create the empty dataframe
    df_results = pd.DataFrame(index=df_bigram_weight.keys(), columns=df_bigrams.keys())
    
    # iterate over the dataframe to compute the grades
    # iterating isn't efficient but this is small enough
    for column in df_results: # language
        for row in df_results.itertuples(): # layout
            df_results.at[row.Index, column] = (df_bigrams[column] * df_bigram_weight[row.Index]).sum()
    
    return df_results


def removeComments(string):
    """
    Remove the comments from the config file passed as argument. From:
    https://stackoverflow.com/questions/2319019/using-regex-to-remove-comments-from-source-files
    """
    pattern = r"(\".*?\"|\'.*?\')|(/\*.*?\*/|//[^\r\n]*$)"
    regex = re.compile(pattern, re.MULTILINE | re.DOTALL)
    
    def _replacer(match):
        if match.group(2) is not None:
            return ""
        else:
            return match.group(1)
    
    return regex.sub(_replacer, string)


if __name__ == '__main__':
    main()
