# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.11.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# # Crawler

# [Click here to run this chapter on Colab](https://colab.research.google.com/github/AllenDowney/DSIRP/blob/main/notebooks/crawler.ipynb)

# ## Crawling the web
#
# At this point we have all the pieces we need to build a web crawler; it's time to bring them together.
#
# First, from `philosophy.ipynb`, we have `WikiFetcher`, which we'll use to download pages from Wikipedia while limiting requests to about one per second.

# +
from urllib.request import urlopen
from bs4 import BeautifulSoup
from time import time, sleep
    
class WikiFetcher:
    next_request_time = None
    min_interval = 1  # second

    def fetch_wikipedia(self, url):
        self.sleep_if_needed()
        fp = urlopen(url)
        soup = BeautifulSoup(fp, 'html.parser')
        return soup

    def sleep_if_needed(self):
        if self.next_request_time:
            sleep_time = self.next_request_time - time()    
            if sleep_time > 0:
                sleep(sleep_time)
        
        self.next_request_time = time() + self.min_interval


# -

# Here's an example:

# +
fetcher = WikiFetcher()

url = 'https://en.wikipedia.org/wiki/Python_(programming_language)'
soup = fetcher.fetch_wikipedia(url)
# -

# The result is a BeautifulSoup object that represents the document object model (DOM) of the page.
#
# Note that `WikiFetcher` won't work if `url` is a bytearray, because `urlopen` doesn't work with bytearrays.

url = b'https://en.wikipedia.org/wiki/Python_(programming_language)'
# soup = fetcher.fetch_wikipedia(url)

# To convert a bytearray to a string, you have to decode it.

url_str = url.decode()
soup = fetcher.fetch_wikipedia(url_str)

# Usually when you call `decode`, you should [specify which encoding to use](https://docs.python.org/3.8/library/stdtypes.html#bytes.decode). But in this case we know that the original strings were URLs, so the default encoding will work.
#
# Wikipedia pages contain boilerplate content that we don't want to index, so we'll select the `div` element that contains the "body content" of the page.

root = soup.find(class_='mw-body-content')

# ## Finding links
#
# From `philosophy.ipynb`, we have the following function that traverses the DOM and finds links.

# +
from bs4 import Tag

def link_generator(root):
    for element in root.descendants:
        if isinstance(element, Tag) and element.name == 'a':
            href = element.get('href', '')
            if href.startswith('/wiki'):
                yield element


# -

# This version includes links to images and other links we probably don't want to index.
#
# The following version includes a condition that checks whether the link has a `title` attribute, which seems to select mostly "good" links.

def link_generator(root):
    for element in root.descendants:
        if isinstance(element, Tag) and element.name == 'a':
            title = element.get('title', '')
            href = element.get('href', '')
            if title and href.startswith('/wiki'):
                yield element


# Here are the first few links from the page we downloaded.

for i, link in enumerate(link_generator(root)):
    print(link)
    if i == 5:
        break

# ## Finding words
#
# From `indexer.ipynb`, we have the following function, which traverses the DOM and yields individual words, stripped of punctuation and converted to lowercase.

# +
from bs4 import NavigableString
from string import whitespace, punctuation

def iterate_words(root):
    for element in root.descendants:
        if isinstance(element, NavigableString):
            for word in element.string.split():
                word = word.strip(whitespace + punctuation)
                if word:
                    yield word.lower()


# -

# Here are the first words from the page we downloaded. They include keywords from the sidebar on the right side of the page, which are not part of the main text, but might be good to index anyway, since they indicate the topic of the page.

for i, word in enumerate(iterate_words(root)):
    print(word)
    if i > 200:
        break

# ## Redis
#
# Let's get Redis started.

# +
import sys

IN_COLAB = 'google.colab' in sys.modules

if IN_COLAB:
    # !pip install redis-server
    # !/usr/local/lib/python*/dist-packages/redis_server/bin/redis-server --daemonize yes
else:
    # !redis-server --daemonize yes
# -

# And make sure the Redis client is installed.

try:
    import redis
except ImportError:
    # !pip install redis

# We'll make a `Redis` object that creates the connection to the Redis database.

# +
import redis

r = redis.Redis()


# -

# If you have a Redis database running on a different machine, you can create a `Redis` object using the URL of the database, like this
#
# ```
# url = 'redis://redistogo:example@dory.redistogo.com:10534/'
# r = redis.Redis.from_url(url)
# ```

# If your database contains values from previous exercises, or if you make a mistake and want to start over, you can use the following function to clear the database.

# +
def clear_redis(r):
    for key in r.keys():
        r.delete(key)
        
# clear_redis(r)


# -

# ## Indexing
#
# From `indexer.ipynb`, here's the function that counts the words on a page and adds the results to a Redis hash.
#
# For each word, it creates or updates a hash in the database that maps from URLs to word counts. For example if the word `python` appears 428 times on a page, we could find the hash with key `Index:python` and add an entry that maps from the URL to the number 428.

# +
from bs4 import BeautifulSoup
from collections import Counter

def redis_index(root, url):
    counter = Counter(iterate_words(root))
    for word, count in counter.items():
        if count >= 3:
            key = f'Index:{word}'
            # print(key, count)
            r.hset(key, url, count)


