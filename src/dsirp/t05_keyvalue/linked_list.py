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

# # Linked List

# [Click here to run this chapter on Colab](https://colab.research.google.com/github/AllenDowney/DSIRP/blob/main/notebooks/linked_list.ipynb)

# ## Linked Lists
#
# Implementing operations on linked lists is a staple of programming classes and technical interviews.
#
# I resist them because it is unlikely that you will ever have to implement a linked list in your professional work. And if you do, someone has made a bad decision.
#
# However, they can be good études, that is, pieces that you practice in order to learn, but never perform.

# For many of these problems, there are several possible solutions, depending on the requirements:
#
# * Are you allowed to modify an existing list, or do you have to create a new one?
#
# * If you modify an existing structure, are you also supposed to return a reference to it?
#
# * Are you allowed to allocate temporary structures, or do you have to perform all operations in place?
#
# And for all of these problems, you could write a solution iteratively or recursively. So there are many possible solutions for each.

# As we consider alternatives, some of the factors to keep in mind are:
#
# * Performance in terms of time and space.
#
# * Readability and demonstrably correctness.
#
# In general, performance should be asymptotically efficient; for example, if there is a constant time solution, a linear solution would not be acceptable.
# But we might be willing to pay some overhead to achieve bulletproof correctness.

# Here's the class we'll use to represent the nodes in a list.

class Node:
    def __init__(self, data, next=None):
        self.data = data
        self.next = next

    def __repr__(self):
        return f'Node({self.data}, {repr(self.next)})'


