def test_smoke():
    print("fire?")


def test_main():
    # # Redis

    # [Click here to run this chapter on Colab](https://colab.research.google.com/github/AllenDowney/DSIRP/blob/main/notebooks/redis.ipynb)

    # + tags=[]

    def download(url):
        filename = basename(url)
        if not exists(filename):
            from urllib.request import urlretrieve
            local, _ = urlretrieve(url, filename)
            print('Downloaded ' + local)

    # download('https://github.com/AllenDowney/DSIRP/raw/main/utils.py')

    # -

    # [Click here to run this chapter on Colab](https://colab.research.google.com/github/AllenDowney/DSIRP/blob/main/notebooks/chap01.ipynb)

    # ## Persistence
    #
    # Data stored only in the memory of a running program is called "volatile", because it disappears when the program ends.
    #
    # Data that still exists after the program that created it ends is called
    # "persistent". In general, files stored in a file system are persistent,
    # as well as data stored in databases.
    #
    # A simple way to make data persistent is to store it in a file. For example, before the program ends, it could translate its data structures into a format like [JSON](https://en.wikipedia.org/wiki/JSON) and then write them into a file.
    # When it starts again, it could read the file and rebuild the data
    # structures.

    # But there are several problems with this solution:
    #
    # 1.  Reading and writing large data structures (like a Web index) would
    #     be slow.
    #
    # 2.  The entire data structure might not fit into the memory of a single
    #     running program.
    #
    # 3.  If a program ends unexpectedly (for example, due to a power outage),
    #     any changes made since the program last started would be lost.
    #
    # A better alternative is a database that provides persistent storage and
    # the ability to read and write parts of the database without reading and
    # writing the whole thing.

    # There are many kinds of [database management systems](https://en.wikipedia.org/wiki/Database) (DBMS) that provide
    # these capabilities.
    #
    # The database we'll use is Redis, which organizes data in structures that are similar to Python data structures.
    # Among others, it provides lists, hashes (similar to Python dictionaries), and sets.
    #
    # Redis is a "key-value database", which means that it represents a mapping from keys to values.
    # In Redis, the keys are strings and the values can be one of several types.

    # ## Redis clients and servers
    #
    # Redis is usually run as a remote service; in fact, the name stands for
    # "REmote DIctionary Server". To use Redis, you have to run the Redis
    # server somewhere and then connect to it using a Redis client.
    #
    # To get started, we'll run the Redis server on the same machine where we run the Jupyter server.
    # This will let us get started quickly, but if we are running Jupyter on Colab, the database lives in a Colab runtime environment, which disappears when we shut down the notebook.
    # So it's not really persistent.
    #
    # Later we will use [RedisToGo](http://thinkdast.com/redistogo), which runs Redis in the cloud.
    # Databases on RedisToGo are persistent.
    #
    # The following cell installs the Redis server and starts it with the `daemonize` options, which runs it in the background so the Jupyter server can resume.

    # +
    import sys

    IN_COLAB = 'google.colab' in sys.modules

    if IN_COLAB:
    # !pip install redis-server
    # !/usr/local/lib/python*/dist-packages/redis_server/bin/redis-server --daemonize yes
    else:
    # !redis-server --daemonize yes
    # -

    # ## redis-py
    #
    # To talk to the Redis server, we'll use [redis-py](https://redis-py.readthedocs.io/en/stable/index.html).
    # Here's how we use it to connect to the Redis server.

    try:
        import redis
    except ImportError:
    # !pip install redis

    # + tags=[]
    import redis

    r = redis.Redis()
    # -

    # The `set` method adds a key-value pair to the database.
    # In the following example, the key and value are both strings.

    # + tags=[]
    r.set('key', 'value')
    # -

    # The `get` method looks up a key and returns the corresponding value.

    # + tags=[]
    r.get('key')
    # -

    # The result is not actually a string; it is a [bytearray](https://stackoverflow.com/questions/6224052/what-is-the-difference-between-a-string-and-a-byte-string).
    #
    # For many purposes, a bytearray behaves like a string so for now we will treat it like a string and deal with differences as they arise.

    # The values can be integers or floating-point numbers.

    # + tags=[]
    r.set('x', 5)
    # -

    # And Redis provides some functions that understand numbers, like `incr`.

    # + tags=[]
    r.incr('x')
    # -

    # But if you `get` a numeric value, the result is a bytearray.

    # + tags=[]
    value = r.get('x')
    value
    # -

    # If you want to do math with it, you have to convert it back to a number.

    # + tags=[]
    int(value)
    # -

    # If you want to set more than one value at a time, you can pass a dictionary to `mset`.

    # + tags=[]
    d = dict(x=5, y='string', z=1.23)
    r.mset(d)

    # + tags=[]
    r.get('y')

    # + tags=[]
    r.get('z')
    # -

    # If you try to store any other type in a Redis database, you get an error.

    # + tags=[]
    from redis import DataError

    t = [1, 2, 3]

    try:
        r.set('t', t)
    except DataError as e:
        print(e)
    # -

    # We could use the `repr` function to create a string representation of a list, but that representation is Python-specific.
    # It would be better to make a database that can work with any language.
    # To do that, we can use JSON to create a string representation.
    #
    # The `json` module provides a function `dumps`, that creates a language-independent representation of most Python objects.

    # + jupyter={"source_hidden": true} tags=[]
    import json

    t = [1, 2, 3]
    s = json.dumps(t)
    s
    # -

    # When we read one of these strings back, we can use `loads` to convert it back to a Python object.

    # + tags=[]
    t = json.loads(s)
    t
    # -

    # **Exercise:** Create a dictionary with a few items, including keys and values with different types. Use `json` to make a string representation of the dictionary, then store it as a value in the Redis database. Retrieve it and convert it back to a dictionary.

    # ## Redis Data Types
    #
    # JSON can represent most Python objects, so we could use it to store arbitrary data structures in Redis. But in that case Redis only knows that they are strings; it can't work with them as data structures. For example, if we store a data structure in JSON, the only way to modify it would be to:
    #
    # 1. Get the entire structure, which might be large,
    #
    # 2. Load it back into a Python structure,
    #
    # 3. Modify the Python structure,
    #
    # 4. Dump it back into a JSON string, and
    #
    # 5. Replace the old value in the database with the new value.
    #
    # That's not very efficient. A better alternative is to use the data types Redis provides, which you can read about in the
    # [Redis Data Types Intro](https://redis.io/topics/data-types-intro).

    # # Lists
    #
    # The `rpush` method adds new elements to the end of a list (the `r` indicates the right-hand side of the list).

    # + tags=[]
    r.rpush('t', 1, 2, 3)
    # -

    # You don't have to do anything special to create a list; if it doesn't exist, Redis creates it.
    #
    # `llen` returns the length of the list.

    # + tags=[]
    r.llen('t')
    # -

    # `lrange` gets elements from a list. With the indices `0` and `-1`, it gets all of the elements.

    # + tags=[]
    r.lrange('t', 0, -1)
    # -

    # The result is a Python list, but the elements are bytestrings.
    #
    # `rpop` removes elements from the end of the list.

    # + tags=[]
    r.rpop('t')
    # -

    # You can read more about the other list methods in the [Redis documentation](https://redis.io/commands#list).
    #
    # And you can read about the [redis-py API here](https://redis-py.readthedocs.io/en/stable/index.html#redis.Redis.rpush).
    #
    # In general, the documentation of Redis is very good; the documentation of `redis-py` is a little rough around the edges.

    # **Exercise:** Use `lpush` to add elements to the beginning of the list and `lpop` to remove them.
    #
    # Note: Redis lists behave like linked lists, so you can add and remove elements from either end in constant time.

    # + tags=[]
    r.lpush('t', -3, -2, -1)

    # + tags=[]
    r.lpop('t')
    # -

    # ## Hash
    #
    # A [Redis hash](https://redis.io/commands#hash) is similar to a Python dictionary, but just to make things confusing the nomenclature is a little different.
    #
    # What we would call a "key" in a Python dictionary is called a "field" in a Redis hash.
    #
    # The `hset` method sets a field-value pair in a hash:

    # + tags=[]
    r.hset('h', 'field', 'value')
    # -

    # The `hget` method looks up a field and returns the corresponding value.

    # + tags=[]
    r.hget('h', 'field')
    # -

    # `hset` can also take a Python dictionary as a parameter:

    # + tags=[]
    d = dict(a=1, b=2, c=3)
    r.hset('h', mapping=d)
    # -

    # To iterate the elements of a hash, we can use `hscan_iter`:

    # + tags=[]
    for field, value in r.hscan_iter('h'):
        print(field, value)
    # -

    # The results are bytestrings for both the fields and values.

    # **Exercise:** To add multiple items to a hash, you can use `hset` with the keyword `mapping` and a dictionary (or other mapping type).
    #
    # Use the `Counter` object from the `collections` module to count the letters in a string, then use `hset` to store the results in a Redis hash.
    #
    # Then use `hscan_iter` to display the results.

    # ## Deleting
    #
    # Before we go on, let's clean up the database by deleting all of the key-value pairs.

    # + tags=[]
    for key in r.keys():
        r.delete(key)
    # -

    # ## Anagrams (again!)
    #
    # In a previous notebook, we made sets of words that are anagrams of each other by building a dictionary where they keys are sorted strings of letters and the values are lists of words.
    #
    # We'll start by solving this problem again using Python data structures; then we'll translate it into Redis.
    #
    # The following cell downloads a file that contains the list of words.

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

    # And here's a generator function that reads the words in the file and yields them one at a time.

    def iterate_words(filename):
        """Read lines from a file and split them into words."""
        for line in open(filename):
            for word in line.split():
                yield word.strip()

    # The "signature" of a word is a string that contains the letter of the word in sorted order.
    # So if two words are anagrams, they have the same signature.

    def signature(word):
        return ''.join(sorted(word))

    # The following loop makes a dictionary of anagram lists.

    anagram_dict = {}
    for word in iterate_words('american-english'):
        key = signature(word)
        anagram_dict.setdefault(key, []).append(word)

    # The following loop prints all anagram lists with 6 or more words

    for v in anagram_dict.values():
        if len(v) >= 6:
            print(len(v), v)

    # Now, to do the same thing in Redis, we have two options:
    #
    # * We can store the anagram lists using Redis lists, using the signatures as keys.
    #
    # * We can store the whole data structure in a Redis hash.
    #
    # A problem with the first option is that the keys in a Redis database are like global variables. If we create a large number of keys, we are likely to run into name conflicts.
    # We can mitigate this problem by giving each key a prefix that identifies its purpose.
    #
    # The following loop implements the first option, using "Anagram" as a prefix for the keys.

    # + tags=[]
    for word in iterate_words('american-english'):
        key = f'Anagram:{signature(word)}'
        r.rpush(key, word)
    # -

    # An advantage of this option is that it makes good use of Redis lists. A drawback is that makes many small database transactions, so it is relatively slow.
    #
    # We can use `keys` to get a list of all keys with a given prefix.

    # + tags=[]
    keys = r.keys('Anagram*')
    len(keys)
    # -

    # **Exercise:** Write a loop that iterates through `keys`, uses `llen` to get the length of each list, and prints the elements of all lists with 6 or more elements.

    # Before we go on, we can delete the keys from the database like this.

    # + tags=[]
    r.delete(*keys)
    # -

    # The second option is to compute the dictionary of anagram lists locally and then store it as a Redis hash.
    #
    # The following function uses `dumps` to convert lists to strings that can be stored as values in a Redis hash.

    # + jupyter={"source_hidden": true} tags=[]
    hash_key = 'AnagramHash'
    for field, t in anagram_dict.items():
        value = json.dumps(t)
        r.hset(hash_key, field, value)
    # -

    # We can do the same thing faster if we convert all of the lists to JSON locally and store all of the field-value pairs with one `hset` command.
    #
    # First, I'll delete the hash we just created.

    # + tags=[]
    r.delete(hash_key)
    # -

    # **Exercise:** Make a Python dictionary that contains the items from `anagram_dict` but with the values converted to JSON. Use `hset` with the `mapping` keyword to store it as a Redis hash.

    # **Exercise:** Write a loop that iterates through the field-value pairs, converts each value back to a Python list, and prints the lists with 6 or more elements.

    # ## Shut down
    #
    # If you are running this notebook on your own computer, you can use the following command to shut down the Redis server.
    #
    # If you are running on Colab, it's not really necessary: the Redis server will get shut down when the Colab runtime shuts down (and everything stored in it will disappear).

    # !killall redis-server

    # *Data Structures and Information Retrieval in Python*
    #
    # Copyright 2021 Allen Downey
    #
    # License: [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-nc-sa/4.0/)
