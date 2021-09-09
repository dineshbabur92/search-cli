from cmd import Cmd
from glob import glob
from collections import defaultdict
import os

SEARCH_FOLDER = "./search_folder/" 

class MyPrompt(Cmd):
    # cli intro
    prompt = 'search-cli> '
    intro = "Welcome to the search-cli. Enter 'help' to explore options. Enter 'help' <option> to view documentation"
    
    def do_index(self, inp: str):
        """
        for indexing the ./search_folder files
        """
        if inp:
            print("Indexing does not require any parameters")
        print("Indexing files in ./search_folder...")
        
        # inverted_index similar to elastic search
        self.inverted_index = index_files()

    def help_index(self):
        print("Indexes documents in ./search_folder")

    def do_search(self, search_txt:str):
        """
        Searching txt in files
        """
        if not search_txt:
            print("Please enter some search text")
            return
        if not hasattr(self,'inverted_index'):
            print("Please index the files first, before searching. Enter 'index'")
            return
        
        search_files(search_txt, self.inverted_index)
        # return True

    def help_search(self):
        print("Searches files in ./search_folder for words in search_txt and ranks top 10")    

    def do_exit(self, inp):
        print("Bye")
        return True

    def help_exit(self):
        print("Enter 'exit' to exit the cli")
 
    # def do_add(self, inp):
    #     print("adding '{}'".format(inp))
 
    # def help_add(self):
    #     print("Add a new entry to the system.")
 
    # def default(self, inp):
    #     if inp == 'x' or inp == 'q':
    #         return self.do_exit(inp)
 
    #     print("Default: {}".format(inp))
 
    # do_EOF = do_exit
    # help_EOF = help_exit
 
 
def index_files():
    """
    To create inverted index for files in ./search_folder
    """

    # list of files in SEARCH_FOLDER
    files = glob(f"{SEARCH_FOLDER}*")
    
    # init
    inverted_index = defaultdict(lambda: defaultdict(lambda: 0))
    
    for file in files:
        
        # reading by lines and spliting to words
        words = []
        with open(file, "r") as file_reader:
            words = file_reader.read().split()
        
        # for each words, indexing files in which
        #     it is present
        for word in words:
            inverted_index[word][os.path.basename(file)] += 1
        
    # for key in list(inverted_index.keys())[:3]:
    #     print(inverted_index[key])

    return inverted_index
            
def search_files(search_txt: str, inverted_index: defaultdict(lambda: defaultdict(lambda: 0))):
    """
    Searches files in SEARCH_FOLDER for search_txt

    Args:
    search_txt - Text to be searched
    inverted_index - Indexed word dict represeting words
                     present in each file

    Returns:
    None
    """
    # no. of words present in each file, init to 0
    search_words_in_files =  defaultdict(lambda: 0)

    # words to be searched
    search_words = search_txt.split()
    total_words = len(search_words)

    # searching all words in all files
    #     using inverted index
    files = glob(f"{SEARCH_FOLDER}*")
    for word in search_words:
        for file in files:
            filename = os.path.basename(file)
            if inverted_index[word][filename]:
                    search_words_in_files[filename] += 1

    # converting to perc
    for filename in search_words_in_files:
        search_words_in_files[filename] = round(search_words_in_files[filename]/total_words * 100,2)

    # final files rank sorted by scores(0 to 100 based perc of no. of words)
    files_ranked = sorted(search_words_in_files.items(), key=lambda x:x[1], reverse=True)

    # printing output files by rank
    print(files_ranked[:10])

if __name__ == '__main__':
    # runs an infinite cli
    MyPrompt().cmdloop()