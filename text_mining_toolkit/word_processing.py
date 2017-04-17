# module apply processing to text (not word lists)

import collections
import pandas
import re


# keep words longer than minimum
def keep_words_min_length(input_words_list, min_length):
    output_words_list = [word for word in input_words_list if (len(word) >= min_length)]
    return output_words_list


# count word occurance
def count_word_occurance(input_words_list):
    word_counts = collections.Counter(input_words_list)
    # returns a dataframe
    word_counts_df = pandas.DataFrame.from_dict(dict(word_counts), orient='index')
    word_counts_df.columns = ['count']
    return word_counts_df.sort_values(by='count', ascending=0)


# remove stop words (given stop word list source file)
def remove_stop_words(input_words_list, stop_words_file):
    with open(stop_words_file, "r") as f:
        stop_words_list= f.read().split()
        pass

    # remove comments lines starting with #
    stop_words_list[:] = [word for word in stop_words_list if word[:1]!='#']

    # remove stop words from input words list
    output_words_list = [word for word in input_words_list if word not in stop_words_list]

    return output_words_list


# build n-grams
def build_ngrams_from_words(input_words_list, ngram_length):
    #print("ngram_length = ", ngram_length)
    # construct the ngrams
    z = zip(*[input_words_list[i:] for i in range(ngram_length)])
    # join them together to make a string (in a list)
    output_ngrams_list = [" ".join(t) for t in z]
    return output_ngrams_list


# remove word with n repeated characters
def remove_words_with_n_repeated_chars(input_words_list, n):
    # words with repeated chars anywhere in the strong (re.match only matches from the start)
    # seems to require (n-1) in expression
    regex = re.compile(r'(.)\1{' + str(n - 1) + r',}')
    output_text = [word for word in input_words_list if not regex.search(word)]
    return output_text