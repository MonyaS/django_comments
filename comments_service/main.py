import json

from pika import BasicProperties

from db_connection.db_connection import DbConnection
from initializing_connections import db_obj, broker_obj
from models.exeption_handler import exception_handler
from models.message import Message




# Function with incoming message processing logic
@exception_handler
def callback(_ch, _method, properties: BasicProperties, body):
    if body:
        json_body = json.loads(body)
    else:
        json_body = None
    message_obj = Message(headers=properties.headers, body=json_body)
    if message_obj.method == "get":
        comments = [item.__dict__ for item in DbConnection().get_all_comments()]
        # Create a dictionary to store children of each comment
        comment_dict = {comment["record_id"]: comment for comment in comments}
        tree_comments = []

        for comment in comments:
            parent_id = comment.pop("parent_id", None)
            if parent_id is None:
                tree_comments.append(comment)
            else:
                comment_dict[parent_id]['children'].append(comment)

        broker_obj.send(data={"comments": tree_comments}, recipient=message_obj.answer_key,
                        answer_user=message_obj.answer_user)
    elif message_obj.method == "add":
        message_obj.get_comment()
        DbConnection().add_comment_to_db(message_obj.comment)
        broker_obj.send(data=message_obj.comment.__dict__, recipient=message_obj.answer_key, answer_user="all")
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
