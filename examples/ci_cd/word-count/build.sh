#!/usr/bin/env bash
python setup.py test
pip install wheel
python setup.py sdist bdist_wheel
mv dist/word_count-0.0.post0.*-py2.py3-none-any.whl dist/word_count-0.0.1-py2.py3-none-any.whl
