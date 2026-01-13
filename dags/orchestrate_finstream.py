from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'bugra',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'finstream_pipeline',
    default_args=default_args,
    description='FinStream dbt transformation pipeline',
    schedule_interval=timedelta(hours=1),
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['finstream', 'dbt'],
) as dag:

    # 1. dbt debug
    dbt_debug = BashOperator(
        task_id='dbt_debug',
        bash_command='cd /opt/airflow/dbt_project/transform && export DBT_TARGET_PATH=/tmp/target && dbt debug --profiles-dir . --log-path /tmp'
    )

    # 2. dbt run
    dbt_run = BashOperator(
        task_id='dbt_run',
        bash_command='cd /opt/airflow/dbt_project/transform && export DBT_TARGET_PATH=/tmp/target && dbt run --profiles-dir . --log-path /tmp'
    )

    # 3. dbt test
    dbt_test = BashOperator(
        task_id='dbt_test',
        bash_command='cd /opt/airflow/dbt_project/transform && export DBT_TARGET_PATH=/tmp/target && dbt test --profiles-dir . --log-path /tmp'
    )

    dbt_debug >> dbt_run >> dbt_test