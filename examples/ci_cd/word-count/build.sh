#!/usr/bin/env bash
set -x
python setup.py test
pip install wheel
python setup.py sdist bdist_wheel
echo "Current dir: $(pwd)"
mv dist/word_count-0.0.post0.*-py2.py3-none-any.whl dist/word_count-0.0.1-py2.py3-none-any.whl
echo "ls dist: $(ls dist) ls build: $(ls build) ls cov_report: $(ls cov_html)"

