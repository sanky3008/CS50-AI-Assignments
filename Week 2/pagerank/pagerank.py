import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    # corpus = crawl('corpus2')

    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    # Get -> Number of keys, list of keys
    N = len(corpus)
    keys = [key for key in corpus]
    numlinks = len(corpus[page])

    # Create a dict
    tm = dict()

    # For each key, add it to the dict alongwith its probability
    for key in keys:
        tm[key] = 0
        tm[key] += (1-DAMPING)/N

        if key in corpus[page]:
            tm[key] += DAMPING/numlinks

    return tm

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    #Initiate samples array, pagerank dict, weights
    samples = []
    pagerank = dict()
    model = dict()
    N = len(corpus)

    for key in corpus.keys():
        model[key] = 1/N

    #Start generating samples in a loop
    for i in range(n):
        #Take out a sample from model
        sample = random.choices(list(model.keys()), weights = list(model.values()))
        #print(sample)

        #Add it to the samples array
        samples.append(sample[0])

        #Generate a transition model using this page
        model = transition_model(corpus, sample[0], DAMPING)

    #print(samples)
    
    #Calculate pagerank of each element from the samples array
    for key in corpus.keys():
        pagerank[key] = samples.count(key)/n

    #Return pagerank dict
    return pagerank

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    #initialise a pagerank dict & a check variable
    pagerank = dict()
    N = len(corpus)
    for keys in corpus.keys():
        pagerank[keys] = 1/N
    
    check = True

    #Start iterating in a do while loop on the check variable
    while check:
        check = False
        for key in corpus:

            newval = (1 - damping_factor)/N

            for page in corpus:
                if key in corpus[page]:
                    newval += damping_factor*(pagerank[page]/len(corpus[page]))
        

            if abs(newval - pagerank[key]) > 0.001:
                check = True
            
            pagerank[key] = newval

    #Return pagerank dict
    return pagerank


if __name__ == "__main__":
    main()
