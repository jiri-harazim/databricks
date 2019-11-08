import pytest
from my_functions.formatter import decorate

def test_decorate():
    assert "HELLO" == decorate("hello")