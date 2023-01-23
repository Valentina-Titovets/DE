from airflow.sensors.s3_key_sensor import S3KeySensor
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.dates import days_ago


default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=1),
    'execution_timeout': timedelta(hours=1),
    'depends_on_past': False
    }


dag = DAG(
    's3_test',
    start_date=days_ago(1),
    max_active_runs=1,
    schedule_interval='* 60 * 60 *',
    default_args=default_args,
    catchup=False
    )


start = DummyOperator(
    dag=dag,
    task_id='start'
    )


s3_key = S3KeySensor(
    task_id='s3_key',
    bucket_key='/data.csv',
    aws_conn_id='aws_test',
    poke_interval=0,
    timeout=10,
    soft_fail=True,
    bucket_name='dp-external-repository',
    verify=False)




end = DummyOperator(
    dag=dag,
    task_id='end'
    )


start >> s3_key >> end





