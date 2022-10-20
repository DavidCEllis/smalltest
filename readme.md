# Smalltest - Minimal python unittest convenience #

Simple unittests, no additional required dependencies.

Smalltest until/unless I come up with a better name.

This is still in the very early exploration stages.

Written mostly as a learning project, but also after finding out that another
project I was working on was still dependant on attrs in the development
environment due to the use of pytest.

The core features this intends to support are:
   1. Writing tests as plain `test_this` named functions without the need for `unittest.TestCase`
      classes. 🗹
   2. Getting useful information from plain `assert` statements to remove the need for 
      assertXYZ style functions. ☐
   3. Some basic decorators to provide xfail/skipif/parametrized tests. 🗹🗹☐
