import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from smalltest.discover import discover_tests, discover_test_functions, discover_test_modules

faketests = """

def test_fake():
    pass
    
def test_real():
    pass
    
def notatest():
    pass
"""


class TestDicover(unittest.TestCase):
    def test_discover_tests_single(self):
        with TemporaryDirectory() as tmpfolder:
            testfile = Path(tmpfolder) / "test_fake.py"
            testfile.write_text(faketests)

            expected = {testfile: ["test_fake", "test_real"]}
            result = discover_tests(base_path=tmpfolder)

            self.assertEqual(expected, result)

    def test_discover_tests_multiple(self):
        with TemporaryDirectory() as tmpfolder:
            testfile = Path(tmpfolder) / "test_fake.py"
            testfile.write_text(faketests)

            testfile2 = Path(tmpfolder) / "fake_test.py"
            testfile2.write_text(faketests)

            expected = {
                testfile: ["test_fake", "test_real"],
                testfile2: ["test_fake", "test_real"]
            }
            result = discover_tests(base_path=tmpfolder)

            self.assertEqual(expected, result)

    def test_discover_modules(self):
        with TemporaryDirectory() as tmpfolder:
            testfile = Path(tmpfolder) / "test_fake.py"
            testfile.write_text(faketests)

            testfile2 = Path(tmpfolder) / "fake_test.py"
            testfile2.write_text(faketests)

            expected = sorted([testfile, testfile2])
            result = sorted(discover_test_modules(base_path=tmpfolder))

            self.assertEqual(expected, result)

    def test_discover_test_functions(self):
        with TemporaryDirectory() as tmpfolder:
            testfile = Path(tmpfolder) / "test_fake.py"
            testfile.write_text(faketests)

            expected = {testfile: ['test_fake', 'test_real']}
            result = discover_test_functions(test_files=[testfile])

            self.assertEqual(expected, result)
