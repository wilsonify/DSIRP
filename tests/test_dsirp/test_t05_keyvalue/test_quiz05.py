from dsirp.t05_keyvalue import quiz05


def test_smoke():
    print("fire?")
    print(dir(quiz05))


def test_main():
    # # Quiz 5
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
    # 5. Paste the link into [this Canvas assignment](https://canvas.olin.edu/courses/313/assignments/5075).

    # This quiz is open notes, open internet.
    #
    # * You can ask for help from the instructor, but not from anyone else.
    #
    # * You can use code you find on the internet, but if you use more than a couple of lines from a single source, you should attribute the source.
    #
    #

    # ## Install and Start Redis
    #
    # For this quiz, we will run Redis on Colab. The following cells install and start the server, install the client, and instantiate a `Redis` object.

    # +
    import sys

    IN_COLAB = 'google.colab' in sys.modules

    # !redis-server --daemonize yes

    # +
    import redis

    r = redis.Redis()
    # -

    # ## Linda the Banker
    #
    # In a [famous experiment](https://en.wikipedia.org/wiki/Conjunction_fallacy), Tversky and Kahneman posed the following question:
    #
    # > Linda is 31 years old, single, outspoken, and very bright. She majored in philosophy. As a student, she was deeply concerned with issues of discrimination and social justice, and also participated in anti-nuclear demonstrations.  Which is more probable?
    # > 1. Linda is a bank teller.
    # > 2. Linda is a bank teller and is active in the feminist movement.
    #
    # Many people choose the second answer, presumably because it seems more consistent with the description.  It seems uncharacteristic if Linda is *just* a bank teller; it seems more consistent if she is also a feminist.

    # But the second answer cannot be "more probable", as the question asks.
    # To see why, let's explore some data.
    # The following cell downloads data from the [General Social Survey](http://www.gss.norc.org/).

    # +
    from os.path import basename, exists


    # download('https://github.com/AllenDowney/BiteSizeBayes/raw/master/gss_bayes.csv')
    # -

    # The following cell loads the data into a Pandas `DataFrame`. If you are not familiar with Pandas, I will explain what you need to know.

    # +
    import pandas as pd

    gss = pd.read_csv('gss_bayes.csv', index_col=0)
    gss.index = pd.Index(range(len(gss)), name='caseid')
    gss.head()
    # -

    # The `DataFrame` has one row for each person surveyed, called a "respondent", and one column for each variable I selected.
    # The columns are:
    #
    # * `caseid`: Identification number for the respondent.
    #
    # * `year`: Year when the respondent was surveyed.
    #
    # * `age`: Respondent's age when surveyed.
    #
    # * `sex`: Male or female.
    #
    # * `polviews`: Political views on a range from liberal to conservative.
    #
    # * `partyid`: Political party affiliation, Democrat, Independent, or Republican.
    #
    # * `indus10`: [Code](https://www.census.gov/cgi-bin/sssd/naics/naicsrch?chart=2007) for the industry the respondent works in.

    # We will use Redis sets to explore the relationships among these variables.
    # Specifically, we will answer the following questions related to the "Linda problem".
    #
    # * The number of respondents who are female bankers,
    #
    # * The number of respondents who are liberal female banker.
    #
    # And we will see that the second number is smaller than the first.

    # ## Iterating rows
    #
    # The following loop iterates the first 3 rows in the `DataFrame` and prints the `caseid` and the contents of the row.

    # + tags=[]
    for caseid, row in gss.iterrows():
        print(caseid)
        print(row)
        if caseid >= 3:
            break
    # -

    # The following loop iterates through the `DataFrame` and makes a set containing the `caseid` for the rows where the industry code is 6870, which indicates that the respondent works in banking.

    # + tags=[]
    bankers = set()

    for caseid, row in gss.iterrows():
        if row.indus10 == 6870:
            bankers.add(caseid)

    len(bankers)
    # -

    # Now let's do the same thing using a Redis set.

    # ## Question 1
    #
    # The following loop creates a Redis set that contains the `caseid` for all respondents whose `indus10` is `6870`.

    # + tags=[]
    banker_key = 'gss_set:bankers'

    for caseid, row in gss.iterrows():
        if row.indus10 == 6870:
            r.sadd(banker_key, caseid)
    # -

    # Write a Redis command to get the number of elements in the resulting set.
    #
    # Here's the [documentation for Redis set commands](https://redis.io/commands#set).
    #

    # + tags=[]

    # -

    # ## Question 2
    #
    # The following cell makes a Python set that contains the `caseid` of all respondents who identify as female.

    # + tags=[]
    female = set()

    for caseid, row in gss.iterrows():
        if row.sex == 2:
            female.add(caseid)

    len(female)
    # -

    # The following cell makes a Python set that includes the `caseid` for people who self-identify as "Extremely liberal", "Liberal", or "Slightly liberal".

    # + tags=[]
    liberal = set()

    for caseid, row in gss.iterrows():
        if row.polviews <= 3:
            liberal.add(caseid)

    len(liberal)
    # -

    # Write versions of these loops that create these sets on Redis, and display the number of elements in each set.
    # For the keys, use the following strings:

    # + tags=[]
    female_key = 'gss_set:female'
    liberal_key = 'gss_set:liberal'

    # + tags=[]

    # + tags=[]

    # -

    # Before you go on, make sure you have three sets on Redis, and the number of elements in each set is consistent with the results we got with Python sets.
    #
    # If you make a mistake, you can use `delete` to start with a fresh, empty set.
    # Or you can use the following loop to start with a fresh, empty database.

    # +
    # for key in r.keys():
    #    r.delete(key)
    # -

    # ## Question 3
    #
    # One of the strengths of Redis is that it provides functions that perform computations on the server, including a function that computes the intersection of two or more sets.
    #
    # Write Redis commands to compute:
    #
    # 1) A set of `caseid` values for respondents who are female bankers.
    #
    # 2) A set of `caseid` values for respondents who are liberal female bankers.
    #
    # Confirm that the second set is, in fact, smaller than the first.

    # ## Question 4
    #
    # Now suppose you want to look up a `caseid` and find all of the sets it belongs to.
    #
    # Write a function called `find_tags` that takes a `caseid` and returns a set of strings, where each string is the key of a set that contains the `caseid`.
    #
    # For example, if the `caseid` is 33, the result should be the set
    #
    # ```
    # {b'gss_set:bankers', b'gss_set:female'}
    # ```
    #
    # which indicates that this respondent is a female banker (but not liberal).

    # You can use the following examples to test your function. You should find that the respondent with `caseid` 33 is a female banker.

    find_tags(33)

    # And the respondent with `caseid` 451 is a liberal female banker.

    find_tags(451)

    # ## Just For Fun Extra Question
    #
    # Suppose there are a large number of sets and you often want to look up a `caseid` and find the sets it belongs to.
    #
    # Iterate through the sets we've defined so far and make a reverse index that maps from each `caseid` to a list of keys for the sets it belongs to.

    # *Data Structures and Information Retrieval in Python*
    #
    # Copyright 2021 Allen Downey
    #
    # License: [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-nc-sa/4.0/)
