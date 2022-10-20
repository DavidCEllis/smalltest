from contextlib import contextmanager
from typing import Type, Union


ExceptionType = Type[Exception]


class ExceptionHolder:
    def __init__(self):
        self.exception = None


@contextmanager
def raises(expected_exception: Union[ExceptionType, tuple[ExceptionType, ...]]):
    exception_holder = ExceptionHolder()
    try:
        yield exception_holder
    except expected_exception as e:
        exception_holder.exception = e
    else:
        raise AssertionError(
            f"Expected exception {expected_exception.__name__} was not raised."
        )
