# -*- coding: utf-8 -*-
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

# # Recursion

# [Click here to run this chapter on Colab](https://colab.research.google.com/github/AllenDowney/DSIRP/blob/main/notebooks/recursion.ipynb)

# ## Example 1
#
# Here's an example of recursion from [this section of Think Python](https://greenteapress.com/thinkpython2/html/thinkpython2006.html#sec62).

# + tags=[]
from dsirp.helper_library.download import download


def countdown(n):
    if n == 0:
        print('Blastoff!')
    else:
        print(n)
        countdown(n - 1)


if __name__ == "__main__":

    # + tags=[]
    countdown(3)


    # -

    # To understand recursion, it's important to have a good mental model of what happens when you run a function:
    #
    # 1. Python interprets the arguments.
    #
    # 2. It creates a stack frame, which will contain the parameters and local variables.
    #
    # 3. Next it assigns the values of the arguments to the parameters.
    #
    # 4. Python runs the body of the function.
    #
    # 5. Then it recycles the stack frame.
    #
    # The runtime stack contains the stack frames of currently-running functions.

    # Here's a stack diagram that shows what happens when this `countdown` runs.
    #
    # <img src="https://greenteapress.com/thinkpython2/html/thinkpython2005.png">

    # **Exercise:** What happens if you run countdown with a negative number?  [See here for more info]()

    # ## Example 2
    #
    # Here's an example of recursion with a function that returns a value, from [this section of Think Python](https://greenteapress.com/thinkpython2/html/thinkpython2007.html#sec74).

    # + tags=[]
    def factorial(n):
        if n == 0:
            print(n, 1)
            return 1
        else:
            recurse = factorial(n - 1)
            result = n * recurse
            print(n, recurse, result)
            return result


    # + tags=[]
    factorial(3)


    # -

    # Here's the stack frame.

    # <img src="https://greenteapress.com/thinkpython2/html/thinkpython2007.png">

    # **Exercise:** Suppose you want to raise a number, `x`, to an integer power, `k`. An efficient way to do that is:
    #
    # * If `k` is even, raise `n` to `k/2` and square it.
    #
    # * If `k` is odd, raise `n` to `(k-1)/2`, square it, and multiply by `x` one more time.
    #
    # Write a recursive function that implements this algorithm.

    # What is the order of growth of this algorithm?
    # To keep it simple, suppose `k` is a power of two.
    # How many times do we have to divide `k` by two before we get to 1?
    #
    # Thinking about it in reverse, starting with 1, how many times do we have to double 1 before we get to `k`? In math notation, the question is
    #
    # $$2^y = k$$
    #
    # where `y` is the unknown number of steps. Taking the log of both sides, base 2:
    #
    # $$y = log_2 k$$
    #
    # In terms of order of growth, this algorithm is in `O(log k)`. We don't have to specify the base of the logarithm, because a log in one base is a constant multiple of a log in any other base.

    # ## Example 3
    #
    # Here's another example of recursion from [this section of Think Python](https://greenteapress.com/thinkpython2/html/thinkpython2007.html#sec76).

    # + tags=[]
    def fibonacci(n):
        print(n)
        if n == 0:
            return 0
        elif n == 1:
            return 1
        else:
            return fibonacci(n - 1) + fibonacci(n - 2)


    # + tags=[]
    fibonacci(4)
    # -

    # Here's a stack graph that shows all stack frames created during this function call.
    #
    # Note that these frames are not all on the stack at the same time.

    # <img src="https://greenteapress.com/thinkpython2/html/thinkpython2017.png">

    # Here's the [section from Think Python](https://greenteapress.com/thinkpython2/html/thinkpython2012.html#sec135) that shows how we can make fibonacci faster by "memoizing" it. That's not a typo; the word is really [memoize](https://en.wikipedia.org/wiki/Memoization).

    # + tags=[]
    known = {0: 0, 1: 1}


    def fibonacci_memo(n):
        if n in known:
            return known[n]

        print(n)
        res = fibonacci_memo(n - 1) + fibonacci_memo(n - 2)
        known[n] = res
        return res


    # + tags=[]
    fibonacci_memo(4)


    # -

    # **Exercise:** The [Ackermann function](http://en.wikipedia.org/wiki/Ackermann_function), $A(m, n)$, is defined:
    #
    # $$
    # A(m, n) = \begin{cases}
    #               n+1 & \mbox{if } m = 0 \\
    #         A(m-1, 1) & \mbox{if } m > 0 \mbox{ and } n = 0 \\
    # A(m-1, A(m, n-1)) & \mbox{if } m > 0 \mbox{ and } n > 0.
    # \end{cases}
    # $$
    #
    # Write a function named `ackermann` that evaluates the Ackermann function.
    # Use your function to evaluate `ackermann(3, 4)`, which should be 125.
    #
    # What happens for larger values of `m` and `n`?
    #
    # If you memoize it, can you evaluate the function with bigger values?

    # ## String functions
    #
    # Many things we do iteratively can be expressed recursively as well.

    # + tags=[]
    def reverse(s):
        if len(s) < 2:
            return s

        first, rest = s[0], s[1:]
        return reverse(rest) + first


    # + tags=[]
    reverse('reverse')
    # -

    # For sequences and mapping types, there's usually no advantage of the recursive version. But for trees and graphs, a recursive implementation can be clearer, more concise, and more demonstrably correct.

    # **Exercise:** Here's an exercise from, of all places, [StackOverflow](https://stackoverflow.com/questions/28977737/writing-a-recursive-string-function):
    #
    # > Write a recursive, string-valued function, `replace`, that accepts a string and returns a new string consisting of the original string with each blank replaced with an asterisk (*)
    # >
    # > Replacing the blanks in a string involves:
    # >
    # > 1. Nothing if the string is empty
    # >
    # > 2. Otherwise: If the first character is not a blank, simply concatenate it with the result of replacing the rest of the string
    # >
    # > 3. If the first character IS a blank, concatenate an * with the result of replacing the rest of the string
    #

    # ## Exercises

    # This one is from [Structure and Interpretation of Computer Programs](https://mitpress.mit.edu/sites/default/files/sicp/index.html):
    #
    # > The greatest common divisor (GCD) of two integers `a` and `b` is defined to be the largest integer that divides both `a` and `b` with no remainder. For example, the GCD of 16 and 28 is 4. [...] One way to find the GCD of two integers is to factor them and search for common factors, but there is a [famous algorithm](https://en.wikipedia.org/wiki/Euclidean_algorithm) that is much more efficient.
    # >
    # > The idea of the algorithm is based on the observation that, if `r` is the remainder when `a` is divided by `b`, then the common divisors of `a` and `b` are precisely the same as the common divisors of `b` and `r`.
    # >
    # > Thus, we can use the equation
    # >
    # > $$GCD(a, b) = GCD(b, r)$$
    # >
    # >to successively reduce the problem of computing a GCD to the problem of computing the GCD of smaller and smaller pairs of integers.
    # >
    # > It is possible to show that starting with any two positive integers and performing repeated reductions will always eventually produce a pair where the second number is 0. Then the GCD is the other number in the pair.
    #
    # Write a function called `gcd` that takes two integers and uses this algorithm to compute their greatest common divisor.

    # This one is from [Structure and Interpretation of Computer Programs](https://mitpress.mit.edu/sites/default/files/sicp/index.html):
    #
    # > How many different ways can we make change of \$1.00, given half-dollars, quarters, dimes, nickels, and pennies? [...]
    # >
    # >[...] Suppose we think of the types of coins available as arranged in some order. [..] observe that the ways to make change can be divided into two groups: those that do not use any of the first kind of coin, and those that do. Therefore, the total number of ways to make change for some amount is equal to the number of ways to make change for the amount without using any of the first kind of coin, plus the number of ways to make change assuming that we do use the first kind of coin.
    #
    # Write a function that takes as parameters an amount of money in cents and a sequence of coin denominations. It should return the number of combinations of coins that add up to the given amount.
    #
    # The result for one dollar (`100` cents) with coins of denominations `(50, 25, 10, 5, 1)` should be `292`.
    #
    # You might have to give some thought to the base cases.

    # **Exercise:** Here's one of my favorite Car Talk Puzzlers (http://www.cartalk.com/content/puzzlers):
    #
    # >What is the longest English word, that remains a valid English word, as you remove its letters one at a time?
    # >
    # >Now, letters can be removed from either end, or the middle, but you can’t rearrange any of the letters. Every time you drop a letter, you wind up with another English word. If you do that, you’re eventually going to wind up with one letter and that too is going to be an English word—one that’s found in the dictionary. I want to know what’s the longest word and how many letters does it have?
    # >
    # >I’m going to give you a little modest example: Sprite. Ok? You start off with sprite, you take a letter off, one from the interior of the word, take the r away, and we’re left with the word spite, then we take the e off the end, we’re left with spit, we take the s off, we’re left with pit, it, and I.
    #
    # Write a program to find all words that can be reduced in this way, and then find the longest one.
    #
    # This exercise is a little more challenging than most, so here are some suggestions:
    #
    # * You might want to write a function that takes a word and computes a list of all the words that can be formed by removing one letter. These are the “children” of the word.
    #
    # * Recursively, a word is reducible if any of its children are reducible. As base cases, you can consider the single letter words “I”, “a” to be reducible.
    #
    # * To improve the performance of your program, you might want to memoize the words that are known to be reducible.

    # +
    from os.path import basename, exists




    download('https://github.com/AllenDowney/DSIRP/raw/main/american-english')


    # -

    def read_words(filename):
        """Read lines from a file and split them into words."""
        res = set()
        for line in open(filename):
            for word in line.split():
                res.add(word.strip().lower())
        return res


    word_set = read_words('american-english')
    len(word_set)

    # + tags=[]

    # + tags=[]

    # + tags=[]

    # + tags=[]

    # + tags=[]

    # -

    # *Data Structures and Information Retrieval in Python*
    #
    # Copyright 2021 Allen Downey
    #
    # License: [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-nc-sa/4.0/)
