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


def word_count():
  peopleList = [('Alice', 21), ('Bob', 27), ('Joe', 33)]
  peopleDF = spark.createDataFrame(peopleList, ['name', 'age'])
  return peopleDF.count()


# print(word_count())