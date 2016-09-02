# module for indexing a corpus, and basic search

# import os file deletion
import os
# import collections for index
import collections
# import pandas for index dataframe
import pandas
# import pickle for saving / restoring index
import pickle


# clear (delete) index
def clear_index(content_directory):
    index_file = content_directory + "index"
    if os.path.isfile(index_file):
        os.remove(index_file)
        print("removed index file: ", index_file)
    pass


# print existing index
def print_index(content_directory):
    index_file = content_directory + "index"
    index = pandas.read_pickle(f)
    print(index)
    pass


# update index
def update_index(content_directory, document_name, doc_words_list):
    # start with empty index
    index = pandas.DataFrame()

    # load index if it already exists
    index_file = content_directory + "index"
    index = pandas.read_pickle(index_file)
    pass

    # update index
    # (word, [document_name]) dictionary, there can be many [document_names] in list
    words_ctr = collections.Counter(doc_words_list)
    for w, c in words_ctr.items():
        print("=== ", w, c)
        index.ix[w, doc_name] = c
    pass

    # finally save updated index again
    index.to_pickle(index_file)

    pass


# query index
def search_index(content_directory, search_query):
    print("search_index called")
    # load index if it already exists
    index_file = content_directory + "index"
    index = pandas.read_pickle(index_file)

        # do query
        matching_documents = index[search_query]
        # count occurences in matching documents
        matching_documents_counter = collections.Counter(matching_documents)
        # return list of matching documents ordered by those with most occurences
        return list(matching_documents_counter.most_common())
    pass