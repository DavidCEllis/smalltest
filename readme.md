# Smalltest - Minimal python unittest convenience #

Simple unittests, no additional required dependencies.

Smalltest until/unless I come up with a better name.

**This is still in the very early exploration stages and is mostly a learning project**

## Motivation ##
I was attempting to remove attrs as a dependency of splitguides and found that despite
doing so it would still end up in my working/testing environment because it was a 
dependency of pytest. I actually found there were a couple of extra usages of attrs
that hadn't been immediately caught because pytest was always in the environment used 
for development.

I really don't like writing unittest format tests but didn't want the extra dependencies
required by pytest, so I put together this barebones testing package in order to write
plain `test_*` functions.
