import time

from airflow import DAG
from airflow.decorators import task
from airflow.utils.timezone import datetime
from datetime import timedelta
from random import randint


@task
def task1():
    time.sleep(randint(1, 10))


with DAG(
    dag_id='otel_dag_author',
    start_date=datetime(2021, 1, 1),
    schedule_interval=timedelta(minutes=1),
    catchup=False
) as dag:

    task1()