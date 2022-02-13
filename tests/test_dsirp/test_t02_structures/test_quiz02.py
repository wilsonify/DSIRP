def test_smoke():
    print("fire?")


def test_main():
    # # Quiz 2
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
    # 5. Paste the link into [this Canvas assignment](https://canvas.olin.edu/courses/313/assignments/4929).
    #
    # This quiz is open notes, open internet. The only thing you can't do is ask for help.
    #
    # Copyright 2021 Allen Downey, [MIT License](http://opensource.org/licenses/MIT)

    # ## Question 1
    #
    # Suppose you have a function that takes a lot of options; some are required and some are optional.
    #
    # Before you run the function, you might want to check that:
    #
    # 1. All required options are provided, and
    #
    # 2. No illegal options are provided.
    #
    # For example, suppose this dictionary contains the provided options and their values:

    options = dict(a=1, b=2)
    options

    # And suppose that only `a` is required.

    required = ['a']

    # And the optional arguments are `b`, and `c`:

    optional = ['b', 'c']

    # An option is legal if it is required or optional. All other options are illegal.
    #
    # Write a function called `check_options` that takes a dictionary of options and their values, a sequence of required options, and a sequence of options that are legal but not required.
    #
    # 1. It should check that all required options are provided and, if not, print an error message that lists the ones that are missing.
    #
    # 2. It should check that all provided options are legal and, if not, print an error message that lists the ones that are illegal.
    #
    # For full credit, you must use set operations when they are appropriate rather than writing `for` loops.

    # The following test should display nothing because the dictionary contains all required options and no illegal ones.

    options = dict(a=1, b=2)
    check_options(options, required, optional)

    # The following test should print an error message because the dictionary is missing a required option.

    options = dict(b=2, c=3)
    check_options(options, required, optional)

    # The following test should display an error message because the dictionary contains an illegal option.

    options = dict(a=1, b=2, d=4)
    check_options(options, required, optional)

    # ## Question 2
    #
    # The set method `symmetric_difference` operates on two sets and computes the set of elements that appear in either set but not both.

    # +
    s1 = {1, 2}
    s2 = {2, 3}

    s1.symmetric_difference(s2)
    # -

    # The symmetric difference operation is also defined for more that two sets. It computes **the set of elements that appear in an odd number of sets**.
    #
    # The `symmetric_difference` method can only handle two sets (unlike some of the other set methods), but you can chain the method like this:

    s3 = {3, 4}
    s1.symmetric_difference(s2).symmetric_difference(s3)

    # However, for the sake of the exercise, let's suppose we don't have the set method `symmetric_difference` the equivalent `^` operator.
    #
    # Write a function that takes a list of sets as a parameter, computes their symmetric difference, and returns the result as a `set`.

    # Use the following tests to check your function.

    symmetric_difference([s1, s2])  # should be {1, 3}

    symmetric_difference([s2, s3])  # should be {2, 4}

    symmetric_difference([s1, s2, s3])  # should be {1, 4}

    # ## Question 3
    #
    # Write a generator function called `evens_and_odds` that takes a list of integers and yields:
    #
    # * All of the elements of the list that are even, followed by
    #
    # * All of the elements of the list that are odd.
    #
    # For example, if the list is `[1, 2, 4, 7]`, the sequence of values generated should be `2, 4, 1, 7`.

    # Use this example to test your function.

    # +
    t = [1, 2, 4, 7]

    for x in evens_and_odds(t):
        print(x)
    # -

    # As a challenge, JUST FOR FUN, write a version of this function that works if the argument is an iterator that you can only iterate once.

    # ## Question 4
    #
    # The following string contains the lyrics of a [well-known song](https://youtu.be/dQw4w9WgXcQ?t=43).

    lyrics = """
    Never gonna give you up
    Never gonna let you down
    Never gonna run around and desert you
    Never gonna make you cry
    Never gonna say goodbye
    Never gonna tell a lie and hurt you 
    """

    # The following generator function yields the words in `lyrics` one at a time.

    def generate_lyrics(lyrics):
        for word in lyrics.split():
            yield word

    # Write a few lines of code that use `generate_lyrics` to iterate through the words **only once** and build a dictionary that maps from each word to the set of words that follow it.
    #
    # For example, the first two entries in the dictionary should be
    #
    # ```
    # {'Never': {'gonna'},
    #  'gonna': {'give', 'let', 'make', 'run', 'say', 'tell'},
    #  ...
    # ```
    #
    # because in `lyrics`, the word "Never" is always followed by "gonna", and the word "gonna" is followed by six different words.
