# module for indexing a corpus, and basic search

# import os file deletion
import os
# import collections for index
import collections
# import pickle for saving / restoring index
import pickle


# clear (delete) index
def clear_index(content_directory):
    index_file = content_directory + "index"
    if os.path.isfile(index_file):
        os.remove(index_file)
        print("removed index file: ", index_file)
    pass


# update index
def update_index(content_directory, document_name, doc_words_list):
    # start with empty index
    index = collections.Counter()

    # load index if it already exists
    index_file = content_directory + "index"
    if os.path.isfile(index_file):
        with open(index_file, "rb") as f:
            print("loading existing index, ", index_file)
            index = pickle.load(f)
            pass
    pass

    # update index


    # finally save updated index again
    with open(index_file, "wb") as f:
        pickle.dump(index, f)
        pass

    pass


# query index
def search_index(corpus, search_query):
    print("search_index called")
    pass