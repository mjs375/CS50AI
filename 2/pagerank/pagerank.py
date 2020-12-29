# Usage: $ python pagerank.py [corpus]

import os
import random
import re
import sys

DAMPING = 0.85 #-- Damping Factor
SAMPLES = 10000 #-- Number of samples we'll use to estimate PageRank values


def main():
    #-- Cmd-line argument: which corpus to sample?:
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    #-- crawl() parses all HTML files, returns a dict of corpus (key=page, values=set of all linking pages):
    corpus = crawl(sys.argv[1])
    #
    #   T E S T I N G :
    #page = "2.html"
    page = random.choice(list(corpus))
    transition_model(corpus, page, DAMPING)
    #
    #
    #-- Estimate PageRank of each page by sampling:
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")

    #-- also calcs PageRank, but uses iterative formula instead:
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
    Return a probability distribution over which page to visit next, given a current page.

    With probability `damping_factor`, choose a link at random linked to by `page`. With probability `1 - damping_factor`, choose a link at random chosen from all pages in the corpus.

    CORPUS = {
        1.html: {2.html, 3.html},
        2.html: {3.html},
        3.html: {2.html}
             }
    Page = 1.html
    Damping = 0.85
    RETURN:
        1   0.15        } (everything else)
        2   0.425   } -  0.85 (D)
        3   0.425   } /
        -------------
            1.00

    """
    #-- Get linked pages of Page:
    linked = corpus[page]
    #print("\nPage:", page, "|", "Links:", linked)
    probs = dict()
    #-- If Page has no direct links, each page in corpus has equal prob:
    #-- OR if Page links to ALL other pages directly, all equal prob:
    if not linked or len(linked) == len(corpus):
        #-- Each page has equal probability:
        eq_prob = 1 / (len(corpus))
        #-- Loop to assign each corpus page the equal prob in a dict return:
        for key in corpus.keys():
            probs[key] = eq_prob
        #print("Probability:", probs, "\n")
        """ dict.fromkeys(corpus, eq_prob) """
    #-- If a mix of linked and (possibly) unlinked pages:
    else:
        #-- 0.85 / num of linked pages:
        link_prob = damping_factor / (len(linked))
        #-- 0.15 / num of unlinked pages:
        dry = 1 - damping_factor # 0.15
        unlinked_prob = dry / (len(corpus) - len(linked))
        #
        #
        for key in corpus.keys():
            if key in linked:
                probs[key] = link_prob
            else:
                probs[key] = unlinked_prob
    #
    #
    #print("Probability:", probs, "\n")
    return probs













def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages according to transition model, starting with a page at random. The 'random surfer' sampler method.

    Return a dictionary where keys are page names, and values are their estimated PageRank value (a value between 0 and 1). All PageRank values should sum to 1.
    """
    #-- Initialize dict of key[pagename] = value(0 tally to start)
    pagerank = {k:0 for k in corpus.keys()}
    #print("\nPAGERANK DICT:", pagerank, "\n")
    #-- Use random.choice to get randomized initial page
    page = random.choice(list(corpus.keys()))
    #print("PAGE:", page, type(page))
    #
    #-- Sample 'n' times: loop range(n):
    for i in range(n):
        #--Increment tally for page currently on:
        pagerank[page] += 1
        #--Use transition model to get next possible pages' probs:
        pages = transition_model(corpus, page, damping_factor)
        #--Choose a next page based on weighted probs:
        page = random.choices(list(pages.keys()), pages.values())[0]
    #
    #--Convert tallies to get PageRank number (proportion, 0-1):
    pagerank = {k: (v/n) for k, v in pagerank.items()}
    #
    #
    return pagerank














def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating PageRank values until convergence.

    Return a dictionary where keys are page names, and values are their estimated PageRank value (a value between 0 and 1). All PageRank values should sum to 1.
    """
    #--Number of webpages in corpus:
    N = len(corpus)
    #--Initialize pagerank dictionary
    pagerank = {k:(1/N) for k in corpus.keys()}
    #print("\nIterative PAGERANKS:", pagerank, "\n")
    #--Initialize check-switch if Pageranks still changing by more than 0.001:
    switch = True
    #
    #
    while switch:
        #--Batch update Pageranks (not 1-by-1):
        batch = {k:(1/N) for k in corpus.keys()}
        c = 0 # Tally to see if pageranks are still increasing by 0.001 or more.
        for page in corpus:
            #--Hold on to old pagerank value to check if still changing significantly (0.001 or more change):
            old_rank = pagerank[page]
            #
            """
            PR(p) =
                (1 - damping_factor) / total num of pages
                    +
                d *
                sigma( PR(i) / NumLinks(i) )
            """
            PR = (1 - damping_factor) / N
            #
            sigma = 0
            #--Sigma(sum) of all Pages(i) that Link TO Page(p):
            for i in corpus:
                #--Don't count page itself (if links to itself):
                if page in corpus[i] and i != page:
                    num_i = len(corpus[i])
                    sigma += pagerank[i] / num_i
            #--A Page that has no links at all should be interpreted as having one link for ever page in the corpus, incl itself:
                # ? ? ? ? ? ? ? ? ? ? ?
            #
            PR += sigma * damping_factor
            #--Set updated Pagerank for page in BATCH:
            batch[page] = PR # BIATCH UPDATE
            #
            #
            if abs(old_rank - PR) < 0.001:
                c += 1
        #
        #
        #--Update Pageranks to BatchRanks
        pagerank = batch
        #--If ALL Pageranks have NOT changed by more than 0.001, then end the Iteration, pagerank values have stabilized:
        if c == N:
            #--Exit while loop:
            switch = False
    #
    #
    #
    #
    return pagerank










if __name__ == "__main__":
    main()
