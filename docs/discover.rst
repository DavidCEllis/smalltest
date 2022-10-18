discover.py
-----------
This module is made up of 3 functions that help to discover test files and functions from
the working directory.


.. py:function:: discover_test_modules(base_path=Path.cwd(), *, test_file_names=["test_*.py", "*_test.py"], test_folder_names=["tests"])

    | Search base_path for files matching test_file_names patterns.
    | Search recursively through any subfolders matching test_folder_names for
    | any files matching test_file_names patterns.
    | Return a list of matching files.


.. py:function:: discover_test_functions(test_files, *, test_prefix="test_")

    | Search the AST of each file in test_files for functions at module level
    | that have the matching test prefix.
    | Return a matching dict of { path: [test_function, ...], ... }


.. py:function:: discover_tests(base_path=Path.cwd(), *, test_file_names=["test_*.py", "*_test.py"], test_folder_names=["tests"], test_prefix=="test_")

    | Search base_path for test modules using discover_test_modules
    | For each module returned search for matching test functions
    | Return a dictionary of { path: [test_function,...], ... }