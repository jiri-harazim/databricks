from pyspark.sql import SparkSession

# Based on https://docs.databricks.com/dev-tools/databricks-connect.html


def get_dbutils(spark):
    try:
        from pyspark.dbutils import DBUtils
        dbutils = DBUtils(spark)
    except ImportError:
        import IPython
        dbutils = IPython.get_ipython().user_ns["dbutils"]
    return dbutils


def list_dbfs(path):
  spark = SparkSession.builder.getOrCreate()
  print(get_dbutils(spark).fs.ls(path))

