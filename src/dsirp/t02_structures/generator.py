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

# # Generators and Iterators

# [Click here to run this chapter on Colab](https://colab.research.google.com/github/AllenDowney/DSIRP/blob/main/notebooks/generator.ipynb)

# This chapter introduces generator functions, which are functions that yield a stream of values, rather than returning a single value.
#
# To demonstrate their use, we'll explore Cartesian products, permutations, and combinations, using playing cards as an example.

# ## Generators
#
# As a first example, we'll write a generator function that generates the playing cards in a standard 52-card deck.
# This example is inspired by an example in Peter Norvig's ["A Concrete Introduction to Probability (using Python)"](https://nbviewer.ipython.org/url/norvig.com/ipython/Probability.ipynb).
#
# Here are Unicode strings that represent the set of suits and the set of ranks.

suits = u'♠♥♦♣'
ranks = u'AKQJ⑽98765432'

# And here's a nested for loop that enumerates all pairings of a rank with a suit.


# This set of pairs is the [Cartesian product](https://en.wikipedia.org/wiki/Cartesian_product) of the set of ranks and the set of suits.
#
# The following function encapsulates the loops and uses the `yield` statement to generate a stream of cards.


# Because this function includes a `yield` statement, it is a generator function. When we call it, the return value is a generator object.


# The generator object is iterable, so we can use `next` to get the first element of the stream.


# The first time we call `next`, the function runs until it hits the `yield` statement.
# If we call `next` again, the function resumes from where it left off and runs until it hits the `yield` statement again. 


# Because `it` is iterable, we can use it in a for loop to enumerate the remaining pairs.


# When the flow of control reaches the end of the function, the generator object raises and exception, which causes the for loop to end.

# ## itertools
#
# The `itertools` library provides function for working with iterators, including `product`, which is a generator function that takes iterators as arguments at yields their Cartesian product.
# We'll use `itertools.product` in the next few sections; then we'll see how to implement it.
#
# Here's a loop that uses `itertools.product` to generate the playing cards again.


# **Exercise:** Encapsulate the previous loop in a generator function called `card_generator2` that yields the playing  cards. Then call your function and use it to print the cards.


# ## Enumerating all pairs
#
# Now that we have playing cards, let's deal a few hands. In fact, let's deal all the hands.
#
# First, I'll create two card generators.


# Now we can use `product` to generate all pairs of cards.


# To check whether it's working correctly, it will be useful to count the number of elements in an iterator, which is what `ilen` does.
# This idiom is discussed [on Stack Overflow](https://stackoverflow.com/questions/390852/is-there-any-built-in-way-to-get-the-length-of-an-iterable-in-python).


# Now we can use it to count the pairs of cards.

it1 = card_generator(ranks, suits)
it2 = card_generator(ranks, suits)
ilen(product(it1, it2))

# If things have gone according to plan, the number of pairs should be $52^2$.

52 ** 2

# Notice that we have to create new card iterators every time, because once they are used up, they behave like an empty list.
# Here's what happens if we try to use them again.

ilen(product(it1, it2))

# That's also why we had to create two card iterators.
# If you create one and try to use it twice, it doesn't work.

it = card_generator(ranks, suits)
ilen(product(it, it))

# However, you can get around this limitation by calling `product` with the `repeat` argument, which makes it possible to use a single iterator to generate a Cartesian product.

it = card_generator(ranks, suits)
ilen(product(it, repeat=2))

# ## Permutations
#
# In the previous section, you might have noticed that some of the hands we generated are impossible because they contain the same card more than once.
#
# One way to solve this problem is to generate all pairs and then eliminate the ones that contain duplicates.


# **Exercise:** Write a generator function called `permutations` that takes an iterator and and integer, `r`, as arguments. It should generate tuples that represent all subsets of the elements in the iterator with size `r` and no duplicates.
#
# Test your function by generating and printing all hands with two distinct cards.
# Then use `ilen` to count how many there are, and confirm that it's `52 * 51`.


# The `itertools` library provides a function called `permutations` that does the same thing.


