# # Algorithms

# [Click here to run this chapter on Colab](https://colab.research.google.com/github/AllenDowney/DSIRP/blob/main/notebooks/algorithms.ipynb)

# ## Searching for anagrams
#
# In this notebook we'll implement algorithms for two tasks:
#
# * Testing a pair of words to see if they are anagrams of each other, that is, if you can rearrange the letters in one word to spell the other.
#
# * Searching a list of words for all pairs that are anagrams of each other.
#
# There is a point to these examples, which I will explain at the end.

# **Exercise 1:** Write a function that takes two words and returns `True` if they are anagrams. Test your function with the examples below.
from collections import defaultdict

from dsirp.helper_library.download import download


def is_anagram(word1, word2):
    """
    takes two words and returns `True` if they are anagrams.
    """
    return sorted(word1) == sorted(word2)


def all_anagram_pairs(word_list):
    """
    takes a word list and returns a list of all anagram pairs.
    """
    result = []
    for w1, w2 in zip(word_list, word_list):
        if is_anagram(w1, w2):
            result.append([w1, w2])
    return []


def read_words(filename):
    """Read lines from a file and split them into words."""
    res = set()
    for line in open(filename):
        for word in line.split():
            res.add(word.strip().lower())
    return list(res)


def all_anagram_lists(word_list):
    """
    Finds all anagrams in a list of words.
    word_list: sequence of strings
    """
    potential_anagrams = defaultdict(list)
    for word in word_list:
        for word2 in word_list:
            if word[0] in word2:
                potential_anagrams[word].append(word2)
    result = set([])
    for word1, word2 in potential_anagrams.items():
        if is_anagram(word1, word2):
            result.add((word1, word2))
    return list(result)


if __name__ == "__main__":
    is_anagram('tachymetric', 'mccarthyite')  # True

    is_anagram('post', 'top')  # False, letter not present

    is_anagram('pott', 'top')  # False, letter present but not enough copies

    is_anagram('top', 'post')  # False, letters left over at the end

    is_anagram('topss', 'postt')  # False

    # **Exercise 2:** Use `timeit` to see how fast your function is for these examples:

    is_anagram('tops', 'spot')

    is_anagram('tachymetric', 'mccarthyite')

    # NOTE: How can we compare algorithms running on different computers?

    # ## Searching for anagram pairs

    # **Exercise 3:** Write a function that takes a word list and returns a list of all anagram pairs.

    short_word_list = ['proudest', 'stop', 'pots', 'tops', 'sprouted']

    all_anagram_pairs(short_word_list)

    # The following cell downloads a file containing a list of English words.

    # +

    download('https://github.com/AllenDowney/DSIRP/raw/main/american-english')

    # -

    # The following function reads a file and returns a set of words (I used a set because after we convert words to lower case, there are some repeats.)

    word_list = read_words('american-english')
    len(word_list)

    # **Exercise 4:** Loop through the word list and print all words that are anagrams of `stop`.

    # Now run `all_anagram_pairs` with the full `word_list`:

    # +
    # pairs = all_anagram_pairs(word_list)
    # -

    # **Exercise 5:** While that's running, let's estimate how long it's going to take.

    # ## A better algorithm
    #
    # **Exercise 6:** Write a better algorithm! Hint: make a dictionary. How much faster is your algorithm?

    anagram_map = all_anagram_lists(word_list)

    len(anagram_map)

    # ## Summary
    #
    # What is the point of the examples in this notebook?
    #
    # * The different versions of `is_anagram` show that, when inputs are small, it is hard to say which algorithm will be the fastest. It often depends on details of the implementation. Anyway, the differences tend to be small, so it might not matter much in practice.
    #
    # * The different algorithms we used to search for anagram pairs show that, when inputs are large, we can often tell which algorithm will be fastest. And the difference between a fast algorithm and a slow one can be huge!

    # ## Exercises
    #
    # Before you work on these exercises, you might want to read the Python [Sorting How-To](https://docs.python.org/3/howto/sorting.html). It uses `lambda` to define an anonymous function, which [you can read about here](https://www.w3schools.com/python/python_lambda.asp).
    #
    # **Exercise 7:**
    # Make a dictionary like `anagram_map` that contains only keys that map to a list with more than one element. You can use a `for` loop to make a new dictionary, or a [dictionary comprehension](https://www.freecodecamp.org/news/dictionary-comprehension-in-python-explained-with-examples/).

    # **Exercise 8:**
    # Find the longest word with at least one anagram. Suggestion: use the `key` argument of `sort` or `sorted` ([see here](https://stackoverflow.com/questions/8966538/syntax-behind-sortedkey-lambda)).

    # **Exercise 9:**
    # Find the largest list of words that are anagrams of each other.

    # **Exercise 10:**
    # Write a function that takes an integer `word_length` and finds the longest list of words with the given length that are anagrams of each other.

    # **Exercise 11:**
    # At this point we have a data structure that contains lists of words that are anagrams, but we have not actually enumerated all pairs.
    # Write a function that takes `anagram_map` and returns a list of all anagram pairs.
    # How many are there?

    # *Data Structures and Information Retrieval in Python*
    #
    # Copyright 2021 Allen Downey
    #
    # License: [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-nc-sa/4.0/)
