import lxml.html
import urllib.request ##get_page
from bs4 import BeautifulSoup
import re
from ranking import collection

def quicksort_pages(pages, ranks):
    if not pages or len(pages) <= 1:
        return pages
    else:
        pivot = ranks[pages[0]]
        bigger = []
        smaller = []
        for element in pages[1:]:
            if ranks[element] <= pivot:
                smaller.append(element)
            else:
                bigger.append(element)
        return quicksort_pages(bigger, ranks) + [pages[0]] + quicksort_pages(smaller, ranks)

def compute_rank(graph):
    d = 0.8
    numloops = 10

    ranks = {}
    npages = len(graph)
    for page in graph:
        ranks[page] = 1.0 / npages

    for i in range(0, numloops):
        newranks = {}
        for page in graph:
            newrank = (1 - d) / npages
            for node in graph:
                if page in graph[node]:
                    newrank = newrank + d * (ranks[node] / len(graph[node]))
            newranks[page] = newrank
        ranks = newranks
    return ranks


def order_search(keyword):
    graph = {}
    entry = collection.find_one({'keyword':keyword})
    
    
    if entry:
        for url in entry['url']:
            other_url = collection.find_one({'seed':url})
            if other_url:
                graph[url] = other_url['all_link']
        ranks = compute_rank(graph)
        pages = entry['url']
        return quicksort_pages(pages, ranks)
    else:
        return "nothing"
