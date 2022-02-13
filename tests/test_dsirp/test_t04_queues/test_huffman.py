def test_smoke():
    print("fire?")


def test_main():
    # # Huffman Code

    # [Click here to run this chapter on Colab](https://colab.research.google.com/github/AllenDowney/DSIRP/blob/main/notebooks/huffman.ipynb)

    # A [Huffman code](https://en.wikipedia.org/wiki/Huffman_coding) is a "type of optimal prefix code that is commonly used for lossless data compression".
    # There are three parts of that definition we have to unpack: "code", "prefix", and "optimal".
    #
    # In this context, a "code" is a mapping from symbols to bit strings.
    # For example, [ASCII](https://en.wikipedia.org/wiki/ASCII) is a character encoding that maps from characters (like letters, numbers, and punctuation) to seven-bit integers.
    # Since all ASCII bit strings are the same length, it is a "fixed-length code", as contrasted with Huffman codes, which are "variable-length codes".
    #
    # In order to decode something encoded in a variable-length code, there has to be some way to figure out where one bit string ends and the next begins.
    # In general, there are three ways to solve this problem:
    #
    # * One option is to begin each bit string with a special sequence that indicates its length. This is [how Unicode works](https://stackoverflow.com/questions/1543613/how-does-utf-8-variable-width-encoding-work).
    #
    # * Another option is to end each bit string with a special sequence that marks the end.
    #
    # * The third option is to use a "prefix code", which is how Huffman codes work.
    #
    # A prefix code is a code where no whole bit string in the code is a prefix of any bit string in the code.
    # If a code has this property, we can decode it by reading bits one at a time and checking to see whether we have completed a valid bit string.
    # If so, we know we are at the end of the bit string, because it cannot be the prefix of another bit string.
    #
    # For example, the following is a prefix code with only three symbols:
    #
    # ```
    # symbol        bit string
    # x             1
    # y             01
    # z             001
    # ```
    #
    # In this code, we can encode the string `xyz` with the bit string `101001`, and we can decode the result without ambiguity.
    #
    # So that's what it means to say that a Huffman code is a prefix code; finally, Huffman codes are "optimal" in the sense that they give short codes to the most common symbols and longer codes to the least common symbols.
    # The result is that they minimize the average number of bits needed to encode a sequence of symbols.
    #
    # However, in order to achieve this feat, we have to know the relative frequencies of the symbols.
    # One way to do that is to start with a "corpus", which is a text that contains the symbols in the proportions we expect for the text we will encode.
    #
    # As an example, I'll use the text from the [Huffman code Wikipedia page](https://en.wikipedia.org/wiki/Huffman_coding).

    text = 'this is an example of a huffman tree'

    # We can use a `Counter` to count the number of times each symbol appears in this text.

    # +
    from collections import Counter

    c = Counter(text)
    c
    # -

    # Now let's see how we can use these counts to build a Huffman code.
    # The first step is to build a Huffman tree, which is a binary tree where every node contains a count and some nodes contain symbols.
    #
    # To make a Huffman tree, we start with a sequence of nodes, one for each symbol.
    # To represent nodes, I'll use a `namedtuple`.

    # + tags=[]
    from collections import namedtuple

    Node = namedtuple('Node', ['count', 'letter', 'left', 'right'])
    # -

    # For example, here's a node that represents the symbol `a` with count `4`.
    # Since this node has no children, it is a leaf node.

    # + tags=[]
    left = Node(4, 'a', None, None)
    left
    # -

    # And here's another leaf node that represents the symbol `n` and its count.

    # + tags=[]
    right = Node(2, 'n', None, None)
    right
    # -

    # One reason we're using a namedtuple is that it behaves like a tuple, so if we compare two `Node` objects, we get a tuple-like sorting order.

    # + tags=[]
    left > right
    # -

    # If two nodes have the same `count`, they get sorted in alphabetical order by `letter`.

    # ## Making trees
    #
    # Given these two leaf nodes, we can make a tree like this:

    # + tags=[]
    count = left.count + right.count
    root = Node(count, '\0', left, right)
    root
    # -

    # Because `root` has children, it is not a leaf node; it is an interior node.
    # In a Huffman tree, the interior nodes do not represent symbols, so I have set `letter` to the null character `\0`.
    # The count of an interior node is the sum of the count of its children.

    # Now, to build a Huffman tree, we'll start with a collection of nodes, one for each symbol, and build the tree "bottom up" by following these steps:
    #
    # 1) Remove the node with the lowest count.
    #
    # 2) Remove the node with the next lowest count.
    #
    # 3) Make a new node with the nodes we just removed as children.
    #
    # 4) Put the new node back into the collection.
    #
    # 5) If there's only one node in the collection, it's the Huffman tree, and we're done.
    #
    # In general, we could use any kind of collection, but if we look at the operations required by this algorithm, the most efficient option is a heap.

    # But we'll start by iterating through the `Counter` and making a list of `Node` objects,

    # + tags=[]
    nodes = [Node(count, letter, None, None)
             for (letter, count) in c.items()]
    nodes
    # -

    # Next we'll use the heap module to convert the list to a heap.

    # + tags=[]
    from heapq import heapify

    heap = nodes.copy()
    heapify(heap)
    heap
    # -

    # Now we can use the heap to make a tree.
    #
    # **Exercise:** Write a function called `make_tree` that takes a heap of `Node` objects and uses the algorithm I described to make and return a Huffman tree. In other words, it should join up the nodes into a tree and return the root node.

    # Use this code to test it.

    # + tags=[]
    tree = make_tree(heap)
    # -

    # ## Drawing the Tree
    #
    # To see what it looks like, we'll use NetworkX and a library called EoN.

    try:
        import EoN
    except ImportError:
    # !pip install EoN

    # The following function traverses the Huffman tree and makes a NetworkX `DiGraph`.

    # +
    import networkx as nx

    def add_edges(parent, G):
        """Make a NetworkX graph that represents the tree."""
        if parent is None:
            return

        for child in (parent.left, parent.right):
            if child:
                G.add_edge(parent, child)
                add_edges(child, G)

    # -

    G = nx.DiGraph()
    add_edges(tree, G)

    # The following function traverses the tree again and collects the node labels in a dictionary.

    def get_labels(parent, labels):
        if parent is None:
            return

        if parent.letter == '\0':
            labels[parent] = parent.count
        else:
            labels[parent] = parent.letter

        get_labels(parent.left, labels)
        get_labels(parent.right, labels)

    labels = {}
    get_labels(tree, labels)

    def get_edge_labels(parent, edge_labels):
        if parent is None:
            return

        if parent.left:
            edge_labels[parent, parent.left] = '0'
            get_edge_labels(parent.left, edge_labels)

        if parent.right:
            edge_labels[parent, parent.right] = '1'
            get_edge_labels(parent.right, edge_labels)

    edge_labels = {}
    get_edge_labels(tree, edge_labels)
    len(edge_labels)

    # Now we're ready to draw.

    # +
    from EoN import hierarchy_pos

    def draw_tree(tree):
        G = nx.DiGraph()
        add_edges(tree, G)
        pos = hierarchy_pos(G)
        labels = {}
        get_labels(tree, labels)
        edge_labels = {}
        get_edge_labels(tree, edge_labels)
        nx.draw(G, pos, labels=labels, alpha=0.4)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='C1')

    # -

    draw_tree(tree)

    # The result might not be identical to the tree on [the Wikipedia page](https://en.wikipedia.org/wiki/Huffman_coding), but a letter in our tree should be on the same level as the same letter in their tree.

    # ## Making the Table
    #
    # The following function traverses the tree, keeping track of the path as it goes. When it finds a leaf node, it makes an entry in the table.

    # + tags=[]
    def is_leaf(node):
        return node.left is None and node.right is None

    # + tags=[]
    def make_table(node, path, table):
        if node is None:
            return

        if is_leaf(node):
            table[node.letter] = path
            return

        make_table(node.left, path + '0', table)
        make_table(node.right, path + '1', table)

    # + tags=[]
    table = {}
    make_table(tree, '', table)

    table

    # -

    # ## Encoding
    #
    # We can use the table to encode a string by looking up each symbol in the string and joining the results into a bit string.

    # + tags=[]
    def encode(s, table):
        t = [table[letter] for letter in s]
        return ''.join(t)

    # -

    # Here's an example, noting that we can encode strings other than the corpus we started with, provided that it contains no symbols that were not in the corpus.

    # + tags=[]
    code = encode('this is spinal tap', table)
    code
    # -

    # ## Decoding
    #
    # To decode the bit string, we start at the top of the tree and follow the path, turning left when we see a `0` and right when we see a `1`.
    # If we get to a root node, we have decoded a symbol, so we should record it and then jump back to the top of the tree to start decoding the next symbol.
    #
    # **Exercise:** Write a function called `decode` that takes as parameters a string on 0s and 1s and a Huffman tree. It should decode the message and return it as a string.

    decode(code, tree)

    # *Data Structures and Information Retrieval in Python*
    #
    # Copyright 2021 Allen Downey
    #
    # License: [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-nc-sa/4.0/)
