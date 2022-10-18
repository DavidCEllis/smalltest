from .run import ResultType


def text_reporter(test_results):
    """
    Basic reporter that prints a text report of failed tests and captured stdout/stderr/warnings
    :param test_results: Results from a test run
    """
    for test_name, test_result in test_results.items():
        match test_result.result_type:
            case ResultType.FAILURE:
                print(f"{test_name} Failed - {test_result.exception_args}")
