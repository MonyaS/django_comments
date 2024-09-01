import pika

from api_gateway.message_broker.abs_message_broker import ABSMessageBroker
from config import Configure


class MessageBroker(ABSMessageBroker):
    def send(self, data, recipient):
        pass

    def connect(self):
        credentials = pika.PlainCredentials(Configure.RABBITMQ_USER, Configure.RABBITMQ_USER_PASSWORD)
        parameters = pika.ConnectionParameters(Configure.RABBITMQ_HOST,
                                               Configure.RABBITMQ_PORT,
                                               '/',
                                               credentials)

        self.connection = pika.BlockingConnection(parameters)
