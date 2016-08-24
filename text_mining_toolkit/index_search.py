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
        for i in range(5):
            print(list(index.items())[i])
            pass
    pass


# update index
def update_index(content_directory, document_name, doc_words_list):
    # start with empty index
    index = collections.defaultdict(list)

    # load index if it already exists
    index_file = content_directory + "index"
    if os.path.isfile(index_file):
        with open(index_file, "rb") as f:
            print("loading existing index, ", index_file)
            index = pickle.load(f)
            pass
    pass

    # update index
    # (word, [document_name]) dictionary, there can be many [document_names] in list
    [index[word].append(document_name) for word in doc_words_list]

    # finally save updated index again
    with open(index_file, "wb") as f:
        print("saving updated index, ", index_file)
        pickle.dump(index, f)
        pass

    pass


# query index
def search_index(content_directory, search_query):
    print("search_index called")
    # load index if it already exists
    index_file = content_directory + "index"
    if os.path.isfile(index_file):
        with open(index_file, "rb") as f:
            print("loading existing index, ", index_file)
            index = pickle.load(f)
            pass

        # do query
        matching_documents = index[search_query]
        # count occurences in matching documents
        matching_documents_counter = collections.Counter(matching_documents)
        # return list of matching documents ordered by those with most occurences
        return list(matching_documents_counter.most_common())
    pass