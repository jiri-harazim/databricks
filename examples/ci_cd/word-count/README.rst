==========
word-count
==========


Word-count is an example project that shows how to build a pyspark project
together with CI CD.
Author: jiri.harazim@databricks.com


Steps
=====

1. clone github project from repo
#. shell: ``putup word-count # This uses scaffolding to create a project skeleton``
#. create and activate conda environment word-count
#. ``pip install -e .``
#. ``pip install word-count[testing]`` # Installs dependencies like pytest, flake8 defined in setup.cfg
#. shell: ``python setup.py test`` to test the installation and see tests are passing, incl code coverage.
#. Configure DBConnect (https://docs.microsoft.com/en-us/azure/databricks/dev-tools/databricks-connect) and test it works
#. ``pip install -U databricks-connect``
#. ``databricks-connect configure`` and enter URL/token/clusterID,..
#. Alternatively, update the file manually `` vi ~/.databricks-connect``
#. Add ``databricks-connect`` to requirements.txt
#. Install ``pip install -U databricks-connect`` (ToDo: use the file/conda yml?)
#. Test your setup works: ``databricks-connect test``
#. Write your code, eg create dbconnect_example.py
#. Run your code, it should work and execute on cluster
#. Test: add your tests.. run ``python setup.py test``
#. Test: Build a wheel ``setup.py sdist bdist_wheel``
#. CI CD: Create build.sh and enter your ci cd commands
#.
