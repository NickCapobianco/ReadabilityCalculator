from time import time

# Get script start time
start = time()

from pandas import read_csv
from numpy import array
import string
from PyPDF2 import PdfReader

# Import known words and file
words = "WordList.csv"
# file_path = "example.pdf"
file_path = "example.txt"

# Create a Pandas DataFrame of known words with Pandas.read_csv
wordList = read_csv(words)

# Convert the Pandas DataFrame to a set
wordList = set(array(wordList)[:, 0])

# Load Text File
def load_file(file_path):
    # Load a file for parsing
    if file_path.endswith(".txt"):
        with open(file_path, 'r') as file:
            file_list = file.read()
        translation_table = str.maketrans(string.punctuation + '\n', ' ' * (len(string.punctuation) + 1))
        file_list = file_list.translate(translation_table)
        return file_list.split()
    elif file_path.endswith(".pdf"):
        file = PdfReader(file_path)
        file_list = []
        for i in range(len(file.pages) - 2):
            page_text = file.pages[i].extract_text()
            translation_table = str.maketrans(string.punctuation + '\n', ' ' * (len(string.punctuation) + 1))
            page_text = page_text.translate(translation_table)
            file_list.extend(page_text.split())
        return file_list

# Load the file using a set for unique words
fileList = set(load_file(file_path))

# Create a new list for storing matched words between known words and file in question
matched_words = []

def readability(word_list, file_list, matched_words):
    matched_word_count = 0
    for word in file_list:
        if word in word_list:
            matched_word_count += 1
            if word not in matched_words:
                matched_words.append(word)
    return matched_word_count, len(file_list), (matched_word_count / len(file_list))

# Compute readability score
known_words, present_words, comparison = readability(wordList, fileList, matched_words)

# Print known word count, word count present in current file, readability score, and matched words
print("Known word count in file:", known_words)
print("Words in file:", present_words)
print("Matched Words:", matched_words)
print("Readability Percentage: {:.2%}".format(comparison))

# Print script execution time
print("Script Execution Time:", time() - start)