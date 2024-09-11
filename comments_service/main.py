from pika import BasicProperties

from broker.rabbit_mq_broker import MessageBroker
import json

from models.exeption_handler import exception_handler
from models.message import Message

# Get main broker object and create connection
broker_obj = MessageBroker()
broker_obj.connect()


# Function with incoming message processing logic
@exception_handler
def callback(_ch, _method, _properties: BasicProperties, body):
    json_body = json.loads(body)
    Message(headers=_properties.headers, body=json_body)


# Create a connection to queue
broker_obj.channel.basic_consume(queue='comments',
                                 auto_ack=True,
                                 on_message_callback=callback)

try:
    # Starting service
    print("Comments server initialize successful.", flush=True)
    broker_obj.channel.start_consuming()
finally:
    broker_obj.connection.close()
