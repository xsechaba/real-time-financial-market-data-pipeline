"""
Market data pipeline DAG.
"""
from datetime import datetime, timedelta
import logging
import os
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from airflow.models import Variable
from airflow.hooks.base import BaseHook

# Set up logging
logger = logging.getLogger(__name__)

def task_failure_callback(context):
    """Handle task failures."""
    task_instance = context['task_instance']
    logger.error(f"Task {task_instance.task_id} failed in DAG {task_instance.dag_id}")

def task_success_callback(context):
    """Handle task success."""
    task_instance = context['task_instance']
    logger.info(f"Task {task_instance.task_id} succeeded in DAG {task_instance.dag_id}")

def verify_connections():
    """Verify all required connections are available."""
    try:
        # Check database connection
        logger.info("Verifying database connection...")
        db_conn = BaseHook.get_connection('postgres_default')
        logger.info("Database connection verified")
        
        # Log pipeline start
        logger.info("Market data pipeline starting")
        return "Connections verified!"
    except Exception as e:
        logger.error(f"Connection verification failed: {str(e)}")
        raise

# Common environment variables
env_vars = {
    'PYTHONPATH': '/opt/airflow/src:${PYTHONPATH}',
    'DB_HOST': 'postgres',
    'DB_PORT': '5432',
    'DB_NAME': 'financial_data',
    'DB_USER': 'postgres',
    'DB_PASSWORD': 'postgres',
}

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'retry_exponential_backoff': True,
    'max_retry_delay': timedelta(minutes=30),
    'on_failure_callback': task_failure_callback,
    'on_success_callback': task_success_callback,
    'execution_timeout': timedelta(minutes=30),
}

# Create the DAG
with DAG(
    'market_data_pipeline',
    default_args=default_args,
    description='Pipeline for processing financial market data',
    schedule_interval='*/30 * * * *',  # Run every 30 minutes
    catchup=False,
    tags=['market_data', 'stocks'],
    max_active_runs=1
) as dag:

    # Verify connections task
    verify_task = PythonOperator(
        task_id='verify_connections',
        python_callable=verify_connections,
        retries=5,
        retry_delay=timedelta(seconds=30),
    )

    # Data ingestion task
    ingest_data = BashOperator(
        task_id='ingest_data',
        bash_command='python /opt/airflow/src/ingestion/data_ingestion.py',
        env=env_vars
    )

    # Data processing task (using Pandas)
    process_data = BashOperator(
        task_id='process_data',
        bash_command='python /opt/airflow/src/processing/data_processor.py',
        env=env_vars
    )

    # Set task dependencies
    verify_task >> ingest_data >> process_data 