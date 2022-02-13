from dsirp.t05_keyvalue import indexer


def test_smoke():
    print("fire?")
    print(dir(indexer))


def test_main():
    # # Indexer

    # [Click here to run this chapter on Colab](https://colab.research.google.com/github/AllenDowney/DSIRP/blob/main/notebooks/indexer.ipynb)

    # + tags=[]
    from os.path import basename, exists

    def download(url):
        filename = basename(url)
        if not exists(filename):
            from urllib.request import urlretrieve
            local, _ = urlretrieve(url, filename)
            print('Downloaded ' + local)
        return filename

    # -

    # [Click here to run this chapter on Colab](https://colab.research.google.com/github/AllenDowney/DSIRP/blob/main/notebooks/indexer.ipynb)

    # ## Indexing the web
    #
    # In the context of web search, an index is a data structure that makes it possible to look up a search term and find the pages where that term appears. In addition, we would like to know how many times the search term appears on each page, which will help identify the pages most relevant to the term.
    #
    # For example, if a user submits the search terms "Python" and "programming", we would look up both search terms and get two sets of
    # pages. Pages with the word "Python" would include pages about the species of snake and pages about the programming language. Pages
    # with the word "programming" would include pages about different
    # programming languages, as well as other uses of the word. By selecting
    # pages with both terms, we hope to eliminate irrelevant pages and find
    # the ones about Python programming.

    # In order to make an index, we'll need to iterate through the words in a document and count them.
    # So that's where we'll start.
    #
    # Here's a minimal HTML document we have seen before, borrowed from the BeautifulSoup documentation.

    html_doc = """
    <html><head><title>The Dormouse's story</title></head>
    <body>
    <p class="title"><b>The Dormouse's story</b></p>
    
    <p class="story">Once upon a time there were three little sisters; and their names were
    <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
    <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
    <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
    and they lived at the bottom of a well.</p>
    
    <p class="story">...</p>
    """

    # We can use `BeautifulSoup` to parse the text and make a DOM.

    # +
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html_doc)
    type(soup)
    # -

    # The following is a generator function that iterates the elements of the DOM, finds the `NavigableString` objects, iterates through the words, and yields them one at a time.
    #
    # From each word, it removes the characters identified by the `string` module as whitespace or punctuation.

    # +
    from bs4 import NavigableString
    from string import whitespace, punctuation

    def iterate_words(soup):
        for element in soup.descendants:
            if isinstance(element, NavigableString):
                for word in element.string.split():
                    word = word.strip(whitespace + punctuation)
                    if word:
                        yield word.lower()

    # -

    # We can loop through the words like this:

    for word in iterate_words(soup):
        print(word)

    # And count them like this.

    # +
    from collections import Counter

    counter = Counter(iterate_words(soup))
    counter
    # -

    # ## Parsing Wikipedia
    #
    # Now let's do the same thing with the text of a Wikipedia page:

    url = "https://en.wikipedia.org/wiki/Python_(programming_language)"
    filename = basename(url)

    fp = open(filename)
    soup2 = BeautifulSoup(fp)

    counter = Counter(iterate_words(soup))
    counter.most_common(10)

    # As you might expect, the word "python" is one of the most common words on the Wikipedia page about Python.
    # The word "programming" didn't make the top 10, but it also appears many times.

    counter['programming']

    # However, there are a number of common words, like "the" and "from" that also appear many times.
    # Later, we'll come back and think about how to distinguish the words that really indicate what the page is about from the common words that appear on every page.
    #
    # But first, let's think about making an index.

    # ## Indexing
    #
    # An index is a map from a search word, like "python", to a collection of pages that contain the word.
    # The collection should also indicate how many times the word appears on each page.
    #
    # We want the index to be persistent, so we'll store it on Redis.
    #
    # So what Redis type should we use?
    # There are several options, but one reasonable choice is a hash for each word, where the fields are pages (represented by URL) and the values are counts.
    #
    # To manage the size of the index, we won't list a page for a given search word unless it appears at least three times.

    # Let's get Redis started.

    # +
    import sys

    IN_COLAB = 'google.colab' in sys.modules

    # !redis-server --daemonize yes

    # And make sure the Redis client is installed.

    # And let's make a `Redis` object that creates the connection to the Redis database.

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

    # **Exercise:** Write a function called `redis_index` that takes a URL and indexes it. It should download the web page with the given URL, iterate through the words, and make a `Counter` that maps from words to their frequencies.
    #
    # Then it should iterate through the words and add field-value pairs to Redis hashes.
    #
    # * The keys for the hashes should have the prefix `Index:`; for example, the key for the word `python` should be `Index:python`.
    #
    # * The fields in the hashes should be URLs.
    #
    # * The values in the hashes should be word counts.
    #
    # Use your function to index at least these two pages:

    url1 = 'https://en.wikipedia.org/wiki/Python_(programming_language)'
    url2 = 'https://en.wikipedia.org/wiki/Python_(genus)'

    # Use `hscan_iter` to iterate the field-values pairs in the index for the word `python`.
    # Print the URLs of the pages where this word appears and the number of times it appears on each page.

    # ## Shutdown
    #
    # If you are running this notebook on your own computer, you can use the following command to shut down the Redis server.
    #
    # If you are running on Colab, it's not really necessary: the Redis server will get shut down when the Colab runtime shuts down (and everything stored in it will disappear).

    # !killall redis-server

    # ## RedisToGo
    #
    # [RedisToGo](https://redistogo.com) is a hosting service that provides remote Redis databases.
    # They offer a free plan that includes a small database that is perfect for testing our indexer.
    #
    # If you sign up and go to your list of instances, you should find a URL that looks like this:
    #
    # ```
    # redis://redistogo:digitsandnumbers@dory.redistogo.com:10534/
    # ```
    #
    # If you pass this url to `Redis.from_url`, as described above, you should be able to connect to your database on RedisToGo and run your exercise solution again.
    #
    # And if you come back later and read the index, your data should still be there!

    # + [markdown] tags=[]
    # *Data Structures and Information Retrieval in Python*
    #
    # Copyright 2021 Allen Downey
    #
    # License: [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-nc-sa/4.0/)
