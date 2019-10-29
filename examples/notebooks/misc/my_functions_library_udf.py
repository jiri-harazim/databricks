# Databricks notebook source
# MAGIC %md
# MAGIC ### Working with libraries
# MAGIC This notebook shows how to install a (python) library into Databricks and use it with the pyspark API via udf (user defined function).

# COMMAND ----------

# MAGIC %md
# MAGIC You can install library in the following scopes
# MAGIC 1. Workspace-wide (and enable or disable on all clusters via UI)
# MAGIC 1. Cluster-wide (via UI, REST API, containers or init scripts)
# MAGIC 1. Notebook-session wide (via dbutils, see example below)
# MAGIC 1. Driver only (via pip). Note: you usually don't want this as the library would be missing on workers. But it is a common error for newcomers.

# COMMAND ----------

# Example: Combination of step 1 and 3.
# 1. Install (or rather upload) library workspace-wide. This will store her into /FileStore/jars/... location. Remember the location.
# 2. Use dbutils to install the library into this notebook session

# Code:
## If you installed library workspace-wide, it will be stored in a (similar but no the same) path
# dbutils.library.install('dbfs:/FileStore/jars/a4458173_f07d_404a_9c9a_f0ed86026c28/my_functions-0.0.post0.dev2+gbeb1c4b-py2.py3-none-any.whl')
## You should see the library in the list
# dbutils.library.list()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Prework: Build your library
# MAGIC This step requires for you to work outside of this Databricks notebook shortly. Finish the steps below and come back.
# MAGIC 
# MAGIC 
# MAGIC 1. Clone this python project and build a wheel
# MAGIC https://github.com/jiri-harazim/databricks-public/tree/master/my_functions
# MAGIC ToDo: Add wheel build instructions to README.md in github
# MAGIC 1. Install the library using one of the following methods above.
# MAGIC 
# MAGIC Ready? Proceed below.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Use your function in this notebook

# COMMAND ----------

from my_functions import formatter

# Test the library works.
assert 'HELLO' == formatter.decorate('hello')

# COMMAND ----------

# Create a dummy dataset we will test our function on
people = spark.createDataFrame([('Jim', 2), ('Monica', 3)], "name: string, id:int")

# COMMAND ----------

# Note the name in lowercase
display(people)

# COMMAND ----------

from pyspark.sql.functions import udf

# Create a wrapper function for our library
def format(s):
    return formatter.decorate(s)

format_udf = udf(format) # Register the function as a udf

people2 = people.withColumn("name", format_udf("name")) # Use the udf in pyspark

display(people2) # Voila! You successfully used a library.