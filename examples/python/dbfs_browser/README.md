### About

This example shows how to bundle dbutils into a library that can be used in your python programs or in databricks notebooks.

### Getting started

1. Create a cluster in Databricks
1. For local development: Install and configure your databricks-connect on your laptop so you can connect to a databricks cluster.
    ```
    pip install -U databricks-connect==6.2 # replace 6.2 with your databricks cluster runtime version
    ```
    See [databricks documentation](https://docs.databricks.com/dev-tools/databricks-connect.html) for complete steps.
    If you use databricks-connect often, you can alternatively edit ~/.databricks-connect file.
1.  Install requiremens.txt (six) to use DBUtils locally. You don't need to install 'six' package on your databricks cluster.
1.  Develop & run you code as needed, eg see list_dbfs_test.py how to list DBFS.
1.  Build a wheel
    1. Install setuptools: 
    
    ```python3 -m pip install --user --upgrade setuptools wheel```
    1. Build a wheel (it will be created in 'dist' folder): 
    
    ```python3 setup.py sdist bdist_wheel```
1. Install wheel into your cluster (ToDo: Add API call how to do it via cli/REST) or distribute it to your colleagues. Your colleagues need to follow previous steps to setup their dbconnect environment.

### Summary
 
You have a python wheel where you can add your code specific to your project and use it both locally or remotely.