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
    num_pages = len(corpus)
    probabilities = dict()

    if not corpus[page]:  
        for p in corpus:
            probabilities[p] = 1 / num_pages

    base_prob = (1 - damping_factor) / num_pages
    for p in corpus:
        probabilities[p] = base_prob

    link_prob= damping_factor / len(corpus[page])
    for p in corpus[page]:
        probabilities[p] += link_prob
    return probabilities

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_counts = {page: 0 for page in corpus}
    current_page = random.choice(list(corpus.keys()))
    page_counts[current_page] += 1
    for _ in range(1, n):
        probabilities = transition_model(corpus, current_page, damping_factor)
        current_page = random.choices(
            population=list(probabilities.keys()),
            weights=list(probabilities.values())
        )[0]
        page_counts[current_page] += 1
    # Normalize the counts to get probabilities
    for page in page_counts:
        page_counts[page] /= n
    return page_counts


def iterate_pagerank(corpus, damping_factor):
    N = len(corpus)
    pagerank = {page: 1 / N for page in corpus}

    while True:
        new_pagerank = {}

        for page in corpus:
            total = (1 - damping_factor) / N

            for posible_page, links in corpus.items():
                if len(links) == 0:
                    total += damping_factor * (pagerank[posible_page] / N)
                elif page in links:
                    total += damping_factor * (pagerank[posible_page] / len(links))

            new_pagerank[page] = total

        # تفقّد إضافة (for page in corpus) داخل دالة max
        max_change = max(
            abs(new_pagerank[page] - pagerank[page]) for page in corpus
        )

        pagerank = new_pagerank

        if max_change <= 0.001:
            break

    return pagerank
  
             
if __name__ == "__main__":
    main()
