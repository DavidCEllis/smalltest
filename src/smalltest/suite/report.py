import sys
import traceback
from collections import Counter

from typing import TextIO

from .run import ResultType, TestResult
from smalltest.util import WritelnDecorator


def text_reporter(
        test_results: dict[str, TestResult],
        stream: TextIO = None,
        strict_xfail: bool = False
) -> dict[ResultType, int]:
    """
    Basic reporter that writes a text report of failed tests
    and captured stdout/stderr/warnings
    :param test_results: Results from a test run
    :param stream: Stream to write text results to.
    :param strict_xfail: Report XPASS as failure
    """
    test_counts = Counter()

    stream = stream if stream else sys.stdout
    stream = WritelnDecorator(stream)

    for test_name, test_result in test_results.items():
        # XPASS on strict_xfail is counted as failure
        if strict_xfail and test_result.result_type == ResultType.XPASS:
            test_counts[ResultType.FAILURE] += 1
        else:
            test_counts[test_result.result_type] += 1

        match test_result.result_type:
            case ResultType.FAILURE:
                stream.writeln(f"{test_name} Failed")
                for arg in test_result.exception.args:
                    stream.writeln(f"\t{arg}")
                stream.writeln("")
            case ResultType.XPASS:
                if strict_xfail:
                    stream.writeln(f"{test_name} Unexpectedly Passed")
                    for arg in test_result.exception.args:
                        stream.writeln(f"\t{arg}")
                    stream.writeln("")
            case ResultType.ERROR:
                stream.writeln(f"{test_name} threw an unexpected exception")
                stream.writeln(f"\tError     {test_result.exception.name}")
                stream.writeln(f"\tMessage")
                for arg in test_result.exception.args:
                    stream.writeln(f"\t\t{arg}")
                stream.writeln(f"\tTraceback")
                formatted_tb = traceback.format_tb(test_result.exception.traceback)
                for line in formatted_tb[1:]:  # Skip the line from running the test itself
                    print(line)
                stream.writeln("")

    digits = len(str(test_counts.total()))

    failure_count = (
            test_counts[ResultType.FAILURE] + test_counts[ResultType.ERROR]
    )
    if strict_xfail:
        failure_count += test_counts[ResultType.XPASS]

    # Extra delimiter if any tests failed
    if failure_count > 0:
        stream.writeln("=" * (digits + 10))  # 10 is length of text

    stream.writeln(f"Ran {test_counts.total():{digits}d} Tests")
    if test_counts[ResultType.SUCCESS]:
        stream.writeln(
            f"    {test_counts[ResultType.SUCCESS]:{digits}d} Passed"
        )
    if test_counts[ResultType.FAILURE]:
        stream.writeln(
            f"    {test_counts[ResultType.FAILURE]:{digits}d} Failed"
        )
    if test_counts[ResultType.XFAIL]:
        stream.writeln(
            f"    {test_counts[ResultType.XFAIL]:{digits}d} XFailed"
        )
    if test_counts[ResultType.XPASS]:
        stream.writeln(
            f"    {test_counts[ResultType.XPASS]:{digits}d} XPassed"
        )
    if test_counts[ResultType.SKIP]:
        stream.writeln(
            f"    {test_counts[ResultType.SKIP]:{digits}d} Skipped"
        )
    if test_counts[ResultType.ERROR]:
        stream.writeln(
            f"    {test_counts[ResultType.ERROR]:{digits}d} "
            f"Failed to run due to errors"
        )

    return test_counts
