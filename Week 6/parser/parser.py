import nltk
import sys
import re

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | S Conj S
NP -> N | N Conj NP | PP N | AdjP N | NP PP NP  
NP -> Det N | Det AdjP N | PP Det AdjP N | PP Det N
AdjP -> Adj | Adj AdjP
PP -> P | P PP
VP -> V | V NP | V Adv | VP Conj VP | Adv VP | V NP Adv
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)

chunks = []

def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

     # with open("sentences/3.txt") as f:
        # s = f.read()

    # Convert input into list of words
    s = preprocess(s)

    # print(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # print(trees)

    # for t in trees:
    #     print(t)
    #     t.pretty_print()

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    ans = nltk.tokenize.word_tokenize(sentence)
    removal = []
    for i in range(len(ans)):
        word = ans[i]
        # print(word)
        ans[i] = word.lower()
        # print(word)
        if not re.search('[a-zA-Z]', word):
            # print("isalpha condition")
            # print(word)
            removal.append(word)
    
    for word in removal:
        ans.remove(word)

    # print('inside the function')
    # print(ans)
    # print('done with function')
    
    return ans


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    for t in tree:
        if t.label() == "NP":
            if len(t) == 1:
                chunks.append(t)
            else:
                np_exist = False
                for sub in t:
                    if sub.label() == "NP":
                        np_exist = True
                        break
                
                if np_exist:
                    np_chunk(t)
                else:
                    chunks.append(t)
        else:
            if len(t) == 1:
                continue
            else:
                np_chunk(t)

    return chunks

if __name__ == "__main__":
    main()
