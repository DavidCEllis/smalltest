Smalltest project structure
===========================

Smalltest consists of a few modules that perform distinct parts of the test setup.

**discover.py** contains the functions that search through the file system for test modules
and search the test modules for test functions to run.

**run.py** Handles running the tests that have been discovered by discover.py.
It provides a dictionary of test_module:test_name mapped to the result from running the test

**reporter.py** Handles the interpretation of the results from running a test suite.

