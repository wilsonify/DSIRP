def test_smoke():
    print("fire?")


def test_main():
    # # Sets

    # [Click here to run this chapter on Colab](https://colab.research.google.com/github/AllenDowney/DSIRP/blob/main/notebooks/set.ipynb)

    # ## Set operators and methods
    #
    # The following example is based on Luciano Ramalho's talk, [Set Practice: Learning from Python's set type](https://www.youtube.com/watch?v=tGAngdU_8D8).

    def fibonacci(stop):
        a, b = 0, 1
        while a < stop:
            yield a
            a, b = b, a + b

    f = {n for n in fibonacci(10)}
    f

    def primes(stop):
        m = {}
        q = 2
        while q < stop:
            if q not in m:
                yield q
                m[q * q] = [q]
            else:
                for p in m[q]:
                    m.setdefault(p + q, []).append(p)
                del m[q]
            q += 1

    p = {n for n in primes(10)}
    p

    # Checking membership is constant time.

    # + tags=[]
    8 in f

    # + tags=[]
    8 in p
    # -

    # Intersection is like AND: it returns elements in f AND in p.

    # + tags=[]
    f & p
    # -

    # Union is like OR: it returns elements in f OR in p.

    # + tags=[]
    f | p
    # -

    # Symmetric difference is like XOR: elements from `f` OR `p` but not both.

    # + tags=[]
    f ^ p
    # -

    # Here are the Fibonacci numbers that are not prime.

    # + tags=[]
    f - p
    # -

    # And the primes that are not Fibonacci numbers.

    # + tags=[]
    p - f
    # -

    # The comparison operators check for subset and superset relationships.
    #
    # The Fibonacci numbers are not a superset of the primes.

    # + tags=[]
    f >= p
    # -

    # And the primes are not a superset of the Fibonacci numbers.

    # + tags=[]
    p >= f
    # -

    # In that sense, sets are not like numbers: they are only [partially ordered](https://en.wikipedia.org/wiki/Partially_ordered_set).
    #
    # `f` is a superset of `{1, 2, 3}`

    # + tags=[]
    f >= {1, 2, 3}

    # + tags=[]
    p >= {1, 2, 3}
    # -

    # Sets provide methods as well as operators. Why?
    #
    # For one thing, the argument you pass to a method can be any iterable, not just a set.

    # + tags=[]
    try:
        f >= [1, 2, 3]
    except TypeError as e:
        print(e)

    # + tags=[]
    f.issuperset([1, 2, 3])
    # -

    # Methods also accept more than one argument:

    f.union([1, 2, 3], (3, 4, 5), {5, 6, 7}, {7: 'a', 8: 'b'})

    # If you don't have a set to start with, you can use an empty set.

    set().union([1, 2, 3], (3, 4, 5), {5, 6, 7}, {7: 'a', 8: 'b'})

    # One small syntax nuisance: `{1, 2, 3}` is a set, but `{}` is an empty dictionary.

    # ## Spelling Bee
    #
    # [The New York Times Spelling Bee](https://www.nytimes.com/puzzles/spelling-bee) is a daily puzzle where the goal is to spell as many words as possible using only the given set of seven letters.
    # For example, in a recent Spelling Bee, the available letters were `dehiklo`,
    # so you could spell "like" and "hold".
    #
    # You can use each of the letters more than once, so "hook" and "deed" would be allowed, too.
    #
    # To make it a little more interesting, one of the letters is special and must be included in every word.
    # In this example, the special letter is `o`, so "hood" would be allowed, but not "like".
    #
    # Each word you find scores points depending on it's length, which must be at least four letters.
    # A word that uses all of the letters is called a "pangram" and scores extra points.
    #
    # We'll use this puzzle to explore the use of Python sets.

    # Suppose we're given a word and we would like to know whether it can be spelled using only a given set of letters.
    # The following function solves this problem using string operations.

    def uses_only(word, letters):
        for letter in word:
            if letter not in letters:
                return False
        return True

    # If we find any letters in `word` that are not in the list of letters, we can return `False` immediately.
    # If we get through the word without finding any unavailable letters, we can return `True`.
    #
    # Let's try it out with some examples. In a recent Spelling Bee, the available letters were `dehiklo`.
    # Let's see what we can spell with them.

    letters = "dehiklo"
    uses_only('lode', letters)

    uses_only('implode', letters)

    # **Exercise:** It is possible to implement `uses_only` more concisely using set operations rather than list operations. [Read the documentation of the `set` class](https://docs.python.org/3/tutorial/datastructures.html#sets) and rewrite `uses_only` using sets.

    uses_only('lode', letters)

    uses_only('implode', letters)

    # ## Word list
    #
    # The following function downloads a list of about 100,000 words in American English.

    # +
    from os.path import basename, exists

    def download(url):
        filename = basename(url)
        if not exists(filename):
            from urllib.request import urlretrieve
            local, _ = urlretrieve(url, filename)
            print('Downloaded ' + local)

    download('https://github.com/AllenDowney/DSIRP/raw/main/american-english')
    # -

    # The file contains one word per line, so we can read the file and split it into a list of words like this:

    word_list = open('american-english').read().split()
    len(word_list)

    # **Exercise:** Write a loop that iterates through this word list and prints only words
    #
    # * With at least four letters,
    #
    # * That can be spelled using only the letters `dehiklo`, and
    #
    # * That include the letter `o`.

    # **Exercise:** Now let's check for pangrams.
    # Write a function called `uses_all` that takes two strings and returns `True` if the first string uses all of the letters in the second string.
    # Think about how to express this computation using set operations.
    #
    # Test your function with at least one case that returns `True` and one that returns `False`.

    # **Exercise:** Modify the previous loop to search the word list for pangrams using `uses_only` and `uses_all`.
    #
    # Or, as a bonus, write a function called `uses_all_and_only` that checks both conditions using a single `set` operation.

    # ## Leftovers
    #
    # So far we've been writing Boolean functions that test specific conditions, but if they return `False`, they don't explain why.
    # As an alternative to `uses_only`, we could write a function called `bad_letters` that takes a word and a set of letters, and returns a new string that contain the letters in words that are not available.  Let's call it `bad_letters`.

    def bad_letters(word, letters):
        return set(word) - set(letters)

    # Now if we run this function with an illegal word, it will tell us which letters in the word are not available.

    bad_letters('oilfield', letters)

    # **Exercise:** Write a function called `unused_letters` that takes a word and a set of letters and returns the subset of the letters that are not used in `word`.

    # **Exercise:** Write a function called `no_duplicates` that takes a string and returns `True` if each letter appears only once.

    # *Data Structures and Information Retrieval in Python*
    #
    # Copyright 2021 Allen Downey
    #
    # License: [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-nc-sa/4.0/)
