from smalltest.markers import xfail


@xfail(True, "Test is always false.")
def test_1_is_2():
    assert 1 == 2, 'Does 1 == 2'
