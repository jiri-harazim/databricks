# -*- coding: utf-8 -*-

import pytest
from word_count.skeleton import fib

__author__ = "Jiri Harazim"
__copyright__ = "Jiri Harazim"
__license__ = "mit"


def test_fib():
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(7) == 13
    with pytest.raises(AssertionError):
        fib(-10)
