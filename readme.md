# Smalltest - Minimal python unittest convenience #

An attempt to make a minimal python unittest runner designed to allow for simple
pytest style test writing without requiring any dependencies outside of the 
stdlib.

Partly written to figure out how something like pytest could work, partly
because while removing attrs as a dependency in another project I found out 
it was still being installed as a requirement for pytest.

The core features this intends to support are:
   1. Writing tests as plain `test_this` named functions without the need for `unittest.TestCase`
      classes. 🗹
   2. Getting useful information from plain `assert` statements to remove the need for 
      assertXYZ style functions. ☐
   3. Some basic decorators to provide xfail/skipif/parametrized tests. 🗹🗹☐
