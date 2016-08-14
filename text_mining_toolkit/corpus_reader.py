# module to read corpora
# a corpus will be a directory with a plain text files


# glob module for finding files that match a pattern
import glob
# os module for filename manipulation
import os


class CorpusReader:
    def __init__(self, directory_of_files, text_filename_pattern):
        # corpus location, and file name pattern
        self.directory_of_files = directory_of_files
        self.text_filename_pattern = text_filename_pattern

        print("directory of files = ", self.directory_of_files)
        print("text_filename_pattern = ", self.text_filename_pattern)

        # list of text files
        self.list_of_text_files = glob.glob(directory_of_files + text_filename_pattern)

        # populate dictionary mapping document name to text content
        self.documents = {os.path.basename(i): self.read_text_from_file(i) for i in self.list_of_text_files}
        print("self.documents populated = ", len(self.documents))
        pass


    # simple function to get text from a given text file
    def read_text_from_file(self, text_file_name):
        with open(text_file_name, "r") as f:
            text_content = f.read()
            pass
        return text_content


    # returns list of document file names from dictionary
    def get_documents(self):
        return sorted(self.documents.keys())


    # returns the text content of a given document_file_nameß
    def get_text_by_document(self, document_file_name):
        return self.documents[document_file_name]


    # returns all the text from all the documents
    def get_all_text(self):
        return " ".join(self.documents.values())
