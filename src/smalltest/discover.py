"""
Discover the paths and the names of each test that needs to run.

This uses a simple pathlib glob to recursively search for test files.
Using the ast module it then finds any defined functions with names that
start with the test prefix.
"""
import ast
from pathlib import Path
# When python 3.11 is released make this customizable from pyproject.toml
TEST_FOLDER_NAMES = ["tests"]
TEST_FILE_NAMES = ["test_*.py", "*_test.py"]


# noinspection PyDefaultArgument
def discover_test_modules(
        base_path=None,
        *,
        test_file_names=TEST_FILE_NAMES,
        test_folder_names=TEST_FOLDER_NAMES
):
    """
    Find and return a list of python test files matching the TEST_FILE_NAMES
    wildcards
    :param base_path: Path to start the search for test folders
    :param test_file_names:
    :param test_folder_names:
    :return: (absolute test_file paths)
    """
    # Default to CWD/relative_to to base_path if not given
    base_path = Path.cwd() if base_path is None else Path(base_path)

    test_files = []
    for file_name in test_file_names:
        test_files.extend(base_path.glob(file_name))
        for folder in test_folder_names:
            test_files.extend(base_path.glob(f"{folder}/**/{file_name}"))

    return test_files


def discover_test_functions(test_files, *, test_prefix="test_"):
    """
    Use the abstract syntax tree of the source in the test files to find the
    name of all the functions that match the test prefix.

    :param test_files: paths to python test module
    :param test_prefix: prefix for test functions
    :return: {test_path: [test_function_name, ...]}
    """

    test_functions = {}
    for pth in test_files:
        # Parse the source of the text file into an AST
        tree = ast.parse(pth.read_text())

        test_functions[pth] = [
            testfunc.name for testfunc in tree.body
            if isinstance(testfunc, ast.FunctionDef)
            and testfunc.name.startswith(test_prefix)
        ]

    return test_functions


# noinspection PyDefaultArgument
def discover_tests(
        base_path=None,
        *,
        test_file_names=TEST_FILE_NAMES,
        test_folder_names=TEST_FOLDER_NAMES,
        test_prefix="test_",
):
    test_files = discover_test_modules(base_path,
                                       test_file_names=test_file_names,
                                       test_folder_names=test_folder_names
                                       )
    test_dict = discover_test_functions(test_files, test_prefix=test_prefix)
    return test_dict


if __name__ == '__main__':  # pragma: nocover
    cwd = Path.cwd()
    print(f"Discovering tests_unittest in {cwd}")
    for module, tests in discover_tests(cwd).items():
        print(f"Tests in {module.relative_to(cwd)}")
        for test in tests:
            print(f"\t{test}")
