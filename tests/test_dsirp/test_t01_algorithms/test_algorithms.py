from dsirp.t01_algorithms import algorithms
from dsirp.t01_algorithms.algorithms import is_anagram, all_anagram_pairs, all_anagram_lists


def test_smoke():
    print("fire?")
    print(dir(algorithms))


def test_is_anagram():
    assert is_anagram('tachymetric', 'mccarthyite')
    assert not is_anagram('post', 'top')  # letter not present
    assert not is_anagram('pott', 'top')  # letter present but not enough copies
    assert not is_anagram('top', 'post')  # letters left over at the end
    assert not is_anagram('topss', 'postt')  # False


def test_all_anagram_pairs_short():
    short_word_list = ['proudest', 'stop', 'pots', 'tops', 'sprouted']
    result = all_anagram_pairs(short_word_list)
    assert result == []


def test_readwords(word_list):
    assert len(word_list) == 100781


def test_all_anagram_pairs_long(word_list):
    pairs = all_anagram_pairs(word_list)
    assert len(pairs) == 10


def test_all_anagram_lists(word_list):
    anagram_map = all_anagram_lists(word_list[:1000])
    assert anagram_map == []


def test_ex7():
    """
    Make a dictionary like `anagram_map` that contains only keys that map to a list with more than one element. You can use a `for` loop to make a new dictionary, or a [dictionary comprehension](https://www.freecodecamp.org/news/dictionary-comprehension-in-python-explained-with-examples/).
    """


def test_ex8():
    """
    Find the longest word with at least one anagram. Suggestion: use the `key` argument of `sort` or `sorted` ([see here](https://stackoverflow.com/questions/8966538/syntax-behind-sortedkey-lambda)).
    """


def test_ex9():
    """
    Find the largest list of words that are anagrams of each other.
    """


def test_ex10():
    """
    Write a function that takes an integer `word_length` and finds the longest list of words with the given length that are anagrams of each other.
    """


def test_ex11():
    """
    At this point we have a data structure that contains lists of words that are anagrams, but we have not actually enumerated all pairs.
    Write a function that takes `anagram_map` and returns a list of all anagram pairs.
    How many are there?
    """
