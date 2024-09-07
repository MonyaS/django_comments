import json

import aio_pika
from django.utils import timezone
from api_gateway.message_broker.abs_message_broker import ABSMessageBroker
from config import Configure


class MessageBroker(ABSMessageBroker):
    def __init__(self):
        self.channel = None

    async def send(self, data: dict, recipient):
        """
            Send a message to chanel and add timestamp to message.
        """
        data["timestamp"] = timezone.now().timestamp()
        await self.channel.default_exchange.publish(
            aio_pika.Message(body=json.dumps(data).encode()),
            routing_key=recipient
        )
        # TODO Need to send an additional message to logger or
        #  configure a default router for duplication any message to logger service

    async def connect(self):
        # Create a connection to RabbitMq

        self.connection = await aio_pika.connect_robust(
            url=Configure.RABBITMQ_HOST,
            port=Configure.RABBITMQ_PORT,
            login=Configure.RABBITMQ_USER,
            password=Configure.RABBITMQ_USER_PASSWORD
        )

        self.channel = await self.connection.channel()
