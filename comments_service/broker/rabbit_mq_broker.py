import pika

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
