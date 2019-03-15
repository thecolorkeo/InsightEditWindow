import os
import sys
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import explode

'''
Parses one XML file from S3 bucket
to TimescaleDB.
'''

def main(num):
	'''
	@num: int in range(1, 27). Corresponds to file name suffix in S3 bucket
	'''
	
	spark = SparkSession.builder.getOrCreate()
	
	df_raw = spark.read.format("xml") \
		.options(rowTag="revision", excludeAttribute=True) \
		.load("s3n://keo-s3-2/history" + num + ".xml.bz2").persist()
	# convert time string to timestamp
	df = df_raw.withColumn("time", df_raw.timestamp.cast(TimestampType()))

	# postgres credentials
	connectionProperties = {
		"user": ["POSTGRES_USER"],
		"password": os.environ["POSTGRES_PASSWORD"],
		"driver":"org.postgresql.Driver"
	}
	jdbcHostname = os.environ["POSTGRES_URL"]
	jdbcDatabase = "pages"
	jdbcPort = "5432"
	jdbcUrl = "jdbc:postgresql://{0}:{1}/{2}".format(jdbcHostname, jdbcPort, jdbcDatabase)

	df.select("id", "text", "time", "contributor.username") \
		.write.jdbc(url=jdbcUrl, table="history"+num, properties=connectionProperties, mode="overwrite")

if __name__ == '__main__':
	main(sys.argv[1])
    	os.environ["POSTGRES_URL"] = sys.argv[2]
    	os.environ["POSTGRES_USER"] = sys.argv[3]
    	os.environ["POSTGRES_PASSWORD"] = sys.argv[4]
