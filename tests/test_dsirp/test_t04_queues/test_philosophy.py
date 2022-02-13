def test_smoke():
    print("fire?")


def test_main():
    # # Getting to Philosophy

    # [Click here to run this chapter on Colab](https://colab.research.google.com/github/AllenDowney/DSIRP/blob/main/notebooks/philosophy.ipynb)

    # # Getting to Philosophy
    #
    # The goal of this notebook is to develop a Web crawler that tests the
    # "Getting to Philosophy" conjecture. As explained on [this Wikipedia page](https://en.wikipedia.org/wiki/Wikipedia:Getting_to_Philosophy):
    #
    # > Clicking on the first link in the main text of an English Wikipedia article, and then repeating the process for subsequent articles, usually leads to the Philosophy article. In February 2016, this was true for 97% of all articles in Wikipedia...
    #
    # More specifically, the link can't be in parentheses or italics, and it can't be an external link, a link to the current page, or a link to a non-existent page.
    #
    # We'll use the `urllib` library to download Wikipedia pages and BeautifulSoup to parse HTML text and navigate the Document Object Model (DOM).

    # Before we start working with Wikipedia pages, let's warm up with a minimal HTML document, which I've adapted from the BeautifulSoup documentation.

    html_doc = """
    <html><head><title>The Dormouse's story</title></head>
    <body>
    <p class="title"><b>The Dormouse's story</b></p>
    
    <p class="story">Once upon a time there were three little sisters; and their names were
    (<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>),
    <i><a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and</i>
    <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
    and they lived at the bottom of a well.</p>
    
    <p class="story">...</p>
    """

    # This document contains three links, but the first one is in parentheses and the second is in italics, so the third is the link we would follow to get to philosophy.
    #
    # Here's how we parse this document and make a `BeautifulSoup` object.

    # +
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html_doc)
    type(soup)

    # -

    # To iterate through the elements in the DOM, we can write our own implementation of depth first search, like this:

    def iterative_DFS(root):
        stack = [root]

        while (stack):
            element = stack.pop()
            yield element

            children = getattr(element, "contents", [])
            stack.extend(reversed(children))

    # For example, we can iterate through the elements and print all `NavigableString` elements:

    # +
    from bs4 import NavigableString

    for element in iterative_DFS(soup):
        if isinstance(element, NavigableString):
            print(element.string, end='')
    # -

    # But we can also use `descendants`, which does the same thing.

    for element in soup.descendants:
        if isinstance(element, NavigableString):
            print(element.string, end='')

    # ## Checking for Parentheses
    #
    # One theory of software development suggests you should tackle the hardest problem first, because it will drive the design. Then you can figure out how to handle the easier problems.
    #
    # For "Getting to Philosophy", one of the harder problems is to figure out whether a link is in parentheses.
    # If you have a link, you could work your way outward looking for enclosing parentheses, but in a tree, that could get complicated.
    #
    # The alternative I chose is to iterate through the text in order, counting open and close parentheses, and yield links only if they are not enclosed.

    # + tags=[]
    from bs4 import Tag

    def link_generator(root):
        paren_stack = []

        for element in root.descendants:
            if isinstance(element, NavigableString):
                for char in element.string:
                    if char == '(':
                        paren_stack.append(char)
                    if char == ')':
                        paren_stack.pop()

            if isinstance(element, Tag) and element.name == "a":
                if len(paren_stack) == 0:
                    yield element

    # -

    # Now we can iterate through the links that are not in parentheses.

    # + tags=[]
    for link in link_generator(soup):
        print(link)
    # -

    # ## Checking for Italics
    #
    # To see whether a link is in italics, we can:
    #
    # 1) If its parent is a `Tag` with name `a`, it's in italics.
    #
    # 2) Otherwise we have to check the parent of the parent, and so on.
    #
    # 3) If we get to the root without finding an italics tag, it's not in italics.

    # For example, here's the first link from `link_generator`.

    link = next(link_generator(soup))
    link

    # Its parent is an italics tag.

    parent = link.parent
    isinstance(parent, Tag)

    parent.name

    # **Exercise:** Write a function called `in_italics` that takes an element and returns `True` if it is in italics.

    # Then write a more general function called `in_bad_element` that takes an element and returns `True` if:
    #
    # * The element or one of its ancestors has a "bad" tag name, like `i`, or
    #
    # * The element or one of its ancestors is a `div` whose `class` attribute contains a "bad" class name.
    #
    # We will need the general version of this function to exclude invalid links on Wikipedia pages.

    # ## Working with Wikipedia Pages
    #
    # Actual Wikipedia pages are more complicated that the simple example, so it will take some effort to understand their structure and make sure we select the right "first link".
    #
    # The following cell downloads the Wikipedia page on Python.

    # +
    from os.path import basename, exists

    def download(url):
        filename = basename(url)
        if not exists(filename):
            from urllib.request import urlretrieve
            local, _ = urlretrieve(url, filename)
            print('Downloaded ' + local)

    # -

    url = "https://en.wikipedia.org/wiki/Python_(programming_language)"
    #download(url)

    # Now we can parse it and make `soup`.

    filename = basename(url)
    fp = open(filename)
    soup2 = BeautifulSoup(fp)

    # If you use a web browser to view this page, and use the Inspect Element tool to explore the structure, you'll see that the body of the article is in a `div` element with the class name `mw-body-content`.
    #
    # We can use `find` to get this element, and we'll use it as the root for our searches.

    # + tags=[]
    root = soup2.find(class_='mw-body-content')
    # -

    # **Exercise:** Write a generator function called `valid_link_generator` that uses `link_generator` to find links that are not in parentheses; then it should filter out links that are not valid, including links that are in italics, links to external pages, etc.
    #
    # Test your function with a few different pages until it reliably finds the "first link" that seems most consistent with the spirit of the rules.

    # ## `WikiFetcher`
    #
    # When you write a Web crawler, it is easy to download too many pages too
    # fast, which might violate the terms of service for the server you are
    # downloading from. To avoid that, we'll use an object called
    # `WikiFetcher` that does two things:
    #
    # 1.  It encapsulates the code for downloading and parsing web pages.
    #
    # 2.  It measures the time between requests and, if we don't leave enough
    #     time between requests, it sleeps until a reasonable interval has
    #     elapsed. By default, the interval is one second.
    #
    # Here's the definition of `WikiFetcher`:

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

    # `fetch_wikipedia` takes a URL as a
    # `String` and returns a BeautifulSoup object that represents the contents of the page.
    #
    # `sleep_if_needed` checks the time since the last
    # request and sleeps if the elapsed time is less than `min_interval`.
    #
    # Here's an example that demonstrates how it's used:

    # +
    wf = WikiFetcher()
    url = "https://en.wikipedia.org/wiki/Python_(programming_language)"

    print(time())
    wf.fetch_wikipedia(url)
    print(time())
    wf.fetch_wikipedia(url)
    print(time())
    # -

    # If things have gone according to plan, the three timestamps should be no less than 1 second apart, which is consistent with the terms in Wikipedia's [robots.txt](https://en.wikipedia.org/robots.txt):
    #
    # > Friendly, low-speed bots are welcome viewing article pages, but not
    # dynamically-generated pages please.

    # **Exercise:** Now let's pull it all together. Write a function called `get_to_philosophy` that takes as a parameter the URL of a Wikipedia page. It should:
    #
    # 1.  Use the `WikiFetcher` object we just created to download and parse the page.
    #
    # 2.  Traverse the resulting `BeautifulSoup` object to find the first valid link according to the spirit of the rules.
    #
    # 3.  If the page has no links, or if the first link is a page we have already seen, the program should indicate failure and exit.
    #
    # 4.  If the link matches the URL of the Wikipedia page on philosophy, the program should indicate success and exit.
    #
    # 5.  Otherwise it should go back to Step 1 (although you might want to put a limit on the number of hops).
    #
    # The program should build a list of the URLs it visits and display the
    # results at the end (whether it succeeds or fails).
    #
    # Since the links you find are relative, you might find the `urljoin` function helpful:

    # +
    from urllib.parse import urljoin

    url = "https://en.wikipedia.org/wiki/Python_(programming_language)"
    relative_path = "/wiki/Interpreted_language"

    urljoin(url, relative_path)
    # -

    get_to_philosophy(url)

    # + [markdown] tags=[]
    # *Data Structures and Information Retrieval in Python*
    #
    # Copyright 2021 Allen Downey
    #
    # License: [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-nc-sa/4.0/)
