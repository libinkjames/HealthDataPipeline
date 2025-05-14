from airflow import DAG
from airflow.operators.empty import EmptyOperator
from datetime import datetime
from plugins.sensors.kafka_sensor import KafkaMessageSensor
from plugins.utils.config_loader import config 
from airflow.operators.python import PythonOperator
import logging

# Kafka Config
KAFKA_BROKER = config["kafka"]["broker"]
KAFKA_TOPIC = config["kafka"]["topic"]

# Define processing function before using it
def process_transform_store_message(**kwargs):
    conf = kwargs['dag_run'].conf or {}
    data = conf.get("data")  # data passed from FastAPI trigger

    if data:
        logging.info(f"Received data: {data}")

with DAG(
    dag_id="fitbit_data_dag",
    start_date=datetime(2025, 5, 1),
    description="Process and store IoT data",
    schedule_interval=None,
    catchup=False,
) as dag:

    start = EmptyOperator(task_id="start")

    kafka_sensor = KafkaMessageSensor(
        task_id="listen_to_fitbit_data",
        topic=KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BROKER
    )

    process_transform_store_data_task = PythonOperator(
        task_id="process_transform_store_data",
        python_callable=process_transform_store_message,
    )

    end = EmptyOperator(task_id="end")

    # Set task dependencies
    start >> kafka_sensor >> process_transform_store_data_task >> end
