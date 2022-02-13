def test_main():
    # # Level Order Traversal

    # [Click here to run this chapter on Colab](https://colab.research.google.com/github/AllenDowney/DSIRP/blob/main/notebooks/level_order.ipynb)

    # ## More tree traversal
    #
    # In a previous notebook we wrote two versions of a depth-first search in a tree.
    # Now we are working toward depth-first search, but we're going to make a stop along the way: level-order traversal.
    #
    # One application of level-order traversal is searching through directories (aka folders) in a file system.
    # Since directories can contain other directories, which can contains other directories, and so on, we can think of a file system as a tree.
    #
    # In this notebook, we'll start by making a tree of directories and fake data files.
    # Then we'll traverse it several ways.
    #
    # And while we're at it, we'll learn about the `os` module, which provides functions for interacting with the operating system, especially the file system.
    #
    #

    # The `os` module provides `mkdir`, which creates a directory. It raises an exception if the directory exists, so I'm going to wrap it in a `try` statement.

    # +
    import os

    def mkdir(dirname):
        try:
            os.mkdir(dirname)
            print('made', dirname)
        except FileExistsError:
            print(dirname, 'exists')

    # -

    # Now I'll create the directory where we'll put the fake data.

    # + tags=[]
    mkdir('level_data')
    # -

    # Inside `level_data`, I want to make a subdirectory named `2021`.
    # It is tempting to write something like:
    #
    # ```
    # year_dir = `level_data/2021`
    # ```
    #
    # This path would work on Unix operating systems (including MacOS), but not Windows, which uses `\` rather than `/` between names in a path.
    #
    # We can avoid this problem by using `os.path.join`, which joins names in a path with whatever character the operating system wants.

    # + tags=[]
    year_dir = os.path.join('level_data', '2021')
    mkdir(year_dir)

    # -

    # To make the fake data files, I'll use the following function, which opens a file for writing and puts the word `data` into it.

    def make_datafile(dirname, filename):
        filename = os.path.join(dirname, filename)
        open(filename, 'w').write('data\n')
        print('made', filename)

    # So let's start by putting a data file in `year_dir`, imagining that this file contains summary data for the whole year.

    # + tags=[]
    make_datafile(year_dir, 'year.csv')

    # -

    # The following function
    #
    # 1. Makes a subdirectory that represents one month of the year,
    #
    # 2. Makes a data file we imagine contains summary data for the month, and
    #
    # 3. Calls `make_day` (below) to make subdirectories each day of the month (in a world where all months have 30 days).

    def make_month(i, year_dir):
        month = '%.2d' % i
        month_dir = os.path.join(year_dir, month)
        mkdir(month_dir)
        make_datafile(month_dir, 'month.csv')

        for j in range(1, 31):
            make_day(j, month_dir)

    # `make_day` makes a sub-subdirectory for a given day of the month, and puts a data file in it.

    def make_day(j, month_dir):
        day = '%.2d' % j
        day_dir = os.path.join(month_dir, day)
        mkdir(day_dir)
        make_datafile(day_dir, 'day.csv')

    # The following loop makes a directory for each month.

    # + tags=[]
    for i in range(1, 13):
        make_month(i, year_dir)
    # -

    # ## Walking a Directory
    #
    # The `os` module provides `walk`, which is a generator function that traverses a directory and all its subdirectories, and all their subdirectories, and so on.
    #
    #
    # For each directory, it yields:
    #
    # * dirpath, which is the name of the directory.
    #
    # * dirnames, which is a list of subdirectories it contains, and
    #
    # * filenames, which is a list of files it contains.
    #
    # Here's how we can use it to print the paths of all files in the directory we created.

    # + tags=[]
    for dirpath, dirnames, filenames in os.walk('level_data'):
        for filename in filenames:
            path = os.path.join(dirpath, filename)
            print(path)

    # -

    # One quirk of `os.walk` is that the directories and files don't appear in any particular order.
    # Of course, we can store the results and sort them in whatever order we want.
    #
    # But as an exercise, we can write our own version of `walk`.
    # We'll need two functions:
    #
    # * `os.listdir`, which takes a directory and list the directories and files it contains, and
    #
    # * `os.path.isfile`, which takes a path and returns `True` if it is a file, and `False` if it is a directory or something else.
    #
    # You might notice that some file-related functions are in the submodule `os.path`.
    # There is some logic to this organization, but it is not always obvious why a particular function is in this submodule or not.
    #
    # Anyway, here is a recursive version of `walk`:

    def walk(dirname):
        for name in sorted(os.listdir(dirname)):
            path = os.path.join(dirname, name)
            if os.path.isfile(path):
                print(path)
            else:
                walk(path)

    walk(year_dir)

    # **Exercise:** Write a version of `walk` called `walk_gen` that is a generator function; that is, it should yield the paths it finds rather than printing them.

    # You can use the following loop to test your code.

    for path in walk_gen(year_dir):
        print(path)

    # **Exercise:** Write a version of `walk_gen` called `walk_dfs` that traverses the given directory and yields the file it contains, but it should use a stack and run iteratively, rather than recursively.

    # You can use the following loop to test your code.

    for path in walk_dfs(year_dir):
        print(path)

    # Notice that the order the files are discovered is "depth-first". For example, it yields all files from the first month before any of the files for the second month.
    #
    # An alternative is a level-order traversal, which yields all files at the first level (the annual summary), then all the files at the second level (the monthly summaries), then the files at the third level.
    #
    # To implement a level-order traversal, we can make a minimal change to `walk_dfs`: replace the stack with a FIFO queue.
    # To implement the queue efficiently, we can use `collections.deque`.
    #
    # **Exercise:** Write a generator function called `walk_level` that takes a directory and yields its files in level order.

    # Use the following loop to test your code.

    for path in walk_level(year_dir):
        print(path)

    # If you are looking for a file in a large file system, a level-order search might be useful if you think the file is more likely to be near the root, rather than deep in a nested subdirectory.

    # *Data Structures and Information Retrieval in Python*
    #
    # Copyright 2021 Allen Downey
    #
    # License: [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-nc-sa/4.0/)
