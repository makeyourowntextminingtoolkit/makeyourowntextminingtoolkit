# module to read corpora
# a corpus will be a directory with a plain text files

# glob module for finding files that match a pattern
import glob

class CorpusReader:

    def __init__(self, directory_of_files, text_filename_pattern):
        self.directory_of_files = directory_of_files
        self.text_filename_pattern = text_filename_pattern

        print("directory of files = ", self.directory_of_files)
        print("text_filename_pattern = ", self.text_filename_pattern)
        pass

    def get_documents(self):
        print("get documents")
        pass

    def get_all_text(self):
        print("get all text")
        pass

    def get_text_by_document(self):
        print("get text by dooucment")
        pass
