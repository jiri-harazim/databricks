============
my_functions
============

Use this example as a sample python library, eg. for demonstrating CI CD, features like DBConnect
and debugging.

It is a dummy python project that contains a couple of simple functions (eg string manipulation).


Get started
===========

1. Clone this repo and prepare your environment

```
pip install -e .
pip install my_functions[testing]
python setup.py test
```

2. Build a wheel
```
python setup.py bdist_wheel
```

3. Use it in tutorials and examples

Description
===========

This project gives you a python library, eg wheel. If you want to see how to use this library in Databricks,
check this [Databricks notebook] (https://github.com/jiri-harazim/databricks-public/tree/master/examples/notebooks/misc).


Note
====

This project has been set up using PyScaffold 3.2.3. For details and usage
information on PyScaffold see https://pyscaffold.org/.
