# module for indexing a corpus for co-occurrence of words

# glob module for finding files that match a pattern
import glob
# import os file deletion
import os
# import collections for matrices
import collections
# import pandas for matrix dataframe
import pandas
# import numpy for maths functions
import numpy
# max columns when printing .. (may not be needed if auto detected from display)
pandas.set_option('max_columns', 5)


# delete matrices
def delete_matrices(content_directory):
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


# create word cooccurrence matrix just for one document
def create_cooccurrence_matrix_for_document(content_directory, document_name, doc_words_list):
    # start with empty matrix
    cooccurrence_matrix = pandas.DataFrame()

    # create co-occurrence matrix
    # first create word-pair list
    word_pair_list = zip(doc_words_list[:-1], doc_words_list[1:])
    # counts for each pair
    word_pair_ctr = collections.Counter(word_pair_list)
    for wp, c in word_pair_ctr.items():
        #print("=== ", wp, c)
        cooccurrence_matrix.ix[wp] = c
        pass

    # replace NaN wirh zeros
    cooccurrence_matrix.fillna(0, inplace=True)

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

    # return pandas Series
    return unstacked_cooccurrence_matrix
