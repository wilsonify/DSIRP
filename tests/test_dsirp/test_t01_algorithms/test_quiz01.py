import os.path

import pytest

from dsirp.t01_algorithms import quiz01
from dsirp.t01_algorithms.algorithms import read_words

current_file = os.path.abspath(__file__)
test_dir, current_tail = os.path.split(current_file)
test_head, test_tail = os.path.split(test_dir)
top_test_dir, test_head_tail = os.path.split(test_head)
data_dir = os.path.join(top_test_dir, "data")


@pytest.fixture(name="word_list")
def word_list_fixture():
    return read_words(f"{data_dir}/american-english")


def test_smoke():
    print("fire?")
    print(dir(quiz01))
    print(f"current_file = {current_file}")
    print(f"test_dir = {test_dir}")
    print(f"top_test_dir = {top_test_dir}")
    print(f"data_dir = {data_dir}")


def test_read_words(word_list):
    assert len(word_list) == 100781

def test_is_alphabetical():
    assert is_alphabetical('almost')
    assert not is_alphabetical('alphabetical')

def test_main(word_list):
    # The following function takes a string and returns `True` if the letters in the string appear in alphabetical order.



    # Make a new list called `alpha_words` that contains only the words in `word_list` that are alphabetical, and display the length of the list.

    # ## Question 2
    #
    # Find and display the longest word in `alpha_words`.
    # If there is more than one word with the maximal length, you can display any one of them (but only one).
    #
    # NOTE: You can write code for this question even if your answer to the previous question doesn't work. I'll grade the code, not the output.

    # ## Question 3
    #
    # Write a function called `encompasses` that takes two words and returns `True` if the first word contains the second word, but not at the beginning or the end (and `False` otherwise). For example, `hippopotomus` encompasses the word `pot`.
    #
    # HINT: You might find the string method `find` useful.

    'hippopotomus'.find('pot')

    'hippopotomus'.find('potato')

    def encompasses(word1, word2):
        """
        takes two words and returns `True` if the first word contains the second word,
        but not at the beginning or the end (and `False` otherwise).
        For example, `hippopotomus` encompasses the word `pot`.
        """
        return word1.__contains__(word2)

    # You can use the following examples to test your function.

    word1 = 'hippopotamus'
    word2 = 'pot'
    word3 = 'hippo'
    word4 = 'mus'
    word5 = 'potato'

    encompasses(word1, word2)  # True

    encompasses(word1, word3)  # False because word3 is at the beginning

    encompasses(word1, word4)  # False because word4 is at the end

    encompasses(word1, word5)  # False because word5 is not in word1

    # ## Question 4
    #
    # Two words make a "reverse pair" if one of them is the reverse of the other. For example, `pots` and `stop` are a reverse pair.
    #
    # The words in a reverse pair must be different, so `gag` and `gag` are not a reverse pair.
    #
    #
    # Make a list of all reverse pairs in `word_list`. Each pair of words should appear only once, so if `('tons', 'snot')` is in the list, `('snot', 'tons')` should not be.
    #

    # BONUS QUESTION JUST FOR FUN: What is the longest reverse pair in this word list?
