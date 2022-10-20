import sys
from collections import Counter

from .run import ResultType


def text_reporter(test_results, strict_xfail=False):
    """
    Basic reporter that prints a text report of failed tests and captured stdout/stderr/warnings
    :param test_results: Results from a test run
    :param strict_xfail: Report XPASS as failure
    """
    test_counts = Counter()

    for test_name, test_result in test_results.items():
        test_counts[test_result.result_type] += 1
        match test_result.result_type:
            case ResultType.FAILURE:
                print(f"{test_name} Failed")
                for arg in test_result.exception_args:
                    print(f"\t{arg}")
            case ResultType.XPASS:
                if strict_xfail:
                    print(f"{test_name} Unexpectedly Passed")
                    for arg in test_result.exception_args:
                        print(f"\t{arg}")

    print("=" * 50)
    print(f"Ran {test_counts.total()} Tests")
    if test_counts[ResultType.SUCCESS]:
        print(f"\t{test_counts[ResultType.SUCCESS]} Passed")
    if test_counts[ResultType.FAILURE]:
        print(f"\t{test_counts[ResultType.FAILURE]} Failed")
    if test_counts[ResultType.XFAIL]:
        print(f"\t{test_counts[ResultType.XFAIL]} XFailed")
    if test_counts[ResultType.XPASS]:
        print(f"\t{test_counts[ResultType.XPASS]} XPassed")
    if test_counts[ResultType.SKIP]:
        print(f"\t{test_counts[ResultType.SKIP]} Skipped")
