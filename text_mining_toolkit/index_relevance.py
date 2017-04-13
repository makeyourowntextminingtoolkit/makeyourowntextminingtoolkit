# module for indexing a corpus for relevance

import os
import pandas
import numpy

# max columns when printing .. (may not be needed if auto detected from display)
pandas.set_option('max_columns', 5)


# delete indices
def delete_index(content_directory):
    # delete relevance index
    relevance_index_file = content_directory + "index_relevance.hdf5"
    if os.path.isfile(relevance_index_file):
        os.remove(relevance_index_file)
        print("removed relevance index file: ", relevance_index_file)
        pass
    pass


# print existing index
def print_index(content_directory):
    # relevance index
    relevance_index_file = content_directory + "index_relevance.hdf5"
    hd5_store = pandas.HDFStore(relevance_index_file, mode='r')
    relevance_index = hd5_store['corpus_index']
    hd5_store.close()
    print("relevance_index_file ", relevance_index_file)
    print(relevance_index.head(10))
    pass


# calculate relevance index from wordcount index
def calculate_relevance_index(content_directory):
    # load wordcount index
    wordcount_index_file = content_directory + "index_wordcount.hdf5"
    hd5_store = pandas.HDFStore(wordcount_index_file, mode='r')
    wordcount_index = hd5_store['corpus_index']
    hd5_store.close()

    # following is a workaround for a pandas bug
    wordcount_index.index = wordcount_index.index.astype(str)

    # word frequency (per document) from wordcount, aka TF
    frequency_index = wordcount_index/wordcount_index.sum()

    # catch the case when document has none of the words,
    # which can happen if a filter (such as min word length) removes them all
    frequency_index.fillna(0, inplace=True)

    # penalise short word length
    for word in frequency_index.index.values:
        frequency_index.loc[word] = frequency_index.loc[word] * numpy.tanh(len(word)/5.0)
        pass

    # inverse document frequency
    for word in frequency_index.index.values:
        documents = frequency_index.loc[word]
        matching_documents = documents[documents > 0]
        inverse_document_frequency = 1.0 - (len(matching_documents) / len(documents))
        # print("word =", word, " idf = ", inverse_document_frequency)
        frequency_index.loc[word] = frequency_index.loc[word] * inverse_document_frequency
        pass

    # save relevance index
    relevance_index_file = content_directory + "index_relevance.hdf5"
    print("saving corpus relevance index ... ", relevance_index_file)
    hd5_store = pandas.HDFStore(relevance_index_file, mode='w')
    hd5_store['corpus_index'] = frequency_index
    hd5_store.close()
    pass


# query relevance index
def search_relevance_index(content_directory, search_query):
    # load index if it already exists
    relevance_index_file = content_directory + "index_relevance.hdf5"
    hd5_store = pandas.HDFStore(relevance_index_file, mode='r')
    relevance_index = hd5_store['corpus_index']
    hd5_store.close()

    # following is a workaround for a pandas bug
    relevance_index.index = relevance_index.index.astype(str)

    # query string to list of search terms
    search_query_list = search_query.split()

    # do query
    documents = relevance_index.loc[search_query_list]
    # sum the scores
    results = documents.sum()
    # multiply the scores
    #results = documents.prod()
    # filter out those with score of zero
    results = results[results > 0]
    return results.sort_values(ascending=False)


# get words ordered by relevance (across all documents)
def get_words_by_relevance(content_directory):
    # load relevance index
    relevance_index_file = content_directory + "index_relevance.hdf5"
    hd5_store = pandas.HDFStore(relevance_index_file, mode='r')
    relevance_index = hd5_store['corpus_index']
    hd5_store.close()

    # following is a workaround for a pandas bug
    relevance_index.index = relevance_index.index.astype(str)

    # sum the relevance scores for a word across all documents, sort
    word_relevance = relevance_index.sum(axis=1).sort_values(ascending=False)

    # return pandas frame
    word_relevance_df = pandas.DataFrame(word_relevance)

    return word_relevance_df
