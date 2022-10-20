import sys
from smalltest.markers import xfail


@xfail(True, "Test is always false.")
def test_1_is_2():
    sys.stdout.write("Captured STDOUT")
    sys.stderr.write("Captured STDERR")
    assert 1 == 2, 'Does 1 == 2'
