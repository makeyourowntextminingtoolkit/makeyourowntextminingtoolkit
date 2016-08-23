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


# print existing index
def print_index(content_directory):
    index_file = content_directory + "index"
    if os.path.isfile(index_file):
        with open(index_file, "rb") as f:
            index = pickle.load(f)
            pass
        for x in index.most_common(20):
            print(x)
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
    # first make (word, document_name) tuple
    doc_and_word = [(word, document_name) for word in doc_words_list]
    # then count it
    doc_word_count = collections.Counter(doc_and_word)
    index += doc_word_count

    # finally save updated index again
    with open(index_file, "wb") as f:
        print("saving updated index, ", index_file)
        pickle.dump(index, f)
        pass

    pass


# query index
def search_index(corpus, search_query):
    print("search_index called")
    pass