# -

# The previous version is likely to be slow because it makes many small requests to the database.
# We can speed it up using a pipeline object, like this:

# + tags=[]
def redis_index_pipeline(root, url):
    counter = Counter(iterate_words(root))
    p = r.pipeline(transaction=False)
    for word, count in counter.items():
        if count >= 3:
            key = f'Index:{word}'
            # print(key, count)
            p.hset(key, url, count)
    p.execute()


# -

# Let's see which version is faster.

url = 'https://en.wikipedia.org/wiki/Python_(programming_language)'
soup = fetcher.fetch_wikipedia(url)
root = soup.find(class_='mw-body-content')

# %time redis_index(root, url)

# %time redis_index_pipeline(root, url)

# We can use `hscan_iter` to iterate the field-values pairs in the index for the word `python`, and print the URLs of the pages where this word appears and the number of times it appears on each page.

# +
key = f'Index:python'

for page, count in r.hscan_iter(key):
    print(page, count)
# -

# Notice that when we get the number back, it's a bytearray. If we want to work with it as a number, we have to convert back to int.

# ## Crawling
#
# In `philosophy.ipynb` we wrote a simple crawler that always follows the first link.

# +
from urllib.parse import urljoin

target = 'https://en.wikipedia.org/wiki/Philosophy'

def get_to_philosophy(url):
    visited = []
    
    for i in range(20):
        if url == target:
            print(f'Got there in {i} steps!')
            return visited
        
        if url in visited:
            raise ValueError(f'URL already visited {url}')
        else:
            print(url)
            visited.append(url)
            
        soup = fetcher.fetch_wikipedia(url)
        root = soup.find(class_='mw-body-content')
        link = next(link_generator(root))
        url = urljoin(url, link['href'])
        
    return visited


# -

get_to_philosophy(url)

# Now we want a crawler that runs a breadth-first search.
# Here's the implementation of BFS from `bfs.ipynb`:

# +
from collections import deque

def reachable_nodes_bfs(G, start):
    seen = set()
    queue = deque([start])
    while queue:
        node = queue.popleft()
        if node not in seen:
            seen.add(node)
            neighbors = set(G[node]) - seen
            queue.extend(neighbors)
    return seen
# -

#
# **Exercise:** Write a function called `crawl` that takes a starting URL as a parameter, and an optional number of pages to crawl.
#
# It should create a queue of URLs and work it's way through the queue, indexing pages as it goes and adding new links to the queue.
#
# For a first draft, I suggest using Python data structures to keep track of the queue and the set of URLs that have already been seen/indexed.
#
#



url = 'https://en.wikipedia.org/wiki/Python_(programming_language)'
seen = crawl(url)

key = 'Index:the'
for page, count in r.hscan_iter(key):
    print(page, count)

# For a second draft, consider storing these structures in Redis so they are persistent; that way, you can call `crawl` later and it will pick up from where it left off. Or you could have multiple crawlers running at the same time.
#
# Hint: When you read a URL from Redis, you might have to decode it to make a string.

# +
queue_key = 'Crawler:queue'

r.lpop(queue_key)

# +
seen_key = 'Crawler:seen'

r.sismember(seen_key, 'anything')
# -



url = 'https://en.wikipedia.org/wiki/Object-oriented_programming'
crawl_persistent(url)

r.smembers(seen_key)

r.lrange(queue_key, 0, -1)

crawl_persistent()

# ## Stop words
#
# The most common English words are likely to appear on every page.
# They don't indicate what the page is about, and we might not want to index them. Words that we don't index are sometimes called [stop words](https://en.wikipedia.org/wiki/Stop_word).
#
# Once you have indexed a few pages, use the index to identify the words that have appeared the most times, totaled across all pages.

# + tags=[]
word_key = 'Index:the'
r.hvals(word_key)

# + tags=[]
sum(int(x) for x in r.hvals(word_key))

# + tags=[]
counter = Counter()

for word_key in r.keys('Index*'):
    total = sum(int(x) for x in r.hvals(word_key))
    word = word_key.decode().split(':')[1]
    counter[word] = total

# + tags=[]
counter.most_common(20)
# -

# The following cells use the results to make a Zipf plot, which shows counts versus "rank" on a log-log scale (the most common word has rank 1, the next most common has rank 2, and so on).
#
# Zipf's law asserts that the distribution of word frequencies follows a power law, which implies that the Zipf plot is approximately a straight line.

# +
import numpy as np

res = []

for i, (word, count) in enumerate(counter.most_common()):
    res.append((i+1, count))
    
rank, count = np.transpose(res)

# +
import matplotlib.pyplot as plt

plt.plot(rank, count)
plt.xlabel('Rank')
plt.ylabel('Count')
plt.title('Zipf plot')
plt.xscale('log')
plt.yscale('log')
# -

# ## Shutdown
#
# If you are running this notebook on your own computer, you can use the following command to shut down the Redis server.
#
# If you are running on Colab, it's not really necessary: the Redis server will get shut down when the Colab runtime shuts down (and everything stored in it will disappear).

# !killall redis-server

# *Data Structures and Information Retrieval in Python*
#
# Copyright 2021 Allen Downey
#
# License: [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-nc-sa/4.0/)
