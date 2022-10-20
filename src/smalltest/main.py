"""
Perform the various combinations of discovering and running tests
"""
import sys
import traceback

from contextlib import contextmanager
from enum import Enum
from io import StringIO
from pathlib import Path
from typing import TextIO, Optional, Union

from smalltest.discover import discover_tests
from smalltest.runner import run_tests_serial, ResultType
from smalltest.reporter import text_reporter


class ExitCode(Enum):
    """Numeric exit codes - matching pytest codes"""
    SUCCESS = 0
    FAILED_TESTS = 1
    ERROR_TESTS = 2
    ERROR_DISCOVERY = 3
    ERROR_RUN = 4
    ERROR_REPORT = 5


@contextmanager
def coverage_if_available():
    try:
        import coverage
    except ImportError:
        yield None
    else:
        cov = coverage.Coverage()
        cov.start()
        cov_output = StringIO()
        yield cov_output
        cov.stop()
        cov.save()
        cov.report(file=cov_output, show_missing=True)


def discover_run_report(
        base_path: Optional[Union[str, Path]] = None,
        strict_xfail: bool = False,
        stream: TextIO = sys.stdout
) -> ExitCode:

    # Discover Tests
    try:
        tests = discover_tests(base_path)
    except Exception as e:
        traceback.print_exception(e)
        return ExitCode.ERROR_DISCOVERY

    # Setup Coverage Before Import
    with coverage_if_available() as cov_output:
        try:
            test_results = run_tests_serial(tests, stream=stream)
        except Exception as e:
            traceback.print_exception(e)
            return ExitCode.ERROR_RUN

    # Report results of tests
    try:
        report = text_reporter(
            test_results,
            stream=stream,
            strict_xfail=strict_xfail
        )
    except Exception as e:
        traceback.print_exception(e)
        return ExitCode.ERROR_REPORT

    if report[ResultType.ERROR] > 0:
        return ExitCode.ERROR_TESTS
    if report[ResultType.FAILURE] > 0:
        return ExitCode.FAILED_TESTS

    # If coverage ran, print the coverage report here
    # only on successful tests.
    if cov_output is not None:
        stream.write("\nCoverage Report\n")
        stream.write(cov_output.getvalue())

    return ExitCode.SUCCESS


if __name__ == "__main__":
    result = discover_run_report()
    sys.exit(result.value)
