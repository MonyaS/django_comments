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
        self.queue = self.channel.queue_declare(queue='captcha_service', durable=True)

    def send(self, data: dict, recipient: str, answer_user: "", answer_type: str):
        """
            Send a message to chanel and add timestamp to message.
            Input fields:
                - data: dict body of message
                - recipient: routing key of recipient queue
                - answer_user: identifier of user that need to get an answer
                - answer_type: type of request-answer messages (get_comments,add_comment,error)
        """
        timezone = pytz.timezone('Europe/Kiev')
        data["timestamp"] = datetime.now(timezone).replace(tzinfo=None, microsecond=0).timestamp()
        headers = pika.BasicProperties(headers={'answer_user': answer_user, "answer_type": answer_type})
        self.channel.basic_publish(exchange='',
                                   routing_key=recipient,
                                   properties=headers,
                                   body=json.dumps(data).encode())