if __name__ == "__main__":
    # We can create nodes like this:

    # + tags=[]
    node1 = Node(1)
    node2 = Node(2)
    node3 = Node(3)

    node1
    # -

    # And then link them up, like this:

    # + tags=[]
    node1.next = node2
    node2.next = node3
    # -

    node1


    # There are two ways to think about what `node1` is:
    #
    # * It is "just" a node object, which happens to contain a link to another node.
    #
    # * It is the first node is a linked list of nodes.
    #
    # When we pass a node as a parameter, sometimes we think of it as a node and sometimes we think of it as the beginning of a list.

    # ## LinkedList objects
    #
    # For some operations, it will be convenient to have another object that represents the whole list (as opposed to one of its nodes).
    #
    # Here's the class definition.

    class LinkedList:
        def __init__(self, head=None):
            self.head = head

        def __repr__(self):
            return f'LinkedList({repr(self.head)})'


    # If we create a `LinkedList` with a reference to `node1`, we can think of the result as a list with three elements.

    # + tags=[]
    t = LinkedList(node1)
    t
    # -

    # ## Search
    #
    # **Exercise:** Write a function called `find` that takes a `LinkedList` and a target value; if the target value appears in the `LinkedList`, it should return the `Node` that contains it; otherwise it should return `None`.

    # You can use these examples to test your code.

    find(t, 1)

    find(t, 3)

    find(t, 5)


    # ## Push and Pop
    #
    # Adding and removing elements from the *left* side of a linked list is relatively easy:

    # + tags=[]
    def lpush(t, value):
        t.head = Node(value, t.head)


    # + tags=[]
    t = LinkedList()
    lpush(t, 3)
    lpush(t, 2)
    lpush(t, 1)
    t


    # + tags=[]
    def lpop(t):
        if t.head is None:
            raise ValueError('Tried to pop from empty LinkedList')
        node = t.head
        t.head = node.next
        return node.data


    # + tags=[]
    lpop(t), lpop(t), lpop(t)

    # + tags=[]
    t
    # -

    # Adding and removing from the end right side take longer because we have to traverse the list.
    #
    # **Exercise:** Write `rpush` and `rpop`.

    # You can use the following example to test your code.

    t = LinkedList()
    rpush(t, 1)
    t

    rpush(t, 2)
    t

    rpop(t)

    rpop(t)

    try:
        rpop(t)
    except ValueError as e:
        print(e)


    # ## Reverse
    #
    # Reversing a linked list is a classic interview question, although at this point it is so classic you will probably never encounter it.
    #
    # But it is still a good exercise, in part because there are so many ways to do it. My solutions here are based on [this tutorial](https://www.geeksforgeeks.org/reverse-a-linked-list/).

    # If you are allowed to make a new list, you can traverse the old list and `lpush` the elements onto the new list:

    def reverse(t):
        t2 = LinkedList()
        node = t.head
        while node:
            lpush(t2, node.data)
            node = node.next

        return t2


    t = LinkedList(Node(1, Node(2, Node(3, None))))
    reverse(t)


    # Here's a recursive version that doesn't allocate anything

    # +
    def reverse(t):
        t.head = reverse_rec(t.head)


    def reverse_rec(node):

        # if there are 0 or 1 nodes
        if node is None or node.next is None:
            return node

        # reverse the rest LinkedList
        rest = reverse_rec(node.next)

        # Put first element at the end
        node.next.next = node
        node.next = None

        return rest


    # -

    t = LinkedList(Node(1, Node(2, Node(3, None))))
    reverse(t)
    t


    # And finally an iterative version that doesn't allocate anything.

    def reverse(t):
        prev = None
        current = t.head
        while current:
            next = current.next
            current.next = prev
            prev = current
            current = next
        t.head = prev


    t = LinkedList(Node(1, Node(2, Node(3, None))))
    reverse(t)
    t


    # ## Remove
    #
    # One of the advantages of a linked list (compared to an array list) is that we can add and remove elements from the middle of the list in constant time.
    #
    # For example, the following function takes a node and removes the node that follows it.

    def remove_after(node):
        removed = node.next
        node.next = node.next.next
        return removed.data


    # Here's an example:

    t = LinkedList(Node(1, Node(2, Node(3, None))))
    remove_after(t.head)
    t

    # **Exercise:** Write a function called `remove` that takes a LinkedList and a target value. It should remove the first node that contains the value, or raise a `ValueError` if it is not found.
    #
    # Hint: This one is a little tricky.

    # You can use this example to test your code.

    t = LinkedList(Node(1, Node(2, Node(3, None))))
    remove(t, 2)
    t

    remove(t, 1)
    t

    try:
        remove(t, 4)
    except ValueError as e:
        print(e)

    remove(t, 3)
    t

    try:
        remove(t, 5)
    except ValueError as e:
        print(e)


    # Although `remove_after` is constant time, `remove` is not. Because we have to iterate through the nodes to find the target, `remove` takes linear time.

    # ## Insert Sorted
    #
    # Similarly, you can insert an element into the middle of a linked list in constant time.
    #
    # The following function inserts `data` after the given node in a list.

    def insert_after(node, data):
        node.next = Node(data, node.next)


    t = LinkedList(Node(1, Node(2, Node(3, None))))
    insert_after(t.head, 5)
    t


    # **Exercise:** Write a function called `insert_sorted` (also known as `insort`) that takes a linked list and a value and inserts the value in the list in the first place where it will be in increasing sorted order, that is, with the smallest element at the beginning.

    def insert_sorted(t, data):
        if t.head is None or t.head.data > data:
            lpush(t, data)
            return

        node = t.head
        while node.next:
            if node.next.data > data:
                insert_after(node, data)
                return
            node = node.next

        insert_after(node, data)


    # You can use the following example to test your code.

    t = LinkedList()
    insert_sorted(t, 1)
    t

    insert_sorted(t, 3)
    t

    insert_sorted(t, 0)
    t

    insert_sorted(t, 2)
    t

    # Although `insert_after` is constant time, `insert_sorted` is not. Because we have to iterate through the nodes to find the insertion point, `insert_sorted` takes linear time.

    # *Data Structures and Information Retrieval in Python*
    #
    # Copyright 2021 Allen Downey
    #
    # License: [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-nc-sa/4.0/)
