# module apply processing to text

# import text string stuff
import string


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
def keep_alphanumeric(input_text):
    delchars = ''.join(c for c in map(chr, range(256)) if c not in (" " + string.ascii_letters + string.digits))
    output_text = input_text.translate(str.maketrans("\n\r", "  ", delchars))
    return output_text


# split into words
def split_text_into_words(input_text):
    output_text = input_text.split(" ")
    return output_text
