"""
Run the tests_unittest
"""
import enum
import importlib.util
import warnings

from collections import namedtuple
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO

TestResult = namedtuple(
    "TestResult",
    ["result_type", "exception_args", "stdout", "stderr", "warnings"]
)


class ResultType(enum.Enum):
    SUCCESS = 0
    FAILURE = 1
    XFAIL = 2
    XPASS = 3
    SKIP = 4


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
            ResultType.FAILURE, e.args, stdout.getvalue(), stderr.getvalue(), warns
        )
    else:
        result = TestResult(
            ResultType.SUCCESS, None, stdout.getvalue(), stderr.getvalue(), warns
        )

    return result


# noinspection PyUnresolvedReferences
def run_tests_serial(test_dict):
    results = {}
    for module_path, test_names in test_dict.items():

        # Load the test module
        module_name = module_path.stem
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Collect the results
        for test_name in test_names:
            result = run_test(getattr(module, test_name))

            match result.result_type:
                case ResultType.SUCCESS:
                    print(f"{module_name}:{test_name} - Success")
                case ResultType.FAILURE:
                    print(f"{module_name}:{test_name} - Failure")

            results[f"{module_name}:{test_name}"] = result

    return results

