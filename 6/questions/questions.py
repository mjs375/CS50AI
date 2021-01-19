import math
import nltk
import os
import re
import string
import sys

"""
Question Answering (QA) natural language processing program.
"""

#--AI will find top-matched document(s) and top-matched sentence(s) to answer the question:
FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])

    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }

    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)










def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each `.txt` file inside that directory to the file's contents as a string.
    """
    #--Dict{Key:.txt filename / value: entire page contents}
    database = {}

    #--Open the Database directory:
    for path, subfolders, files in os.walk(directory):
        for file in files:
            #--Just in case check:
            if file.endswith('.txt'):
                with open(os.path.join(path,file)) as f:
                    contents = f.read()
                    database[file] = contents
    #
    #
    #
    return database










def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    #--Break document string into list of words:
    tokens = nltk.word_tokenize(document)
    #--Filter out punctuation, lowercase words:
    tokens = [word.lower() for word in tokens if word.lower() not in nltk.corpus.stopwords.words("english") and word not in string.punctuation]
    #--2nd punctuation filter:
    words = []
    for token in tokens:
        alpha = bool(re.match("(?=.*[a-z])", token.lower()))
        if alpha:
            words.append(token.lower())
    # Another letter-checker:   any(c.isalpha() for c in word)
    #
    #
    return words









def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the resulting dictionary.
    """
    #--Each word's IDF value:
    idfs = {}

    #--Number of docs in corpus:
    total_docs = len(documents)
    #--A set of all unique words:
    allwords = set() # ... (don't dupe calculations)
    for page in documents:
        allwords.update(documents[page])
    #--Calculate the IDF for each word:
    for word in allwords:
        freq = sum(word in documents[page] for page in documents)
        idf = math.log(total_docs / freq)
        idfs[word] = idf
    #
    #
    #
    return idfs





def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of files to a list of their words), and `idfs` (a dictionary mapping words to their IDF values), return a list of the filenames of the the `n` top files that match the query, ranked according to tf-idf.
    """
    tfidfs = {}

    for file, contents in files.items():
        total = 0
        for word in query:
            if word in contents:
                #--Count TF of target query word:
                tf = term_frequency(contents, word)
                total += tf * idfs[word]
                #-- TF * IDF score = tfidfs
                tfidfs[file] = total
    #--Create a list of tuples (tfidfs, filename):
    topfiles = [ (val, key) for (key, val) in tfidfs.items() ]
    #--Sort high to low by tfidfs (tuple[0]):
    topfiles.sort(key=lambda x:x[0], reverse=True)
    #--List of top 'n' filenames:
    tops = [ top[1] for top in topfiles[:n] if top[0] > 0 ]
    if tops == []:
        raise Exception("Query keywords found no answer.")
    #print(f"Top {n} files: {tops}")
    #
    #
    #
    return tops

def term_frequency(contents, word):
    """ Helper function for top_files(), calculates term frequency given a target word and contents. """
    tf = 0
    for w in contents:
        if w == word:
            tf += 1
    return tf


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping sentences to a list of their words), and `idfs` (a dictionary mapping words to their IDF values), return a list of the `n` top sentences that match the query, ranked according to idf. If there are ties, preference should be given to sentences that have a higher query term density.
        Ex:
    Query: {'python'}
    n: 1
    sentences: <returns the sentences for the top 'n' matching files>
    """

    ranks = {sentence:0 for sentence in sentences.keys()}

    #--Scan each sentence and get its rank (matching word measure):
    for sentence, words in sentences.items():
        #--Get words in BOTH sentence and query-string:
        MATCHED_words = query.intersection(words)
        #--IDF score for each sentence:
        for word in MATCHED_words:
            ranks[sentence] += idfs[word]

    #--Sort the resulting dictionary, high-to-low:
    topsentences = [ (val, key) for (key, val) in ranks.items() ]
    topsentences.sort(key=lambda x:x[0], reverse=True)

    #--Check for ties, if so get most dense, highest-[idf]ranked sentence:
    tied = []
    for idf, sentence in topsentences:
        if idf == topsentences[0][0]:
            tied.append(sentence)
        else: #--else on to 2nd highest, so stop looking...
            break

    if len(tied) == n or len(tied) < n:
        return tied

    #--Get density of highest-ranked [tied] sentences:
    densities = {sentence:0 for sentence in tied}
    for tie in tied:
        count = 0
        words = tokenize(tie)
        for word in words:
            if word in query:
                count += 1

        density = count / len(tie)
        densities[tie] = density



    #--Return the 'n' matchiest sentences; if a tie, return densest sentence:
    D = [ (val, key) for (key, val) in densities.items() ]
    D.sort(key=lambda x:x[0], reverse=True)
    ans = [ sentence for density, sentence in D[:n] ]
    #
    #
    #
    return ans




# # # # # # # # # # # # # # # #
                              #
if __name__ == "__main__":    #
    #os.system('reset')       #
    main()                    #
                              #
# # # # # # # # # # # # # # # #
