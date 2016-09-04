# module apply processing to text (not word lists)

# import collections module for word frequency
import collections


# keep words longer than minimum
def keep_words_min_length(input_words_list, min_length):
    output_words_list = [word for word in input_words_list if (len(word) >= min_length)]
    return output_words_list


# count word occurance
def count_word_occurance(input_words_list):
    word_counts = collections.Counter(input_words_list)
    # returns a collections.Counter object
    return word_counts


# remove stop words (given stop word list source file)
def remove_stop_words(input_words_list, stop_words_file):
    with open(stop_words_file, "r") as f:
        stop_words_list= f.read().split()
        pass

    # remove comments lines starting with #
    stop_words_list[:] = [word for word in stop_words_list if word[:1]!='#']

    # remove stop words from input words list
    output_words_list = [word for word in input_words_list if word not in stop_words_list]

    return output_words_list


# build n-grams
def build_ngrams_from_words(input_words_list, ngram_length):
    print("ngram_length = ", ngram_length)
    # construct the ngrams
    z = zip(*[input_words_list[i:] for i in range(ngram_length)])
    # join them together to make a string (in a list)
    output_ngrams_list = [" ".join(t) for t in z]
    return output_ngrams_list