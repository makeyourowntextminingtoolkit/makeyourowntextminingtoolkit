# module for indexing a corpus for document similarity

import os
import collections
import pandas
import math
import random
import scipy.spatial.distance
import itertools

# max columns when printing .. (may not be needed if auto detected from display)
pandas.set_option('max_columns', 5)

#temp warning catch
import warnings

# delete matrix
def delete_matrix(content_directory):
    doc_similarity_matrix_file = content_directory + "matrix_docsimilarity.hdf5"
    if os.path.isfile(doc_similarity_matrix_file):
        os.remove(doc_similarity_matrix_file)
        print("removed doc similarity matrix file: ", doc_similarity_matrix_file)
        pass
    pass


# print existing matrix
def print_matrix(content_directory):
    # open matrix file
    doc_similarity_matrix_file = content_directory + "matrix_docsimilarity.hdf5"
    hd5_store = pandas.HDFStore(doc_similarity_matrix_file, mode='r')
    doc_similarity_matrix = hd5_store['corpus_matrix']
    hd5_store.close()
    # print first 10 entries
    print("doc_similarity_matrix_file ", doc_similarity_matrix_file)
    print(doc_similarity_matrix.head(10))
    pass


# create document similarity matrix, the relevance matrix needs to already exist
# sample_fraction is useful to select a subset of documents as the combinations get large quickly
def create_doc_similarity_matrix(content_directory, sample_fraction):
    # start with empty dictionary for collecting similarity results
    doc_similarity_dict = collections.defaultdict(dict)

    # load the relevance matrix
    relevance_index_file = content_directory + "index_relevance.hdf5"
    hd5_store = pandas.HDFStore(relevance_index_file, mode='r')
    relevance_index = hd5_store['corpus_index']
    hd5_store.close()

    # following is a workaround for a pandas bug
    relevance_index.index = relevance_index.index.astype(str)

    # calcuate similarity as dot_product(doc1, doc2)
    docs = list(relevance_index.columns)

    print("docs = ", len(docs))
    docs_sample = random.sample(docs, math.ceil(sample_fraction*len(docs)))
    print("docs_sample = ", len(docs_sample))

    total = len(list(itertools.combinations(docs_sample, 2)))
    print("total combinations = ", total)

    # combinations (not permutations) of length 2, also avoid same-same combinations
    docs_combinations = itertools.combinations(docs_sample, 2)
    for doc1, doc2 in docs_combinations:
        # scipy cosine similarity function includes normalising the vectors but is a distance .. so we need to take it from 1.0
        doc_similarity_dict[doc2].update({doc1: 1.0 - scipy.spatial.distance.cosine(relevance_index[doc1],relevance_index[doc2])})
        pass

    #convert dict to pandas dataframe
    doc_similarity_matrix = pandas.DataFrame(doc_similarity_dict)

    # finally save matrix
    doc_similarity_matrix_file = content_directory + "matrix_docsimilarity.hdf5"
    hd5_store = pandas.HDFStore(doc_similarity_matrix_file, mode='w')
    hd5_store['corpus_matrix'] = doc_similarity_matrix
    hd5_store.close()
    print("created ", doc_similarity_matrix_file)
    pass


# query document similarity matrix
def query_doc_similarity_matrix(content_directory, doc1, doc2):
    # open matrix file
    cooccurrence_matrix_file = content_directory + "matrix_docsimilarity.hdf5"
    hd5_store1 = pandas.HDFStore(cooccurrence_matrix_file, mode='r')
    cooccurrence_matrix = hd5_store1['corpus_matrix']
    hd5_store1.close()

    # query matrix and return
    return cooccurrence_matrix[doc, word2]


# get document pairs ordered by similarity
def get_doc_pairs_by_similarity(content_directory):
    # open matrix file
    doc_similarity_matrix_file = content_directory + "matrix_docsimilarity.hdf5"
    hd5_store1 = pandas.HDFStore(doc_similarity_matrix_file, mode='r')
    doc_similarity_matrix = hd5_store1['corpus_matrix']
    hd5_store1.close()

    # unstack the similarity matrix
    unstacked_doc_similarity_matrix = doc_similarity_matrix.unstack()
    # remove the zero occurances (nans)
    unstacked_doc_similarity_matrix = unstacked_doc_similarity_matrix[unstacked_doc_similarity_matrix > 0]
    # sort by similarity value
    unstacked_doc_similarity_matrix.sort_values(ascending=False, inplace=True)

    # convert to pandas dataframe with doc1, doc2, similarity
    doc1_doc1_similarity_list = [(doc1, doc2, unstacked_doc_similarity_matrix.ix[doc1, doc2]) for (doc1, doc2) in unstacked_doc_similarity_matrix.index.values]
    doc1_doc2_similarity = pandas.DataFrame(doc1_doc1_similarity_list, columns=["doc1", "doc2", "similarity"])

    # normalise similarity to 0-1
    doc1_doc2_similarity['similarity'] /= doc1_doc2_similarity['similarity'].max()

    # return dataframe
    return doc1_doc2_similarity
