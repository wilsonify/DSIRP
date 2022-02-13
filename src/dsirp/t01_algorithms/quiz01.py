# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.11.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# # Quiz 1
#
# BEFORE YOU START THIS QUIZ:
#
# 1. Click on "Copy to Drive" to make a copy of the quiz,
#
# 2. Click on "Share",
#     
# 3. Click on "Change" and select "Anyone with this link can edit"
#     
# 4. Click "Copy link" and
#
# 5. Paste the link into [this Canvas assignment](https://canvas.olin.edu/courses/313/assignments/4866). 
#
# Copyright 2021 Allen Downey, [MIT License](http://opensource.org/licenses/MIT)

# ## Setup

# The following cells download a file that contains a list of words, reads the words, and stores them in a `set`.

# +
from os.path import basename, exists


def download(url):
    filename = basename(url)
    if not exists(filename):
        from urllib.request import urlretrieve
        local, _ = urlretrieve(url, filename)
        print('Downloaded ' + local)


if __name__ == "__main__":
    download('https://github.com/AllenDowney/DSIRP/raw/main/american-english')


    # -

    def read_words(filename):
        """Read lines from a file and split them into words."""
        res = set()
        for line in open(filename):
            for word in line.split():
                res.add(word.strip().lower())
        return res


    word_list = read_words('american-english')
    len(word_list)


    # ## Question 1
    #
    # The following function takes a string and returns `True` if the letters in the string appear in alphabetical order.

    def is_alphabetical(word):
        return list(word) == sorted(word)


    is_alphabetical('almost')  # True

    is_alphabetical('alphabetical')  # False

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

    def encompasses():
        """
        takes two words and returns `True` if the first word contains the second word,
        but not at the beginning or the end (and `False` otherwise).
        For example, `hippopotomus` encompasses the word `pot`.
        """
        return True


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
