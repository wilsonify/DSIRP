from dsirp.t03_search import quiz03


def test_smoke():
    print("fire?")
    print(dir(quiz03))


def test_main():
    # # Quiz 3
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
    # 5. Paste the link into [this Canvas assignment](https://canvas.olin.edu/courses/313/assignments/4985).
    #
    # This quiz is open notes, open internet. The only thing you can't do is ask for help.
    #
    # Copyright 2021 Allen Downey, [MIT License](http://opensource.org/licenses/MIT)

    # +
    from os.path import basename, exists


    # download('https://github.com/AllenDowney/DSIRP/raw/main/american-english')

    # -

    # ## Question 1
    #
    # The following is the implementation of a binary search tree (BST) from `search.ipynb`.

    class Node:
        def __init__(self, data, left=None, right=None):
            self.data = data
            self.left = left
            self.right = right

        def __repr__(self):
            return f'Node({self.data}, {repr(self.left)}, {repr(self.right)})'

    class BSTree:
        def __init__(self, root=None):
            self.root = root

        def __repr__(self):
            return f'BSTree({repr(self.root)})'

    # +
    def insert(tree, data):
        tree.root = insert_rec(tree.root, data)

    def insert_rec(node, data):
        if node is None:
            return Node(data)

        if data < node.data:
            node.left = insert_rec(node.left, data)
        else:
            node.right = insert_rec(node.right, data)

        return node

    # -

    # The following cell reads words from a file and adds them to a BST.
    # But if you run it, you'll get a `RecursionError`.

    filename = 'american-english'
    tree = BSTree()
    for line in open(filename):
        for word in line.split():
            insert(tree, word.strip())

    # However, if we put the words into a list, shuffle the list, and then put the shuffled words into the BST, it works.

    word_list = []
    for line in open(filename):
        for word in line.split():
            word_list.append(word.strip())

    # +
    from random import shuffle

    shuffle(word_list)
    # -

    tree = BSTree()
    for word in word_list:
        insert(tree, word.strip())

    # Write a few clear, complete sentences to answer the following two questions:
    #
    # 1) Why did we get a `RecursionError`, and why does shuffling the words fix the problem?

    #

    # 2) What is the order of growth for the whole process; that is, reading the words into a list, shuffling the list, and then putting the shuffled words into a binary search tree. You can assume that `shuffle` is linear.

    #

    # ## Question 2
    #
    # As we discussed in class, there are three versions of the search problem:
    #
    # 1) Checking whether an element is in a collection; for example, this is what the `in` operator does.
    #
    # 2) Finding the index of an element in an ordered collection; for example, this is what the string method `find` does.
    #
    # 3) In a collection of key-value pairs, finding the value that corresponds to a given key; this is what the dictionary method `get` does.
    #
    # In `search.ipynb`, we used a BST to solve the first problem. In this exercise, you will modify it to solve the third problem.
    #
    # Here's the code again (although notice that the names of the objects are `MapNode` and `BSTMap`).

    class MapNode:
        def __init__(self, data, left=None, right=None):
            self.data = data
            self.left = left
            self.right = right

        def __repr__(self):
            return f'Node({self.data}, {repr(self.left)}, {repr(self.right)})'

    class BSTMap:
        def __init__(self, root=None):
            self.root = root

        def __repr__(self):
            return f'BSTMap({repr(self.root)})'

    # +
    def insert_map(tree, data):
        tree.root = insert_map_rec(tree.root, data)

    def insert_map_rec(node, data):
        if node is None:
            return MapNode(data)

        if data < node.data:
            node.left = insert_map_rec(node.left, data)
        else:
            node.right = insert_map_rec(node.right, data)

        return node

    # -

    # Modify this code so that it stores keys and values, rather than just elements of a collection.
    # Then write a function called `get` that takes a `BSTMap` and a key:
    #
    # * If the key is in the map, it should return the corresponding value;
    #
    # * Otherwise it should raise a `KeyError` with an appropriate message.
    #
    # You can use the following code to test your implementation.

    # +
    tree_map = BSTMap()

    keys = 'uniqueltrs'
    values = range(len(keys))
    for key, value in zip(keys, values):
        print(key, value)
        insert_map(tree_map, key, value)

    tree_map
    # -

    for key in keys:
        print(key, get(tree_map, key))

    # The following should raise a `KeyError`.

    get(tree_map, 'b')

    # ## Alternative solution

    # Modify this code so that it stores keys and values, rather than just elements of a collection.
    # Then write a function called `get` that takes a `BSTMap` and a key:
    #
    # * If the key is in the map, it should return the corresponding value;
    #
    # * Otherwise it should raise a `KeyError` with an appropriate message.
    #
    # You can use the following code to test your implementation.

    # +
    tree_map = BSTMap()

    keys = 'uniqueltrs'
    values = range(len(keys))
    for key, value in zip(keys, values):
        print(key, value)
        insert_map(tree_map, key, value)

    tree_map
    # -

    for key in keys:
        print(key, get(tree_map, key))
