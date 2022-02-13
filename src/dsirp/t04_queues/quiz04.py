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

# # Quiz 4
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
# 5. Paste the link into [this Canvas assignment](https://canvas.olin.edu/courses/313/assignments/5032). 
#
# This quiz is open notes, open internet. The only thing you can't do is ask for help.
#
# Copyright 2021 Allen Downey, [MIT License](http://opensource.org/licenses/MIT)

# +
from os.path import basename, exists

from dsirp.helper_library.download import download

if __name__ == "__main__":
    download('https://github.com/AllenDowney/DSIRP/raw/main/american-english')


    # -

    # ## Question 1
    #
    # According to [Wikipedia](https://en.wikipedia.org/wiki/Gray_code), a Gray code is "an ordering of the binary numeral system such that two successive values differ in only one bit (binary digit)."
    #
    # A "Gray code list" is a table that lists the Gray code for each decimal number in order. For example, the following is the Gray code list for decimal numbers up to 3:
    #
    # ```
    # number    Gray code
    # ------    ---------
    # 0         00
    # 1         01
    # 2         11
    # 3         10
    # ```
    #
    # In this code, the representation of the number 3 is the bit sequence `10`.
    #
    # [This section of the Wikipedia page](https://en.wikipedia.org/wiki/Gray_code#Constructing_an_n-bit_Gray_code) presents an algorithm for constructing a Gray code list with a given number of binary digits.
    #
    # Write a function called `gray_code` that takes the number of binary digits, `n`, as a parameter and returns a list of strings that represents a Gray code list.
    #
    # For example, `gray_code(3)` should return
    #
    # ```
    # ['000', '001', '011', '010', '110', '111', '101', '100']
    # ```
    #
    # Your function can be iterative or recursive.

    # +
    # Buggy solution

    def gray_code(n, codes=['0', '1']):
        if n <= 1:
            return codes

        r = codes[::-1]

        for i, code in enumerate(codes):
            codes[i] = '0' + code

        for i, code in enumerate(r):
            r[i] = '1' + code

        codes.extend(r)

        return gray_code(n - 1, codes)


    # -

    # You can use the following cells to test your solution.

    gray_code(1)  # should be ['0', '1']

    gray_code(2)  # should be ['00', '01', '11', '10']

    gray_code(3)  # see above

    gray_code(4)  # see above

    # ## Question 2
    #
    # Suppose you are given a very large sequence of numbers and you are asked to find the `k` largest elements.
    # One option would be to sort the sequence, but that would take time proportional to `n log n`, where `n` is the length of the sequence.
    # And you would have to store the entire sequence.
    #
    # An alternative is to use a "bounded heap", that is, a heap that never contains more than `k` elements.
    #
    # Write a function called `k_largest` that takes as parameters an iterable and an integer `k` and returns a list that contains the `k` largest elements in the iterable. Don't worry about ties.
    #
    # Your implementation should not store more than `k` elements and it should take time proportional to `n log k`.

    # You can use the following cells to test your function.

    # +
    from random import shuffle

    sequence = list(range(10))
    shuffle(sequence)
    sequence
    # -

    k_largest(sequence, 3)  # should return [7, 8, 9]

    # ## Question 3
    #
    # An expression tree is a tree that represents a mathematical expression.
    # For example, the expression `(1+2) * 3` is represented by a tree with the multiplication operator at the root and two children:
    #
    # * The left child is a node that contains the addition operator and two children, the number 1 and the number 2.
    #
    # * The right child is a node that contains the number 3.
    #
    # To represent an expression tree, we can use a `namedtuple` called `Node` that contains three attributes, `data`, `left`, and `right`.

    # +
    from collections import namedtuple

    Node = namedtuple('Node', ['data', 'left', 'right'])
    # -

    # In a leaf node, `data` contains a number. For example, here are two nodes representing the numbers `1` and `2`.

    operand1 = Node(1, None, None)
    operand1

    operand2 = Node(2, None, None)
    operand2

    # For internal nodes (that is, not leaf nodes) `data` contains a function. To represent addition, subtraction, and multiplication, I'll import functions from the `operator` module.

    from operator import add, sub, mul

    # Now we can make an expression tree with the `add` function at the root and two operands as children.

    etree = Node(add, operand1, operand2)
    etree

    # To evaluate this tree, we can extract the function and the two operands, then call the function and pass the operands as arguments.

    func = etree.data
    left = operand1.data
    right = operand2.data
    func(left, right)

    # Write a function called `evaluate` that takes an arbitrary expression tree, evaluates it, and returns an integer.
    #
    # You will probably want to write this one recursively.

    # You can test your function with the following examples:

    etree

    evaluate(etree)  # result should be 3

    operand3 = Node(3, None, None)
    etree2 = Node(mul, etree, operand3)

    evaluate(etree2)  # result should be 9

    operand4 = Node(4, None, None)
    etree3 = Node(sub, etree2, operand4)

    evaluate(etree3)  # result should be 5
