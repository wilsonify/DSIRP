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

# # Depth First Search

# [Click here to run this chapter on Colab](https://colab.research.google.com/github/AllenDowney/DSIRP/blob/main/notebooks/dfs.ipynb)

# This notebook presents "depth first search" as a way to iterate through the nodes in a tree.
# This algorithm applies to any kind of tree, but since we need an example, we'll use BeautifulSoup, which is a Python module that reads HTML (and related languages) and builds a tree that represents the content.

# ## Using BeautifulSoup
#
# When you download a web page, the contents are written in HyperText Markup Language, aka HTML. 
# For example, here is a minimal HTML document, which I borrowed from the [BeautifulSoup documentation](https://beautiful-soup-4.readthedocs.io), but the text is from Lewis Carroll's [*Alice's Adventures in Wonderland*](https://www.gutenberg.org/files/11/11-h/11-h.htm).

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

# Here's how we use BeautifulSoup to read it.

# + tags=[]
from bs4 import BeautifulSoup

soup = BeautifulSoup(html_doc)
type(soup)
# -

# The result is a `BeautifulSoup` object that represents the root of the tree. If we display the soup, it reproduces the HTML.

# + tags=[]
soup
# -

# `prettify` uses indentation to show the structure of the document.

# + tags=[]
print(soup.prettify())
# -

# The `BeautifulSoup` object has a property called `children` that returns an iterator of the objects it contains.

# + tags=[]
soup.children
# -

# We can use a for loop to iterate through them.

# + tags=[]
for element in soup.children:
    print(type(element))
# -

# This soup contains only a single child, which is a `Tag`.
#
# `BeautifulSoup` also provides `contents`, which returns the children in the form of a list, which can be more convenient.

# + tags=[]
soup.contents
# -

# The only child is an HTML element that contains the whole document.
# Let's get just this element:

# + tags=[]
element = soup.contents[0]
element
# -

# The type of the element is `Tag`:

# + tags=[]
type(element)
# -

# And the name of the tag is `html`.

# + tags=[]
element.name
# -

# Now let's get the children of this top-level element:

# + tags=[]
children = element.contents
children
# -

# There are three elements in this list, but it's hard to read because when you print an element, it prints all of the HTML.
#
# I'll use the following function to print elements in a simple form.

# +
from bs4 import Tag, NavigableString

def print_element(element):
    if isinstance(element, Tag):
        print(f'{type(element).__name__}<{element.name}>')
    if isinstance(element, NavigableString):
        print(type(element).__name__)


# + tags=[]
print_element(element)


# -

# And the following function to print a list of elements.

def print_element_list(element_list):
    print('[')
    for element in element_list:
        print_element(element)
    print(']')


# + tags=[]
print_element_list(element.contents)
# -

# Now let's try navigating the tree. I'll start with the first child of `element`.

# + tags=[]
child = element.contents[0]
print_element(child)
# -

# And print its children.

# + tags=[]
print_element_list(child.contents)
# -

# Now let's get the first child of the first child.

# + tags=[]
grandchild = child.contents[0]
print_element(grandchild)

# + tags=[]
grandchild = child.contents[0]
print_element(grandchild)
# -

# And the first child of the first grandchild.

greatgrandchild = grandchild.contents[0]
print_element(greatgrandchild)

try:
    greatgrandchild.contents
except AttributeError as e:
    print('AttributeError:', e)

greatgrandchild


# `NavigableString` has no children, so we've come to the end of the road.
#
# In order to continue, we would have to backtrack to the grandchild and select the second child.
#
# Which means we have to keep track of which elements we have seen, in order to pick up where we left off.
#
# That's what depth-first search does.

# ## Depth-first search
#
# DFS starts at the root of the tree and selects the first child. If the
# child has children, it selects the first child again. When it gets to a
# node with no children, it backtracks, moving up the tree to the parent
# node, where it selects the next child if there is one; otherwise it
# backtracks again. When it has explored the last child of the root, it's
# done.
#
# There are two common ways to implement DFS, recursively and iteratively.
# The recursive implementation looks like this:

# + tags=[]
def recursive_DFS(element):
    if isinstance(element, NavigableString):
        print(element, end='')
        return

    for child in element.children:
        recursive_DFS(child)


# + tags=[]
recursive_DFS(soup)


# -

# Here is an iterative version of DFS that uses a list to represent a stack of elements:

# + tags=[]
def iterative_DFS(root):
    stack = [root]
    
    while(stack):
        element = stack.pop()
        if isinstance(element, NavigableString):
            print(element, end='')
        else:
            children = reversed(element.contents)
            stack.extend(children)


# -

# The parameter, `root`, is the root of the tree we want to traverse, so
# we start by creating the stack and pushing the root onto it.
#
# The loop continues until the stack is empty. Each time through, it pops
# a `PageElement` off the stack. If it gets a `NavigableString`, it prints the contents.
# Then it pushes the children onto the stack. In order to process the
# children in the right order, we have to push them onto the stack in
# reverse order.
#

# + tags=[]
iterative_DFS(soup)


# -

# **Exercise:** Write a function similar to `PageElement.find` that takes a `PageElement` and a tag name and returns the first tag with the given name. You can write it iteratively or recursively.
#
# Here's how to check whether a `PageElement` is a `Tag`.
#
# ```
# from bs4 import Tag
# isinstance(element, Tag)
# ```

def is_right_tag(element, tag_name):
    return (isinstance(element, Tag) and 
            element.name == tag_name)















# **Exercise:** Write a generator function similar to `PageElement.find_all` that takes a `PageElement` and a tag name and yields all tags with the given name. You can write it iteratively or recursively.











# *Data Structures and Information Retrieval in Python*
#
# Copyright 2021 Allen Downey
#
# License: [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-nc-sa/4.0/)
