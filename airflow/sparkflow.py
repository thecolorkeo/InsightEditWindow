from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
import os

#generic spark submit
sparkSubmit = 'spark-submit --master spark://ec2-3-93-99-240.compute-1.amazonaws.com:7077 --conf spark.executor.extraJavaOptions="-XX:MaxPermSize=6g" --driver-memory 28g --executor-memory 6500m --executor-cores 1 --packages com.databricks:spark-xml_2.11:0.4.1,org.postgresql:postgresql:42.2.5 ~/databricks-history.py '

#define dag
default_args = {
    'owner': 'keo',
    'depends_on_past': False,
    'start_date': datetime(2016, 10, 15),
    'retries': 5,
    'retry_delay': timedelta(minutes=5),
}
dag = DAG('sparkflow',
    default_args=default_args,
    schedule_interval='@once')

spark1 = BashOperator(
    task_id = 'spark1',
    bash_command = sparkSubmit + '1',
    dag = dag)

spark2 = BashOperator(
    task_id = 'spark2',
    bash_command = sparkSubmit + '2',
    dag = dag)

spark3 = BashOperator(
    task_id = 'spark3',
    bash_command = sparkSubmit + '3',
    dag = dag)

spark4 = BashOperator(
    task_id = 'spark4',
    bash_command = sparkSubmit + '4',
    dag = dag)

spark5 = BashOperator(
    task_id = 'spark5',
    bash_command = sparkSubmit + '5',
    dag = dag)

spark6 = BashOperator(
    task_id = 'spark6',
    bash_command = sparkSubmit + '6',
    dag = dag)

spark7 = BashOperator(
    task_id = 'spark7',
    bash_command = sparkSubmit + '7',
    dag = dag)

spark8 = BashOperator(
    task_id = 'spark8',
    bash_command = sparkSubmit + '8',
    dag = dag)

spark9 = BashOperator(
    task_id = 'spark9',
    bash_command = sparkSubmit + '9',
    dag = dag)

spark10 = BashOperator(
    task_id = 'spark10',
    bash_command = sparkSubmit + '10',
    dag = dag)

spark11 = BashOperator(
    task_id = 'spark11',
    bash_command = sparkSubmit + '11',
    dag = dag)

spark12 = BashOperator(
    task_id = 'spark12',
    bash_command = sparkSubmit + '12',
    dag = dag)

spark13 = BashOperator(
    task_id = 'spark13',
    bash_command = sparkSubmit + '13',
    dag = dag)

spark14 = BashOperator(
    task_id = 'spark14',
    bash_command = sparkSubmit + '14',
    dag = dag)

spark15 = BashOperator(
    task_id = 'spark15',
    bash_command = sparkSubmit + '15',
    dag = dag)

spark16 = BashOperator(
    task_id = 'spark16',
    bash_command = sparkSubmit + '16',
    dag = dag)

spark17 = BashOperator(
    task_id = 'spark17',
    bash_command = sparkSubmit + '17',
    dag = dag)

spark18 = BashOperator(
    task_id = 'spark18',
    bash_command = sparkSubmit + '18',
    dag = dag)

spark19 = BashOperator(
    task_id = 'spark19',
    bash_command = sparkSubmit + '19',
    dag = dag)

spark20 = BashOperator(
    task_id = 'spark20',
    bash_command = sparkSubmit + '20',
    dag = dag)

spark21 = BashOperator(
    task_id = 'spark21',
    bash_command = sparkSubmit + '21',
    dag = dag)

spark22 = BashOperator(
    task_id = 'spark22',
    bash_command = sparkSubmit + '22',
    dag = dag)

spark23 = BashOperator(
    task_id = 'spark23',
    bash_command = sparkSubmit + '23',
    dag = dag)

spark24 = BashOperator(
    task_id = 'spark24',
    bash_command = sparkSubmit + '24',
    dag = dag)

spark25 = BashOperator(
    task_id = 'spark25',
    bash_command = sparkSubmit + '25',
    dag = dag)

spark26 = BashOperator(
    task_id = 'spark26',
    bash_command = sparkSubmit + '26',
    dag = dag)

spark27 = BashOperator(
    task_id = 'spark27',
    bash_command = sparkSubmit + '27',
    dag = dag)

spark2.set_upstream(spark1)
spark3.set_upstream(spark2)
spark4.set_upstream(spark3)
spark5.set_upstream(spark4)
spark6.set_upstream(spark5)
spark7.set_upstream(spark6)
spark8.set_upstream(spark7)
spark9.set_upstream(spark8)
spark10.set_upstream(spark9)
spark11.set_upstream(spark10)
spark12.set_upstream(spark11)
spark13.set_upstream(spark12)
spark14.set_upstream(spark13)
spark15.set_upstream(spark14)
spark16.set_upstream(spark15)
spark17.set_upstream(spark16)
spark18.set_upstream(spark17)
spark19.set_upstream(spark18)
spark20.set_upstream(spark19)
spark21.set_upstream(spark20)
spark22.set_upstream(spark21)
spark23.set_upstream(spark22)
spark24.set_upstream(spark23)
spark25.set_upstream(spark24)
spark26.set_upstream(spark25)
spark27.set_upstream(spark26)
