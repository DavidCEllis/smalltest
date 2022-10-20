"""
Perform the various combinations of discovering and running tests
"""
import sys
import traceback

from enum import Enum

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


def discover_run_report(base_path=None, strict_xfail=False) -> ExitCode:
    # Discover Tests
    try:
        tests = discover_tests(base_path)
    except Exception as e:
        traceback.print_exception(e)
        return ExitCode.ERROR_DISCOVERY

    # Run Tests
    try:
        test_results = run_tests_serial(tests, stream=sys.stderr)
    except Exception as e:
        traceback.print_exception(e)
        return ExitCode.ERROR_RUN

    # Report results of tests
    try:
        report = text_reporter(
            test_results,
            stream=sys.stdout,
            strict_xfail=strict_xfail
        )
    except Exception as e:
        traceback.print_exception(e)
        return ExitCode.ERROR_REPORT

    if report[ResultType.ERROR] > 0:
        return ExitCode.ERROR_TESTS
    if report[ResultType.FAILURE] > 0:
        return ExitCode.FAILED_TESTS

    return ExitCode.SUCCESS


if __name__ == "__main__":
    result = discover_run_report()
    sys.exit(result.value)
