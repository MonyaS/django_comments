import json
from datetime import datetime

import pika
import pytz

from config import Configure


class MessageBroker:
    def __init__(self):
        self.queue = None
        self.connection = None
        self.channel = None

    def connect(self):
        # Create a connection to RabbitMq
        credentials = pika.PlainCredentials(
            username=Configure.RABBITMQ_USER,
            password=Configure.RABBITMQ_USER_PASSWORD)

        connection_parameters = pika.ConnectionParameters(
            host=Configure.RABBITMQ_HOST,
            port=Configure.RABBITMQ_PORT,
            credentials=credentials)

        self.connection = pika.BlockingConnection(connection_parameters)

        # Declare needed queue for service
        self.channel = self.connection.channel()
        self.queue = self.channel.queue_declare(queue='comments', durable=True)

    def send(self, data: dict, recipient: str):
        """
            Send a message to chanel and add timestamp to message.
            Input fields:
                - data: dict body of message
                - recipient: routing key of recipient queue
        """
        timezone = pytz.timezone('Europe/Kiev')
        data["timestamp"] = datetime.now(timezone).replace(tzinfo=None, microsecond=0).timestamp()
        self.channel.basic_publish(exchange='',
                                   routing_key=recipient,
                                   body=json.dumps(data).encode())
