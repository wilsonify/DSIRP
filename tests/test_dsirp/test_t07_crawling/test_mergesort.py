from dsirp.t07_crawling import mergesort


def test_smoke():
    print("fire?")
    print(dir(mergesort))


def test_main():
    # # Merge Sort

    # [Click here to run this chapter on Colab](https://colab.research.google.com/github/AllenDowney/DSIRP/blob/main/notebooks/mergesort.ipynb)

    # ## Implementing Merge Sort
    #
    # [Merge sort](https://en.wikipedia.org/wiki/Merge_sort) is a divide and conquer strategy:
    #
    # 1. Divide the sequence into two halves,
    #
    # 2. Sort the halves, and
    #
    # 3. Merge the sorted sub-sequences into a single sequence.

    # Since step 2 involves sorting, this algorithm is recursive, so we need a base case.
    # There are two options:
    #
    # 1. If the size falls below some threshold, we can use another sort algorithm.
    #
    # 2. If the size of a sub-sequence is 1, it is already sorted.
    #
    # [Comparison with other sort algorithms](https://en.wikipedia.org/wiki/Merge_sort#Comparison_with_other_sort_algorithms)

    # To implement merge sort, I think it's helpful to start with a non-recursive version that uses the Python `sort` function to sort the sub-sequences.

    # + tags=[]
    def merge_sort_norec(xs):
        n = len(xs)
        mid = n // 2
        left = xs[:mid]
        right = xs[mid:]

        left.sort()
        right.sort()

        return merge(left, right)

    # -

    # **Exercise:** Write a function called `merge` that takes two sorted sequences, `left` and `right`, and returns a sequence that contains all elements from `left` and `right`, in ascending order (or non-decreasing order, to be more precise).
    #
    # Note: this function is not conceptually difficult, but it is notoriously tricky to get all of the edge cases right without making the function unreadable.
    # Take it as a challenge to write a version that is correct, concise, and readable.
    # I found that I could write it more concisely as a generator function.

    # You can use the following example to test your code.

    # +
    import random

    population = range(100)
    xs = random.sample(population, k=6)
    ys = random.sample(population, k=6)
    ys
    # -

    xs.sort()
    ys.sort()
    ys

    res = list(merge(xs, ys))
    res

    sorted(res) == res

    # **Exercise:**  Starting with `merge_sort_norec`, write a function called `merge_sort_rec` that's fully recursive; that is, instead of using Python's `sort` function to sort the halves, it should use `merge_sort_rec`.  Of course, you will need a base case to avoid an infinite recursion.
    #
    #

    # Test your method by running the code in the next cell, then use `test_merge_sort_rec`, below, to check the performance of your function.

    xs = random.sample(population, k=12)
    xs

    res = list(merge_sort_rec(xs))
    res

    sorted(res) == res

    # ## Heap Merge
    #
    # Suppose we want to merge more than two sub-sequences.
    # A convenient way to do that is to use a heap.
    # For example, here are three sorted sub-sequences.

    # +
    xs = random.sample(population, k=5)
    ys = random.sample(population, k=5)
    zs = random.sample(population, k=5)

    min(xs), min(ys), min(zs)
    # -

    xs.sort()
    ys.sort()
    zs.sort()

    # For each sequence, I'll make an iterator and push onto the heap a tuple that contains:
    #
    # * The first element from the iterator,
    #
    # * An index that's different for each iterator, and
    #
    # * The iterator itself.
    #
    # When the heap compares two of these tuples, it compares the elements first.
    # If there's a tie, it compares the indices.
    # Since the indices are unique, there can't be a tie, so we never have to compare iterators (which would be an error).

    # + tags=[]
    sequences = [xs, ys, zs]

    # + tags=[]
    from heapq import heappush, heappop

    heap = []
    for i, seq in enumerate(sequences):
        iterator = iter(seq)
        first = next(iterator)
        heappush(heap, (first, i, iterator))
    # -

    # When we pop a value from the heap, we get the tuple with the smallest value.

    # + tags=[]
    value, i, iterator = heappop(heap)
    value
    # -

    # If we know that the iterator has more values, we can use `next` to get the next one and then push a tuple back into the heap.

    # + tags=[]
    heappush(heap, (next(iterator), i, iterator))
    # -

    # If we repeat this process, we'll get all elements from all sub-sequences in ascending order.
    #
    # However, we have to deal with the case where the iterator is empty.
    # In Python, the only way to check is to call `next` and take your chances!
    # If there are no more elements in the iterator, `next` raises a `StopIteration` exception, which you can handle with a `try` statement, like this:

    # + tags=[]
    iterator = iter(xs)

    while True:
        try:
            print(next(iterator))
        except StopIteration:
            break
    # -

    # **Exercise:** Write a generator function called `heapmerge` that takes a list of sequences and yields the elements from the sequences in increasing order.

    # You can use the following examples to test your function.

    seq = list(heapmerge([xs, ys, zs]))
    seq

    sorted(seq) == seq

    # The `heapq` module provides a function called `merge` that implements this algorithm.

    # ## Comparing sort algorithms
    #
    # NumPy provides implementations of three sorting algorithms, quicksort, mergesort, and heapsort.
    #
    # In theory that are all in `O(n log n)`.
    # Let's see what that looks like when we plot runtime versus problem size.
    #

    # +

    # download('https://github.com/AllenDowney/DSIRP/raw/main/timing.py')
    # -

    from timing import run_timing_test, plot_timing_test

    # +
    import numpy as np

    def test_quicksort(n):
        xs = np.random.normal(size=n)
        xs.sort(kind='quicksort')

    ns, ts = run_timing_test(test_quicksort)
    plot_timing_test(ns, ts, 'test_quicksort', exp=1)

    # -

    # quicksort is hard to distinguish from linear, up to about 10 million elements.

    # +
    def test_mergesort(n):
        xs = np.random.normal(size=n)
        xs.sort(kind='mergesort')

    ns, ts = run_timing_test(test_mergesort)
    plot_timing_test(ns, ts, 'test_mergesort', exp=1)

    # -

    # Merge sort is similar, maybe with some upward curvature.

    # +
    def test_heapsort(n):
        xs = np.random.normal(size=n)
        xs.sort(kind='heapsort')

    ns, ts = run_timing_test(test_quicksort)
    plot_timing_test(ns, ts, 'test_heapsort', exp=1)

    # -

    # The three methods are effectively linear over this range of problem sizes.
    #
    # And their run times are about the same, with quicksort being the fastest, despite being the one with the worst asympotic performance in the worst case.
    #
    # Now let's see how our implementation of merge sort does.

    # +
    def test_merge_sort_rec(n):
        xs = np.random.normal(size=n)
        spectrum = merge_sort_rec(xs)

    ns, ts = run_timing_test(test_merge_sort_rec)
    plot_timing_test(ns, ts, 'test_merge_sort_rec', exp=1)
    # -

    # If things go according to plan, our implementation of merge sort should be close to linear, or a little steeper.

    # *Data Structures and Information Retrieval in Python*
    #
    # Copyright 2021 Allen Downey
    #
    # License: [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-nc-sa/4.0/)
