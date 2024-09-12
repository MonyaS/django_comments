import json

from pika import BasicProperties

from broker.rabbit_mq_broker import MessageBroker
from config import Configure
from db_connection.db_connection import DbConnection
from models.exeption_handler import exception_handler
from models.message import Message

# Initialize connections
Configure().validate()

db_obj = DbConnection()
db_obj.initial_migrations()

broker_obj = MessageBroker()
broker_obj.connect()


# Function with incoming message processing logic
@exception_handler
def callback(_ch, _method, properties: BasicProperties, body):
    json_body = json.loads(body)
    message_obj = Message(headers=properties.headers, body=json_body)
    if message_obj.method == "get":
        comments = DbConnection().get_all_comments()

        # Create a dictionary to store children of each comment
        comment_dict = {comment.id: comment.__dict__ for comment in comments}
        tree_comments = []

        for comment in comments:
            parent_id = comment.parent_id
            if parent_id is None:
                tree_comments.append(comment)
            else:
                comment_dict[parent_id]['children'].append(comment)
        broker_obj.send({"comments": tree_comments}, recipient=message_obj.answer_key)
    elif message_obj.method == "add":
        message_obj.get_comment()
        inserted_id = DbConnection.add_comment_to_db(message_obj.comment)

        broker_obj.send({"inserted_id": inserted_id}, recipient=message_obj.answer_key)
    else:
        pass


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
