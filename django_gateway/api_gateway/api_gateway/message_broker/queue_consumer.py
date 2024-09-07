import aio_pika
import json
from channels.layers import get_channel_layer
from rabbit_mq_broker import MessageBroker


async def rabbitmq_consumer():
    connection = MessageBroker.connection
    async with connection:
        # Declare queue for incoming channel
        channel = await connection.channel()
        queue = await channel.declare_queue("django_gateway", durable=True)

        async def process_message(message: aio_pika.IncomingMessage):
            async with message.process():
                # Get data from incoming message
                response_message = json.loads(message.body)
                user_id = response_message.get("user_id")
                response_data = response_message.get("result")

                # Send the response to the correct WebSocket group using Redis
                channel_layer = get_channel_layer()
                await channel_layer.group_send(
                    f"user_{user_id}",
                    {
                        "type": "send_response",
                        "response": response_data
                    }
                )

        await queue.consume(process_message)
