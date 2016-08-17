# module apply processing to text

# import text string stuff
import string


# make lowercase
def make_lowercase(nput_text):
    output_text = input_text.lower()
    return output_text


# remove punctuation
def remove_punctuation(input_text):
    output_text = input_text.translate(str.maketrans({a:None for a in string.punctuation}))
    return output_text


# split into words
def split_text_into_words(input_text):
    output_text = input_text.split(" ")
    return output_text
