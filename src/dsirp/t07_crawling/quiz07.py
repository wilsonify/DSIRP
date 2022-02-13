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

# # Quiz 7
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
# 5. Paste the link into [this Canvas assignment](https://canvas.olin.edu/courses/313/assignments/5183). 

# This quiz is open notes, open internet. 
#
# * You can ask for help from the instructor, but not from anyone else.
#
# * You can use code you find on the internet, but if you use more than a couple of lines from a single source, you should attribute the source.
#
#

# ## Question 1
#
# A certain function is defined recursively like this:
#
# $$ f(n, m) = f(n-1, m-1) + f(n-1, m) $$
#
# with two special cases: if $m=0$ or $m=n$, the value of the function is 1.
#
# Write a (Python) function called `f` that computes this (mathematical) function.


# You can use the following examples to test your function.

assert f(2, 1) == 2

assert f(4, 1) == 4

assert f(4, 2) == 6

assert f(5, 3) == 10

assert f(10, 5) == 252

# If you try to run the following example, you will find that it runs for a long time.

# +
# f(100, 50)
# -

# ## Question 2
#
# Write a version of `f` called `f_memo` that uses an appropriate Python data structure to "memoize" `f`.
# In other words, you should keep a record of results you have already computed and look them up rather than compute them again.
#
# There's an example of memoization in recursion.ipynb.


# You can use this example to confirm that the function still works.

f_memo(10, 5)

# And use this one to confirm that it is faster.
# It should take less than a second, and the result should be `100891344545564193334812497256`.

f_memo(100, 50)


# ## LetterSet
#
# The next two questions are based on a set implementation I'll call a `LetterSet`.
#
# > Note: In this problem statement, "set" refers to the concept of a set, not the Python object called `set`.
# We won't use any Python `set` objects in these problems.
#
# If you know ahead of time what elements can appear in a set, you can represent the set efficiently using a [bit array](https://en.wikipedia.org/wiki/Bit_array).
# For example, to represent a set of letters, you can use a list of 26 Boolean values, one for each letter in the Roman alphabet (ignoring upper and lower case).
#
# Here's a class definition for this representation of a set.

class LetterSet:
    def __init__(self, bits=None):
        if bits is None:
            bits = [False] * 26
        self.bits = bits

    def __repr__(self):
        return f'LetterSet({repr(self.bits)})'


if __name__ == "__main__":
    # If all of the elements in the list are False, the set is empty.

    set1 = LetterSet()
    set1


    # To add a letter to a set, we have to compute the index that corresponds to a given letter.
    # The following function uses `ord`, which is a built-in Python function, to compute the index of a given letter.

    def get_index(letter):
        return ord(letter.lower()) - ord('a')


    # The index of `a` is 0, and the index of `Z` is 25.

    get_index('a'), get_index('Z')


    # To add a letter, we set the corresponding element of the list to `True`.

    def add(ls, letter):
        ls.bits[get_index(letter)] = True


    add(set1, 'a')
    add(set1, 'Z')
    set1


    # To count the elements of a set, we can use the built-in `sum` function:

    def size(ls):
        return sum(ls.bits)


    size(set1)

    # ## Question 3
    #
    # Write a function called `is_in` that takes a set and a letter and returns `True` if the letter is in the set.
    # In a comment, identify the order of growth of this function.

    #
    # Use the following examples to test your code.

    is_in(set1, 'a'), is_in(set1, 'b')

    # ## Question 4
    #
    # Write a function called `intersect` that takes two `LetterSet` objects and returns a new `LetterSet` that represents the intersection of the two sets.
    # In other words, the new `LetterSet` should contain only elements that appear in both sets.
    #
    # In a comment, identify the order of growth of this function.

    # Use the following examples to test your code.

    intersect(set1, set1)

    set2 = LetterSet()
    add(set2, 'a')
    add(set2, 'b')

    set3 = intersect(set1, set2)
    set3

    size(set3)


    # ## Just for fun bonus question
    #
    # One way to represent large numbers is to use a linked list where each node contains a digit.
    #
    # Here are class definitions for `DigitList`, which represents a list of digits, and `Node`, which contains one digit and a reference to the next `Node` in the list.

    class DigitList:
        def __init__(self, head=None):
            self.head = head


    class Node:
        def __init__(self, data=None, next=None):
            self.data = data
            self.next = next


    # In a `DigitList`, digits are stored in reverse order, so a list that contains the digits `1`, `2`, and `3`, in that order, represents the number `321`.

    head = Node(1, Node(2, Node(3, None)))
    head

    dl321 = DigitList(head)
    dl321


    # The following function takes a `DigitList` and prints the digits in reverse order.

    # +
    def print_dl(dl):
        print_dl_rec(dl.head)
        print()


    def print_dl_rec(node):
        if node is not None:
            print_dl_rec(node.next)
            print(node.data, end='')


    # -

    print_dl(dl321)

    head = Node(4, Node(5, Node(6, None)))
    dl654 = DigitList(head)
    print_dl(dl654)

    # Write a function called `add` that takes two `DigitList` objects and returns a new `DigitList` that represents their sum.

    divmod(11, 10)

    # You can use the following examples to test your code.

    total = add(dl321, dl654)
    print_dl(total)
    321 + 654

    head = Node(7, Node(8, None))
    dl87 = DigitList(head)
    print_dl(dl87)

    print_dl(add(dl654, dl87))
    654 + 87

    print_dl(add(dl87, dl654))
    87 + 654

    zero = DigitList(None)
    print_dl(add(dl87, zero))
    87 + 0

    print_dl(add(zero, dl87))
    0 + 87

    # *Data Structures and Information Retrieval in Python*
    #
    # Copyright 2021 Allen Downey
    #
    # License: [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-nc-sa/4.0/)
