#!/usr/bin/python3

import os
import string
import pandas as pd


# where the data is
fileDir = os.path.join(os.path.dirname(os.path.realpath('__file__')), 'data')

# list the data files
fileslist = [f for f in os.listdir(fileDir) if os.path.isfile(os.path.join(fileDir, f))]

# list of characters to take into account
chars = list(string.ascii_lowercase) + ['é', 'è', 'ê', 'à', 'ç', 'â', 'î', 'ô'] + ['.', ',', '-', '\'', '/']
# + ['.', ',', ':', ';', '?', '!', '\'', '(', ')', '<', '>', '-', '+', '/', '*', '%', '=', '@', '"', '&']

# create list of bigrams
bigrams = []
for a in chars:
    for b in chars:
        bigrams.append(a + b)

# create pandas arrays
dfchars = pd.DataFrame(index=chars)
dfbigram = pd.DataFrame(index=bigrams)

# loop through files
for f in fileslist:
    filename = os.path.join(fileDir, f)
    filehandle = open(filename)
    filetext = filehandle.read()
    
    # add column to the dataframe
    colname = f
    if '.txt' in colname:
        colname = colname[:-4]
        
    dfchars[colname] = 0
    dfbigram[colname] = 0
    
    # iterate over all chars of the file
    for i in range(len(filetext)):
        chari = filetext[i].lower()
        if i < len(filetext) - 1:
            bigrami = filetext[i].lower() + filetext[i + 1].lower()
        
        if chari in dfchars.index:
            dfchars.at[chari, colname] = dfchars.loc[chari, colname] + 1
        if bigrami in dfbigram.index:
            dfbigram.at[bigrami, colname] = dfbigram.loc[bigrami, colname] + 1
    
    filehandle.close()

dfchars.to_csv('chars.csv')
dfbigram.to_csv('bigrams.csv')
