# module apply processing to text (not word lists)

# import collections module for word frequency
import collections


# split into words
def split_text_into_words(input_text):
    output_words_list = input_text.split(" ")
    return output_words_list


# keep words longer than minimum
def keep_words_min_length(input_words_list, min_length):
    output_words_list = [word for word in input_words_list if (len(word) >= min_length)]
    return output_words_list


# count word frequency
def count_word_frequency(input_words_list):
    word_counts = collections.Counter(input_words_list)
    # returns a collections.Counter object
    return word_counts


# remove stop words (given stop word list source file)
def remove_stop_words(input_words_list, stop_words_file):
    print("stop words file = ", stop_words_file)
    with open(stop_words_file, "r") as f:
        stop_words_list= f.read().split()
        pass

    # remove comments lines starting with #
    stop_words_list[:] = [word for word in stop_words_list if word[:1]!='#']

    # remove stop words from input words list
    output_words_list = [word for word in input_words_list if word not in stop_words_list]

    return output_words_list