# ## Combinations
#
# At this point we are generating legitimate hands in the sense that the same card never appears twice.
# But we end up generating the same hand more than once, in the sense that the order of the cards does not matter.
# So we consider `(card1, card2)` to be the same hand as `(card2, card1)`.
# To avoid that, we can generate all permutations and then filter out the ones that are not in sorted order.
#
# It doesn't really matter which order is considered "sorted"; it's just a way to choose one ordering we consider "canonical".
#
# That's what the following loop does.


# **Exercise:** Write a generator function called `combinations` that takes an iterator and and integer, `r`, as arguments. It should generate tuples that represent all *sorted* subsets of the elements in the iterator with size `r` and no duplicates.
#
# Test your function by generating and printing all hands with two distinct cards.
# Then use `ilen` to count how many there are, and confirm that it's `52 * 51 / 2`.


# The `itertools` library provides a function called `combinations` that does the same thing.


# ## Generating hands
#
# We can use `combinations ` to write a generator that yields all valid hands with `n` playing cards, where "valid" means that the cards are in sorted order with no duplicates.


ilen(hand_generator(2))

# If you ever find yourself looping through an iterator and yielding all of the elements, you can simplify the code using `yield from`.


ilen(hand_generator(2))

# Now let's see how many hands there are with 3, 4, and (maybe) 5 cards.

ilen(hand_generator(3))

ilen(hand_generator(4))


# I'm not patient enough to let this one finish.

# +
# ilen(hand_generator(5))
# -

# But if we only care about the number of combinations, we can use [`math.comb`](https://docs.python.org/3/library/math.html).


# ## How many flushes?
#
# In poker, a "flush" is a hand where all cards have the same suit.
# To check whether a hand is a flush, it is convenient to extract the suit part of the cards and make a set.


# **Exercise:** Write a function called `is_flush` that takes a hand as an argument and returns `True` if all cards are the same suit.
#
# Then write a generator function called `flush_generator` that takes an integer `n` and return all hands with `n` cards that are flushes.
#
# What fraction of hands with 3, 4, and 5 cards are flushes?


# ## Write your own product
#
# So far we've been using `itertools.product`, but in the same way we wrote `permutations` and `combinations`, we can write our own `product`.
#
# If there are only two iterators, we can do it with nested `for` loops.

def product2(it1, it2):
    for x in it1:
        for y in it2:
            yield x, y


# So we can generate the cards like this.

for t in product2(ranks, suits):
    card = ''.join(t)
    print(card, end=' ')

# Now, we might be tempted to write two-card hands like this.

# +
it1 = card_generator(ranks, suits)
it2 = card_generator(ranks, suits)

for hand in product2(it1, it2):
    print(hand)


# -

# But that doesn't work; it only generates the first 52 pairs.
# Before you go on, see if you can figure out why.
#
# We can solve this problem by making each iterator into a tuple; then we can loop through them more than once.
# The price we pay is that we have to store all of the elements of the iterators.

def product2(it1, it2):
    t1 = tuple(it1)
    t2 = tuple(it2)
    for x in t1:
        for y in t2:
            yield x, y


# This version of `product2` works if the arguments are iterators.

# +
it1 = card_generator(ranks, suits)
it2 = card_generator(ranks, suits)

for hand in product2(it1, it2):
    print(hand)

# +
it1 = card_generator(ranks, suits)
it2 = card_generator(ranks, suits)

ilen(product2(it1, it2))
# -

# Now let's take it up a notch. What if you want the product of more than two iterators.
# The version of `product` we got from `itertools` can handle this case.

# +
import itertools

for pair in itertools.product(range(2), range(3), range(4)):
    print(pair)
# -

# **Exercise:** Write a generator function that takes an arbitrary number of iterables and yields their Cartesian product. Compare the results to `itertools.product`.
#
# Hint: I found it easiest to write this recursively.


# + [markdown] tags=[]
# *Data Structures and Information Retrieval in Python*
#
# Copyright 2021 Allen Downey
#
# License: [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-nc-sa/4.0/)
