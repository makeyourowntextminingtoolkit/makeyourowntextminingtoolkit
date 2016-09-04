# module for indexing a corpus, and basic search

# import os file deletion
import os
# import collections for index
import collections
# import pandas for index dataframe
import pandas
# import numpy for maths functions
import numpy
# max columns when printing .. (may not be needed if auto detected from display)
pandas.set_option('max_columns', 5)


# delete indices
def delete_indices(content_directory):
    # delete wordcount index
    wordcount_index_file = content_directory + "index.wordcount"
    if os.path.isfile(wordcount_index_file):
        os.remove(wordcount_index_file)
        print("removed wordcount index file: ", wordcount_index_file)
        pass

    # delete relevance index
    relevance_index_file = content_directory + "index.relevance"
    if os.path.isfile(relevance_index_file):
        os.remove(relevance_index_file)
        print("removed relevance index file: ", relevance_index_file)
        pass
    pass


# print existing index
def print_index(content_directory):
    # wordcount index
    wordcount_index_file = content_directory + "index.wordcount"
    wordcount_index = pandas.read_pickle(wordcount_index_file)
    print(wordcount_index.head(10))

    # relevance index
    relevance_index_file = content_directory + "index.relevance"
    relevance_index_ = pandas.read_pickle(relevance_index_file)
    print(relevance_index_.head(10))
    pass


# update word count index
def update_wordcount_index(content_directory, document_name, doc_words_list):
    # start with empty index
    wordcount_index = pandas.DataFrame()

    # load index if it already exists
    wordcount_index_file = content_directory + "index.wordcount"
    if os.path.isfile(wordcount_index_file):
        wordcount_index = pandas.read_pickle(wordcount_index_file)
        pass

    # update index
    # (word, [document_name]) dictionary, there can be many [document_names] in list
    words_ctr = collections.Counter(doc_words_list)
    for w, c in words_ctr.items():
        #print("=== ", w, c)
        wordcount_index.ix[w, document_name] = c
        pass

    # replace NaN wirh zeros
    wordcount_index.fillna(0, inplace=True)

    # finally save updated index again
    wordcount_index.to_pickle(wordcount_index_file)
    pass


# calculate relevance index from wordcount index
def calculate_relevance_index(content_directory):
    # load wordcount index
    wordcount_index_file = content_directory + "index.wordcount"
    wordcount_index = pandas.read_pickle(wordcount_index_file)

    # word frequency (per document) from wordcount, aka TF
    frequency_index = wordcount_index/wordcount_index.sum()

    # penalise short word length
    print("1=== ", frequency_index)
    for word in frequency_index.index.values:
        frequency_index.loc[word] = frequency_index.loc[word] * numpy.tanh(len(word)/5.0)
        pass
    # still to do IDF
    print("2=== ", frequency_index)

    # save relevance index
    relevance_index_file = content_directory + "index.relevance"
    frequency_index.to_pickle(relevance_index_file)
    pass


# query index
def search_index(content_directory, search_query):
    print("search_index called")
    # load index if it already exists
    relevance_index_file = content_directory + "index.relevance"
    relevance_index = pandas.read_pickle(relevance_index_file)

    # do query
    documents = relevance_index.loc[search_query]
    # filter out those with word count of zero
    matching_documents = documents[documents > 0]
    print("matching_documents", matching_documents)
    # to list
    matching_documents_list = [(k,v) for (k,v) in matching_documents.to_dict().items()]
    return matching_documents_list
