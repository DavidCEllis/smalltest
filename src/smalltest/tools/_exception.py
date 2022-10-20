import sys

from contextlib import contextmanager
from typing import Type, Union


ExceptionType = Type[Exception]


class ExceptionHolder:
    def __init__(self):
        self.type = None
        self.value = None
        self.traceback = None

    def set_exception(self, exc_info):
        self.type, self.value, self.traceback = exc_info


@contextmanager
def raises(expected_exception: Union[ExceptionType, tuple[ExceptionType, ...]]):
    exception_holder = ExceptionHolder()
    try:
        yield exception_holder
    except expected_exception:
        exception_holder.set_exception(sys.exc_info())
    else:
        raise AssertionError(
            f"Expected exception {expected_exception.__name__} was not raised."
        )
