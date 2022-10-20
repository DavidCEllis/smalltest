# Test structure #
This document tries to explain how the test runner works and how
all the parts are connected.

## discover.py ##
**discover.py** provides methods to find test files and functions for the 
testrunner. 

The main function `discover_tests` finds files matching `"test_*.py"` or
`"*_test.py"` by within the base folder and a `"tests"` subfolder if it exists.
It then looks within these files using the AST to find any module level 
functions that match the prefix `"test_"`. It returns a dictionary of 
`{ module_path: [test_function, ...] }`.

An example of the use case is something like this:
```python
>>> from pprint import pprint
>>> from smalltest.discover import discover_tests
>>> tests = discover_tests()
>>> pprint(tests)
{Path('tests/test_discovery.py'): ['test_discover_tests_single',
                                   'test_discover_tests_multiple',
                                   'test_discover_modules',
                                   'test_discover_test_functions'],
...
}
```

## runner.py ##
**runner.py** handles the running of tests and capturing output. 

The main function `run_test` takes a single test function, runs it and 
captures the output, returning a `TestResult` object with the output details.

`run_tests_serial` is the current handler for running all of the tests in a 
single threaded mode. Given the output from `discover_tests` it imports the
necessary module and provides the tests to `run_test` and provides a quick
report indicating whether the test has passed or failed to a provided stream.
It then returns a dictionary mapping the module and test name to the
corresponding `TestResult`.

Example given the output from `discover_tests()`
```python
>>> from smalltest.runner import run_tests_serial
>>> results = run_tests_serial(tests)
=========================================
Smalltest: running 5 tests from 2 modules
=========================================
[1/5] test_discovery::test_discover_tests_single - Success
[2/5] test_discovery::test_discover_tests_multiple - Success
[3/5] test_discovery::test_discover_modules - Success
[4/5] test_discovery::test_discover_test_functions - Success
[5/5] test_fail::test_1_is_2 - XFailed
=========================================

>>> print(result["test_fail::test_1_is_2"])
TestResult(result_type=<ResultType.XFAIL: 2>, exception_args=('Test is always false.', 'Does 1 == 2'), stdout='Captured STDOUT', stderr='Captured STDERR', warnings=[])
```

