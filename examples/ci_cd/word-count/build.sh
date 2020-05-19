#!/usr/bin/env bash
python setup.py test
pip install wheel
python setup.py sdist bdist_wheel
