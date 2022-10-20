"""
Perform the various combinations of discovering and running tests
"""
import sys

from smalltest.discover import discover_tests
from smalltest.run import run_tests_serial
from smalltest.reporter import text_reporter


def discover_and_run():
    try:
        base_path = sys.argv[1]
    except IndexError:
        base_path = None
    tests = discover_tests(base_path)
    test_results = run_tests_serial(tests, stream=sys.stderr)
    text_reporter(test_results, stream=sys.stderr)


if __name__ == "__main__":
    discover_and_run()
