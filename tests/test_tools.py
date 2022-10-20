"""
A small set of tests designed to skip or xfail
"""
import sys

from smalltest.tools import xfail, raises


@xfail(reason="Test is always false.")
def test_1_is_2():
    sys.stdout.write("Captured STDOUT")
    sys.stderr.write("Captured STDERR")
    assert 1 == 2, 'Does 1 == 2'


@xfail(reason="Doesn't throw the exception")
def test_exception_failure():
    with raises(TypeError):
        pass


# noinspection PyTypeChecker
def test_exception_success():
    with raises(TypeError):
        result = 1 + "apple"
