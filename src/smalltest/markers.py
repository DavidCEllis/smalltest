"""
Special test decorators to mark for skip/xfail/parameterized tests
"""
from functools import wraps


# Normally a test can only pass or fail, provide special exceptions
# for alternative  test conditions
class MarkerException(Exception):
    """Exception markers used to replace original errors"""


class XFailMarker(MarkerException):
    """Exception raised when a test XFails"""


class XPassMarker(MarkerException):
    """Exception raised when a test XPasses"""


class SkipMarker(MarkerException):
    """Exception raised when a test is skipped"""


def skip(reason=''):
    def skipped(func):
        @wraps(func)
        def inner():
            raise SkipMarker(reason)
        return inner
    return skipped


def skipif(condition, reason=''):
    def skipped(func):
        if condition:
            @wraps(func)
            def inner():
                raise SkipMarker(reason)
            return inner
        else:
            return func
    return skipped


def xfail(condition=True, reason=''):
    def xfailed(func):
        if condition:
            @wraps(func)
            def inner():
                try:
                    func()
                except AssertionError as e:
                    raise XFailMarker(reason, *e.args)
                else:
                    raise XPassMarker(reason)
            return inner
        else:
            return func
    return xfailed
