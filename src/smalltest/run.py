"""
Run the tests_unittest
"""
import importlib.util
import warnings

from collections import namedtuple
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO

TestResult = namedtuple(
    "TestResult",
    ["success", "exception_args", "stdout", "stderr", "warnings"]
)


def run_test(test):
    """
    Run the test function, capture stdout, stderr and uncaught warnings
    to display in the report.

    :param test function - callable
    :return: TestResult
    """
    stdout = StringIO()
    stderr = StringIO()
    try:
        with redirect_stdout(stdout), \
             redirect_stderr(stderr), \
             warnings.catch_warnings(record=True) as warns:
            test()
    except AssertionError as e:
        result = TestResult(
            False, e.args, stdout.getvalue(), stderr.getvalue(), warns
        )
    else:
        result = TestResult(
            True, None, stdout.getvalue(), stderr.getvalue(), warns
        )

    return result


def run_tests_serial(test_dict):
    results = {}
    for module_path, test_names in test_dict.items():
        module_name = module_path.stem
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        results[module_name] = []

        for test_name in test_names:
            result = run_test(getattr(module, test_name))
            if result.success:
                print(f"{test_name} - Success")
            else:
                print(f"{test_name} - Failure")

        results[module_name] = [
            run_test(getattr(module, test_name))
            for test_name in test_names
        ]
    return results

