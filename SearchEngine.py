def get_page(url):
    try:
        import urllib
        return urllib.urlopen(url).read()
    except:
        return ""

#seed = 'https://www.udacity.com/cs101x/index.html'
seed = 'https://www.udacity.com/cs101x/urank/index.html'

def crawl_web(seed): # returns index, graph of outlinks
    tocrawl = [seed]
    crawled = []
    graph = {}  # <url>:[list of pages it links to]
    index = {} 
    while tocrawl: 
        page = tocrawl.pop()
        if page not in crawled:
            content = get_page(page)
            add_page_to_index(index, page, content)
            outlinks = get_all_links(content)
            graph[page] = outlinks;
            union(tocrawl, outlinks)
            crawled.append(page)
    return index, graph

def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1: 
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote

def get_all_links(page):
    links = []
    while True:
        url, endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links

def union(p,q):
    for e in q:
        if e not in p:
            p.append(e)

def add_page_to_index(index, url, content):
    words = content.split()
    for word in words:
        add_to_index(index, word, url)
        
def add_to_index(index, keyword, url):
    if keyword in index:
        index[keyword].append(url)
    else:
        index[keyword] = [url]

def lookup(index, keyword):
    if keyword in index:
        return index[keyword]
    else:
        return None

def compute_ranks(graph):
    D = 0.8 #damping factor
    N = len(graph)
    numloops = 10 #relaxation factor
    ranks = {}
    for page in graph:
        ranks[page] = 1.0 / N

    for i in range(0, numloops):
        newranks = {}
        for page in graph:
            newrank = (1 - D) / N
            for node in graph:
                if page in graph[node]:
                    newrank = newrank + D * (ranks[node] / len(graph[node]))
            newranks[page] = newrank
        ranks = newranks
    return ranks

def search(index, ranks, keyword):
    pages = lookup(index, keyword)
    if not pages:
        return None
    best_page = pages[0]
    for candidate in pages:
        if ranks[candidate] > ranks[best_page]:
            best_page = candidate
    return best_page

index, graph = crawl_web(seed)
ranks = compute_ranks(graph)
print ranks
