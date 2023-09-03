import nltk
import sys
import os
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1

def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    
    # files = load_files("corpus")
    
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
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    ans = dict()
    for file in os.listdir(directory):
        with open(os.path.join(directory, file), "r") as filedir:
            ans[file] = filedir.read()

    return ans


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    tokens = nltk.tokenize.word_tokenize(document)
    remove = []

    for i in range(len(tokens)):
        tokens[i] = tokens[i].lower()

    for word in tokens:
        if word in nltk.corpus.stopwords.words("english"):
            remove.append(word)
            continue
        
        punc = False
        alpha = False
        for char in word:
            if char in string.punctuation:
                punc = True
            elif char.isalnum():
                alpha = True
        
        if punc and not alpha:
            remove.append(word)

    for word in remove:
        tokens.remove(word)
    
    return tokens


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    idf = dict()

    for wordlist in documents.values():
        for word in wordlist:
            # if word already in idf, ignore
            if word in idf:
                continue
            # if word not in idf, then check how many documents have that word
            else:
                n_total = len(documents)
                n_included = 0
                for document in documents:
                    if word in documents[document]:
                        n_included += 1
                
                idf[word] = math.log(n_total/n_included)
    
    return idf

def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    #create a dict mapping a sentence to its match score
    f = dict()

    #iterate across all files and calculate their scores
    for file in files:
        #initialise score
        score = 0

        #iterate across all words in the query and check which of them are in the file
        #if a word is in a file, score += count(word)*idf(word)
        for word in query:
            if word in files[file]:
                score += files[file].count(word)*idfs[word]
    
        f[file] = score
    
    f_sorted = dict(sorted(f.items(), key=lambda x:x[1], reverse=True))

    # print(list(f_sorted.keys())[:n])

    return list(f_sorted.keys())[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    # initialise a dictionary with sentence scores
    sent_dict = dict()

    # iterate across all sentences
    for sent in sentences:
        score = 0
        query_density = 0
        # iterate for all words in the query
        for word in query:
            # if a word exists in the sentence, add its idf value to the score
            if word in sentences[sent]:
                score += idfs[word]
                query_density += 1/len(sent)
    
        sent_dict[sent] = (score, query_density)

    # print(sent_dict)

    # Now, figure out out top n sentences :)
    duplicate_sent_dict = sent_dict.copy()

    #initialise ans
    ans = []

    # Start a loop to pick out top n sentences
    for i in range(n):
        #initialise first key values
        pick_out = list(duplicate_sent_dict.keys())[0]
        max_score = duplicate_sent_dict[pick_out][0]
        max_density = duplicate_sent_dict[pick_out][1]

        #iterate to pick out the best sentence
        for sent in duplicate_sent_dict:
            if duplicate_sent_dict[sent][0] < max_score:
                continue
            elif duplicate_sent_dict[sent][0] > max_score:
                pick_out = sent
                max_score = duplicate_sent_dict[sent][0]
            elif duplicate_sent_dict[sent][0] == max_score:
                if duplicate_sent_dict[sent][1] > max_density:
                    pick_out = sent
                    max_score = duplicate_sent_dict[sent][0]
                    max_density = duplicate_sent_dict[sent][1]
                else:
                    continue
        
        # Add best sentence to the ans
        ans.append(pick_out)

        # Remove picked sentence from the copy dict so that loop finds second best sentence
        duplicate_sent_dict.pop(pick_out)
    
    return ans

if __name__ == "__main__":
    main()
