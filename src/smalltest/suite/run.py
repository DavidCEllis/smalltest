"""
Run the tests_unittest
"""
import sys
import enum
import importlib.util
import warnings

from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path
from typing import Any, Callable, Optional, TextIO
from typing import NamedTuple
from types import TracebackType

from smalltest.tools import XFailMarker, XPassMarker, SkipMarker
from smalltest.util import WritelnDecorator


class TestResult(NamedTuple):
    result_type: "ResultType"
    exception: Optional["ErrorDetails"]
    stdout: str
    stderr: str
    warnings: list[warnings.WarningMessage]


class ErrorDetails(NamedTuple):
    args: tuple[Any, ...]
    name: Optional[str] = None
    traceback: Optional[TracebackType] = None


class ResultType(enum.Enum):
    ERROR = -1
    SUCCESS = 0
    FAILURE = 1
    XFAIL = 2
    XPASS = 3
    SKIP = 4


def run_test(test: Callable) -> TestResult:
    """
    Run the test function, capture stdout, stderr and uncaught warnings
    to display in the report.

    :param test function
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
            ResultType.FAILURE,
            ErrorDetails(e.args, traceback=e.__traceback__),
            stdout.getvalue(),
            stderr.getvalue(),
            warns
        )
    except XFailMarker as e:
        result = TestResult(
            ResultType.XFAIL,
            ErrorDetails(e.args),
            stdout.getvalue(),
            stderr.getvalue(),
            warns
        )
    except XPassMarker as e:
        result = TestResult(
            ResultType.XPASS,
            ErrorDetails(e.args),
            stdout.getvalue(),
            stderr.getvalue(),
            warns
        )
    except SkipMarker as e:
        result = TestResult(
            ResultType.SKIP,
            ErrorDetails(e.args),
            stdout.getvalue(),
            stderr.getvalue(),
            warns
        )
    except Exception as e:
        # In the case of an unexpected error, also provide more error info
        result = TestResult(
            ResultType.ERROR,
            ErrorDetails(
                e.args,
                name=e.__class__.__qualname__,
                traceback=e.__traceback__
            ),
            stdout.getvalue(),
            stderr.getvalue(),
            warns
        )
    else:
        result = TestResult(
            ResultType.SUCCESS,
            None,
            stdout.getvalue(),
            stderr.getvalue(),
            warns
        )

    return result


# noinspection PyUnresolvedReferences
def run_tests_serial(
        test_dict: dict[Path, list[str]],
        stream: Optional[TextIO] = None
) -> dict[str, TestResult]:
    """
    Run the tests one at a time serially.

    :param test_dict: { module: [test_name, ...] }
    :param stream: Output stream - should be stdout/stderr or equivalent
    :return: result dict
    """
    results = {}
    stream = stream if stream else sys.stdout
    stream = WritelnDecorator(stream)

    test_total = sum(len(tests) for tests in test_dict.values())
    test_counter = 0

    top_banner = (f"Smalltest: running {test_total} tests "
                  f"from {len(test_dict)} modules")

    delimiters = "=" * len(top_banner)

    stream.writeln(delimiters)
    stream.writeln(top_banner)
    stream.writeln(delimiters)

    for module_path, test_names in test_dict.items():

        # Load the test module
        module_name = module_path.stem
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)

        # Collect the results
        for test_name in test_names:
            test_counter += 1
            result = run_test(getattr(module, test_name))
            stream.write(f"[{test_counter}/{test_total}] ")

            full_test_name = f"{module_name}::{test_name}"

            match result.result_type:
                case ResultType.SUCCESS:
                    stream.writeln(f"{full_test_name} - Success")
                case ResultType.FAILURE:
                    stream.writeln(f"{full_test_name} - Failure")
                case ResultType.XFAIL:
                    stream.writeln(f"{full_test_name} - XFailed")
                case ResultType.XPASS:
                    stream.writeln(f"{full_test_name} - XPassed")
                case ResultType.SKIP:
                    stream.writeln(f"{full_test_name} - Skipped / "
                                   f"{result.exception.args[0]}")
                case ResultType.ERROR:
                    stream.writeln(f"{full_test_name} - ERROR")

            results[full_test_name] = result
        stream.flush()
    stream.writeln(delimiters)
    stream.flush()
    return results
