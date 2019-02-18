import sys
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import explode

'''
Parses one XML file from S3 bucket
to TimescaleDB. Takes one argument
from command line which should be
an integer between 1 and 27.
'''

spark = SparkSession.builder.getOrCreate()

def xmlWriteFrom (num):
	df_raw = spark.read.format("xml") \
		.options(rowTag="revision", excludeAttribute=True) \
		.load("s3n://keo-s3-2/history" + num + ".xml.bz2").persist()
	# convert time string to timestamp
	df = df_raw.withColumn("time", df_raw.timestamp.cast(TimestampType()))

	connectionProperties = {
		"user":"postgres",
		"password":"password",
		"driver":"org.postgresql.Driver"
	}
	jdbcHostname = "ec2-3-94-24-76.compute-1.amazonaws.com"
	jdbcDatabase = "pages"
	jdbcPort = "5432"
	jdbcUrl = "jdbc:postgresql://{0}:{1}/{2}".format(jdbcHostname, jdbcPort, jdbcDatabase)

	df.select("id", "text", "time", "contributor.username") \
		.write.jdbc(url=jdbcUrl, table="history"+num, properties=connectionProperties, mode="append")

if __name__ == '__main__':
	xmlWriteFrom(sys.argv[1])
