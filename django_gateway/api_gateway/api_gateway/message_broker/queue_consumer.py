import asyncio

import aio_pika
import json
from channels.layers import get_channel_layer
from api_gateway.message_broker.rabbit_mq_broker import MessageBroker


async def rabbitmq_consumer():
    broker_obj = await MessageBroker()
    # Declare queue for incoming channel
    channel = await broker_obj.connection.channel()
    queue = await channel.declare_queue("api_gateway", durable=True)

    async def process_message(message: aio_pika.IncomingMessage):
        async with message.process():
            # Get data from incoming message
            user_group = message.headers.get("answer_user")
            answer_type = message.headers.get("answer_type")
            response_message = json.loads(message.body)
            # Send the response to the correct WebSocket group using Redis
            channel_layer = get_channel_layer()
            await channel_layer.group_send(
                user_group,
                {
                    "type": answer_type,
                    "response": response_message
                }
            )

    await queue.consume(process_message)
    try:
        # Wait until terminate
        await asyncio.Future()
    finally:
        await broker_obj.connection.close()
