# module for indexing a corpus for co-occurrence of words

# glob module for finding files that match a pattern
import glob
# import os file deletion
import os
# import collections for matrices
import collections
# import pandas for matrix dataframe
import pandas
# import for maths functions
import math
# max columns when printing .. (may not be needed if auto detected from display)
pandas.set_option('max_columns', 5)


# delete matrix
def delete_matrix(content_directory):
    cooccurrence_matrix_file = content_directory + "matrix.cooccurrence"
    if os.path.isfile(cooccurrence_matrix_file):
        os.remove(cooccurrence_matrix_file)
        print("removed co-occurrence matrix file: ", cooccurrence_matrix_file)
        pass
    pass


# print existing matrix
def print_matrix(content_directory):
    # open matrix file
    cooccurrence_matrix_file = content_directory + "matrix.cooccurrence"
    hd5_store1 = pandas.HDFStore(cooccurrence_matrix_file, mode='r')
    cooccurrence_matrix = hd5_store1['corpus_matrix']
    hd5_store1.close()
    # print first 10 entries
    print("cooccurrence_matrix_file ", cooccurrence_matrix_file)
    print(cooccurrence_matrix.head(10))
    pass


# create word cooccurrence matrix just for one document, updated to extend beyond immediate neighbour
def create_cooccurrence_matrix_for_document(content_directory, document_name, doc_words_list, window):

    # start with empty matrix
    cooccurrence_matrix = pandas.DataFrame()

    # work along window
    for ci in range(1, window + 1):
        # first create word-pair list
        word_pair_list = zip(doc_words_list[:-ci], doc_words_list[ci:])

        # counts for each pair
        word_pair_ctr = collections.Counter(word_pair_list)

        for wp, c in word_pair_ctr.items():
            neighbour_factor = math.exp(- math.pow(ci / window,2))
            # this try-exceptis ugly, needed because pandas doesn't yet have df[wp] += ...
            try:
                cooccurrence_matrix.ix[wp] += (c * neighbour_factor)
            except KeyError:
                cooccurrence_matrix.ix[wp] = (c * neighbour_factor)
                pass
            # replaces any created NaNs with zeros
            cooccurrence_matrix.fillna(0, inplace=True)
        pass

    pass

    # finally save matrix
    cooccurrence_matrix_file = content_directory + document_name + "_matrix.cooccurrence"
    hd5_store = pandas.HDFStore(cooccurrence_matrix_file, mode='w')
    hd5_store['doc_matrix'] = cooccurrence_matrix
    hd5_store.close()
    pass


# merge document matrices into a single matrix for the corpus
def merge_cooccurrence_matrices_for_corpus(content_directory):
    # start with empty matrix
    cooccurrence_matrix = pandas.DataFrame()

    # list of text files
    list_of_matrix_files = glob.glob(content_directory + "*_matrix.cooccurrence")

    # load each matrix file and merge into accummulating corpus matrix
    for document_matrix_file in list_of_matrix_files:
        hd5_store = pandas.HDFStore(document_matrix_file, mode='r')
        temporary_document_matrix = hd5_store['doc_matrix']
        hd5_store.close()

        cooccurrence_matrix = cooccurrence_matrix.add(temporary_document_matrix, fill_value=0)

        # remove document index after merging
        os.remove(document_matrix_file)
        pass

    # replace NaN wirh zeros
    cooccurrence_matrix.fillna(0, inplace=True)

    # finally save matrix
    corpus_matrix_file = content_directory + "matrix.cooccurrence"
    print("saving corpus co-occurrence matrix ... ", corpus_matrix_file)
    hd5_store = pandas.HDFStore(corpus_matrix_file, mode='w')
    hd5_store['corpus_matrix'] = cooccurrence_matrix
    hd5_store.close()
    pass


# query co-occurrence matrix
def query_cooccurance_matrix(content_directory, word1, word2):
    # open matrix file
    cooccurrence_matrix_file = content_directory + "matrix.cooccurrence"
    hd5_store1 = pandas.HDFStore(cooccurrence_matrix_file, mode='r')
    cooccurrence_matrix = hd5_store1['corpus_matrix']
    hd5_store1.close()

    # query matrix and return
    return cooccurrence_matrix.ix[word1, word2]


# query co-occurrence matrix
def most_likely_next(content_directory, word1):
    # open matrix file
    cooccurrence_matrix_file = content_directory + "matrix.cooccurrence"
    hd5_store1 = pandas.HDFStore(cooccurrence_matrix_file, mode='r')
    cooccurrence_matrix = hd5_store1['corpus_matrix']
    hd5_store1.close()

    # query matrix and return index with max cooccurrence value
    return  cooccurrence_matrix.loc[word1].idxmax()


# get words ordered by cooccurrence (across all documents)
def get_word_pairs_by_cooccurrence(content_directory):
    # open matrix file
    cooccurrence_matrix_file = content_directory + "matrix.cooccurrence"
    hd5_store1 = pandas.HDFStore(cooccurrence_matrix_file, mode='r')
    cooccurrence_matrix = hd5_store1['corpus_matrix']
    hd5_store1.close()

    # to find max we need to unstack (unpack 2d matrix into 1d list)
    unstacked_cooccurrence_matrix = cooccurrence_matrix.T.unstack()
    # remove the zero occurances
    unstacked_cooccurrence_matrix = unstacked_cooccurrence_matrix[unstacked_cooccurrence_matrix>0]
    # sort by co-occurance value
    unstacked_cooccurrence_matrix.sort_values(ascending=False, inplace=True)

    # convert to pandas dataframe with word1, word2, weight columns
    word1_word2_weight_list = [ (w1, w2, unstacked_cooccurrence_matrix.ix[w1,w2]) for (w1,w2) in unstacked_cooccurrence_matrix.index.values]
    word1_word2_weight = pandas.DataFrame(word1_word2_weight_list, columns=["word1", "word2", "weight"])

    # normalise weight to 0-1
    word1_word2_weight['weight'] /= word1_word2_weight['weight'].max()

    # return dataframe
    return word1_word2_weight
