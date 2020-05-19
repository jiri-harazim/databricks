#!/usr/bin/env bash
python setup.py sdist bdist_wheel
python setup.py test
