import os

import pytest

from dsirp.t01_algorithms.algorithms import read_words

current_file = os.path.abspath(__file__)
test_dir, current_tail = os.path.split(current_file)
test_head, test_tail = os.path.split(test_dir)
top_test_dir, test_head_tail = os.path.split(test_head)
data_dir = os.path.join(top_test_dir, "data")


@pytest.fixture(name="word_list")
def word_list_fixture():
    return read_words(f"{data_dir}/american-english")
