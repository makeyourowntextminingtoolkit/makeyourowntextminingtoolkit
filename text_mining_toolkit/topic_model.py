# module for extracting topic models using Singular Value Decomposition (SVD)

import os
import pandas
import numpy

# max columns when printing .. (may not be needed if auto detected from display)
pandas.set_option('max_columns', 5)


# delete svd file
def delete_svd(content_directory):
    # delete relevance index
    svd_file = content_directory + "svd.hdf5"
    if os.path.isfile(svd_file):
        os.remove(svd_file)
        print("removed svd: ", svd_file)
        pass
    pass


# calculate SVD and save
def calculate_singular_value_decomposition(content_directory):
    # load word-docuent matrix (here using relevance, not wordcount)
    relevance_index_file = content_directory + "index_relevance.hdf5"
    hd5_store = pandas.HDFStore(relevance_index_file, mode='r')
    relevance_index = hd5_store['corpus_index']
    hd5_store.close()

    # following is a workaround for a pandas bug
    relevance_index.index = relevance_index.index.astype(str)

    # calculate SVD
    U, S, VT = numpy.linalg.svd(relevance_index, full_matrices=False)
    # not S is a 1-d series of eigenvalues, not a matrix, for efficient storage
    # to make a matrix use S_matrix = numpy.diag(S)

    # convert to dataframe
    U_df = pandas.DataFrame(U, index=relevance_index.index)
    S_df = pandas.DataFrame(S)
    VT_df = pandas.DataFrame(VT, columns = relevance_index.columns)

    # save the three SVD matrices in the same hdf5 file
    svd_file = content_directory + "svd.hdf5"
    print("saving singular value decomposition ... ", svd_file)
    hd5_store = pandas.HDFStore(svd_file, mode='w')
    hd5_store['U'] = U_df
    hd5_store['S'] = S_df
    hd5_store['VT'] = VT_df
    hd5_store.close()
    pass


# get already calculated SVD frames
def get_svd(content_directory):
    # load dataframes of U, S, VT
    svd_file = content_directory + "svd.hdf5"
    hd5_store = pandas.HDFStore(svd_file, mode='r')
    U_df = hd5_store['U']
    S_df = hd5_store['S']
    VT_df = hd5_store['VT']
    hd5_store.close()

    # following is a workaround for a pandas bug
    U_df.index = U_df.index.astype(str)
    S_df.index = S_df.index.astype(str)
    VT_df.index = VT_df.index.astype(str)

    return U_df, S_df, VT_df