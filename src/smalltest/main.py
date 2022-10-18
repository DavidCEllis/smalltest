"""
Perform the various combinations of discovering and running tests
"""
from smalltest.discover import discover_tests
from smalltest.run import run_tests_serial
from smalltest.reporter import text_reporter


def discover_and_run(base_path):
    tests = discover_tests(base_path)
    test_results = run_tests_serial(tests)
    return test_results


if __name__ == "__main__":
    from pathlib import Path
    result = discover_and_run(Path.cwd())
    print("-"*50)
    text_reporter(result)
