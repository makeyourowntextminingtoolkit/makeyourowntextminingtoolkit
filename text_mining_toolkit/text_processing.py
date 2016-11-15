# module apply processing to text (not word lists)

import string
import re

# split into words
def split_text_into_words(input_text):
    output_words_list = input_text.split(" ")
    return output_words_list


# make lowercase
def to_lowercase(input_text):
    output_text = input_text.lower()
    return output_text


# remove whitespace, convert to single space
def simplify_whitespace(input_text):
    #output_text = input_text.translate(str.maketrans(string.whitespace, ' ' * len(string.whitespace)))
    output_text = " ".join(input_text.split())
    return output_text


# remove punctuation
def remove_punctuation(input_text):
    output_text = input_text.translate(str.maketrans({a:None for a in string.punctuation}))
    return output_text


# keep only alphanumeric characters
def keep_only_alphanumeric(input_text):
    regex = re.compile('[^a-zA-Z0-9 ]+')
    output_text = regex.sub('', input_text)
    return output_text
