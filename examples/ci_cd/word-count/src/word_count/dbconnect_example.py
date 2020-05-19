import os
from pyspark.sql import SparkSession
from pyspark.dbutils import DBUtils


# Useful to debug if you have eg sdkman installed
# print(os.environ['PATH'])

# Get spark session. It is a proxy object for the remote Databricks SparkSession.
spark = SparkSession\
.builder\
.getOrCreate()

dbutils = DBUtils(spark.sparkContext)


def simple_count():
  print("Testing simple count\n")
  # The Spark code will execute on the Azure Databricks cluster.
  print(spark.range(100).count())

# simple_count()

def parquet_count():
  print(spark.read.format("parquet").load("dbfs:/mnt/jiri-training-sources/initech/orders/").count())


def list_adls():
  dbutils = DBUtils(spark.sparkContext)
  print(dbutils.fs.ls("dbfs:/"))
  print(dbutils.secrets.listScopes())


# list_adls()

# from myfunctions import upper

def write_csv_file():
  peopleList = [('Alice', 1)]
  peopleDF = spark.createDataFrame(peopleList, ['name', 'age'])
  dbutils.fs.rm("/mnt/jiri/people-csv-20191021/", True)
  peopleDF.write.format("csv").save("/mnt/jiri/people-csv-20191021/")


def word_count():
  peopleList = [('Alice', 21), ('Bob', 27), ('Joe', 33)]
  peopleDF = spark.createDataFrame(peopleList, ['name', 'age'])
  return peopleDF.count()


print(word_count())