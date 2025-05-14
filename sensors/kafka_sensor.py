from airflow.sensors.base import BaseSensorOperator
from kafka import KafkaConsumer


class KafkaMessageSensor(BaseSensorOperator):
 """
 Sensor to listen for Kafka messages on a specific topic.
 """
 def __init__(self, topic, bootstrap_servers, *args, **kwargs):
   super().__init__(*args, **kwargs)
   self.topic = topic
   self.bootstrap_servers = bootstrap_servers
 
 def poke(self, context):
    self.log.info(f"Listening for messages on topic: {self.topic}")
    consumer = KafkaConsumer(
    self.topic,
    bootstrap_servers=self.bootstrap_servers,
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='airflow_group'
    )
    for message in consumer:
       self.log.info(f"Received message: {message.value}")
       return True # Successfully received a message
    return False