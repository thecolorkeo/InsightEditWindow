from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import explode

'''
Unit test for Wikipedia's
NYC page entry.
'''

spark = SparkSession.builder.getOrCreate()

def xmlWriteFrom (file):
	df = spark.read.format("xml") \
		.options(rowTag="page", excludeAttribute=True) \
		.load(file)
	df2 = df.withColumn("rev", explode(df.revision))
	df2.printSchema()
	df2.show()

	connectionProperties = {
		"user":"postgres",
		"password":"password",
		"driver":"org.postgresql.Driver"
	}
	jdbcHostname = "ec2-3-94-24-76.compute-1.amazonaws.com"
	jdbcDatabase = "pages"
	jdbcPort = "5432"
	jdbcUrl = "jdbc:postgresql://{0}:{1}/{2}".format(jdbcHostname, jdbcPort, jdbcDatabase)

	df2.select('id', 'rev.text', 'rev.timestamp') \
		.write.jdbc(url=jdbcUrl, table='revs', properties=connectionProperties, mode='overwrite')

xmlWriteFrom("s3n://keo-s3-1/wiki-nyc.xml.bz2")
