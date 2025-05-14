import json


def parse_kafka_message(message):
 """
 Utility function to parse Kafka messages.
 """
 return json.loads(message)