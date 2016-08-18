# module apply processing to text (not word lists)

# import text string stuff
#import string


# split into words
def split_text_into_words(input_text):
    output_words_list = input_text.split(" ")
    return output_words_list


# keep words longer than minimum
def keep_words_min_length(input_words_list, min_length):
    output_words_list = [word for word in input_words_list if (len(word) >= min_length)]
    return output_words_list
