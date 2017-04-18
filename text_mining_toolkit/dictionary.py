# module for working with language dictionaries

import pandas

# get dictionary words
def get_dictionary_words(dictionary):
    # load dictionary
    dictionary_file = "dictionaries/" + dictionary
    words_df = pandas.read_table(dictionary_file)
    words_df.columns=['words']
    return words_df
