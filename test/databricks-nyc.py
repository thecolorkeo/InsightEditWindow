from pyspark.sql import SparkSession
from pyspark.sql.types import *

spark = SparkSession.builder.getOrCreate()

def xmlWriteFrom (file):
	df = spark.read.format('xml') \
		.options(rowTag='revision', excludeAttribute=True) \
		.load(file)

	connectionProperties = {
		"user":"postgres",
		"password":"password",
		"driver":"org.postgresql.Driver"
	}
	jdbcHostname = "ec2-54-82-89-174.compute-1.amazonaws.com"
	jdbcDatabase = 'page'
	jdbcPort = '5432'
	jdbcUrl = "jdbc:postgresql://{0}:{1}/{2}".format(jdbcHostname, jdbcPort, jdbcDatabase)

	df.select('id', 'text', 'parentid', 'timestamp').write.jdbc(url=jdbcUrl, table='revs', properties=connectionProperties, mode='overwrite')

xmlWriteFrom('s3n://keo-s3-1/wiki-nyc.xml.bz2')
