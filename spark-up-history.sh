#!/bin/bash
spark-submit --master spark://ec2-3-93-99-240.compute-1.amazonaws.com:7077 \
	     --conf spark.executor.extraJavaOptions="-XX:MaxPermSize=6g" \
	     --driver-memory 28g \
	     --executor-memory 6500m \
	     --executor-cores 1 \
	     --packages com.databricks:spark-xml_2.11:0.4.1, \
			org.postgresql:postgresql:42.2.5 \
	     databricks-history.py $1
