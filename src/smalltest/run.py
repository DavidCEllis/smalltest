"""
Run the tests
"""
import warnings
from collections import namedtuple
from io import StringIO
from contextlib import redirect_stderr, redirect_stdout

TestResult = namedtuple("TestResult", ["Success", "ExceptionArgs", "stdout", "stderr", "warnings"])


def run_test(test):
    """
    Run the test function
    :param test
    :return: TestResult
    """
    stdout = StringIO()
    stderr = StringIO()
    try:
        with redirect_stdout(stdout), redirect_stderr(stderr), warnings.catch_warnings(record=True) as warns:
            test()
    except AssertionError as e:
        result = TestResult(False, e.args, stdout.getvalue(), stderr.getvalue(), warns)
    else:
        result = TestResult(True, None, stdout.getvalue(), stderr.getvalue(), warns)

    return result


def load_test(module, testname):
    """
    Load the module into memory
    Yield the test function
    Clean up the module and assorted code

    :param module: python file path for test file
    :param testname: name of specific test to run
    :return:
    """
