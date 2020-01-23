from pyspark.dbutils import DBUtils
from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()
dbutils = DBUtils(spark.sparkContext)
print(dbutils.fs.ls("dbfs:/"))
print(dbutils.secrets.listScopes())