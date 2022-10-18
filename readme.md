# Smalltest - Minimal python unittest convenience #

An attempt to make a minimal python unittest runner designed to allow for simple pytest
style test writing without requiring any dependencies outside of the stdlib.

The core features this intends to support are:
   1. Writing tests as plain `test_this` named functions without the need for `unittest.TestCase`
      classes.
   2. Getting useful information from plain `assert` statements to remove the need for 
      assertXYZ style functions.
   3. Some basic decorators to provide xfail/skipif/parametrized tests
   
Anything further is up to the user to provide (unless I end up needing it and make my own)


