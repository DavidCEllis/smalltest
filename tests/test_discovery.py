import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from smalltest.discover import discover_tests

faketests = """

def test_fake():
    pass
    
def test_real():
    pass
    
def notatest():
    pass
"""


class TestDicover(unittest.TestCase):
    def test_single_file_full(self):
        with TemporaryDirectory() as tmpfolder:
            testfile = Path(tmpfolder) / "test_fake.py"
            testfile.write_text(faketests)

            expected = {testfile: ["test_fake", "test_real"]}
            result = discover_tests(tmpfolder)

            self.assertEqual(expected, result)

    def test_multiple_files(self):
        with TemporaryDirectory() as tmpfolder:
            testfile = Path(tmpfolder) / "test_fake.py"
            testfile.write_text(faketests)

            testfile2 = Path(tmpfolder) / "fake_test.py"
            testfile2.write_text(faketests)

            expected = {
                testfile: ["test_fake", "test_real"],
                testfile2: ["test_fake", "test_real"]
            }
            result = discover_tests(tmpfolder)

            self.assertEqual(expected, result)
