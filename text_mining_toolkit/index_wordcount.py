# module for indexing a corpus for wordcount

# glob module for finding files that match a pattern
import glob
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
def delete_index(content_directory):
    # delete wordcound index
    wordcount_index_file = content_directory + "index_wordcount.hdf5"
    if os.path.isfile(wordcount_index_file):
        os.remove(wordcount_index_file)
        print("removed wordcount index file: ", wordcount_index_file)
        pass
    pass


# print existing index
def print_index(content_directory):
    wordcount_index_file = content_directory + "index_wordcount.hdf5"
    hd5_store = pandas.HDFStore(wordcount_index_file, mode='r')
    wordcount_index = hd5_store['corpus_index']
    hd5_store.close()
    print("wordcount_index_file ", wordcount_index_file)
    print(wordcount_index.head(10))
    pass


# create word count index just for one document
def create_wordcount_index_for_document(content_directory, document_name, doc_words_list):
    # create index
    # (word, [document_name]) dictionary, there can be many [document_names] in list
    words_ctr = collections.Counter(doc_words_list)

    # convert to numpy structured array, ready for hdf5 storage
    names = ['word', document_name]
    formats = ['S20', 'i4']
    wordcount_index_np = numpy.fromiter(words_ctr.items(), dtype=dict(names=names, formats=formats))

    # convert to pandas
    wordcount_index = pandas.DataFrame(wordcount_index_np[document_name], index=wordcount_index_np['word'], columns=[document_name])
    # convert bytecode string index to normal pandas string
    wordcount_index.index = wordcount_index.index.astype(str)

    # finally save index
    wordcount_index_file = content_directory + document_name + "_index_wordcount.hdf5"
    hd5_store = pandas.HDFStore(wordcount_index_file, mode='w')
    hd5_store['doc_index'] = wordcount_index
    hd5_store.close()
    pass


# merge document indices into a single index for the corpus
def merge_wordcount_indices_for_corpus(content_directory):
    # start with empty index
    wordcount_index = pandas.DataFrame()

    # list of text files
    list_of_index_files = glob.glob(content_directory + "*_index_wordcount.hdf5")

    # load each index file and merge into accummulating corpus index
    for document_index_file in list_of_index_files:
        hd5_store = pandas.HDFStore(document_index_file, mode='r')
        temporary_document_index  = hd5_store['doc_index']
        hd5_store.close()

        # following is a workaround for a pandas bug
        temporary_document_index.index = temporary_document_index.index.astype(str)

        wordcount_index = pandas.merge(wordcount_index, temporary_document_index, sort=False, how='outer', left_index=True, right_index=True)

        # remove document index after merging
        os.remove(document_index_file)
        pass

    # replace NaN wirh zeros
    wordcount_index.fillna(0, inplace=True)

    # finally save index
    wordcount_index_file = content_directory + "index_wordcount.hdf5"
    print("saving corpus word count index ... ", wordcount_index_file)
    hd5_store = pandas.HDFStore(wordcount_index_file, mode='w')
    hd5_store['corpus_index'] = wordcount_index
    hd5_store.close()
    pass


# query wordcount index
def search_wordcount_index(content_directory, search_query):
    # load index if it already exists
    wordcount_index_file = content_directory + "index_wordcount.hdf5"
    hd5_store = pandas.HDFStore(wordcount_index_file, mode='r')
    wordcount_index = hd5_store['corpus_index']
    hd5_store.close()

    # following is a workaround for a pandas bug
    wordcount_index.index = wordcount_index.index.astype(str)

    # query string to list of search terms
    search_query_list = search_query.split()

    # do query
    documents = wordcount_index.loc[search_query_list]
    # sum the scores
    results = documents.sum()
    # multiply the scores
    #results = documents.prod()
    # filter out those with score of zero
    results = results[results > 0]
    return results.sort_values(ascending=False)
