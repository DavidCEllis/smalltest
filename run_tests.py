"""
Run the tests using unittest
"""
from io import StringIO
import unittest
import coverage
from pathlib import Path

test_root = str(Path(__file__).parent / "tests_unittest")


def run_unittest_with_cov():
    loader = unittest.defaultTestLoader
    runner = unittest.TextTestRunner(verbosity=2)

    cov = coverage.Coverage(omit=["tests_unittest/*"])
    cov.start()

    tests = loader.discover(start_dir=test_root)
    runner.run(tests)

    cov.stop()
    cov.save()

    cov_out = StringIO()
    cov.report(file=cov_out, show_missing=True)
    print(cov_out.getvalue())


if __name__ == "__main__":
    run_unittest_with_cov()
