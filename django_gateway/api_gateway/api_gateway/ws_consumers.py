import json
from channels import exceptions
from channels.generic.websocket import WebsocketConsumer


class CommentsConsumer(WebsocketConsumer):
    """
        Websocket consumer for comments.
    """
    def connect(self):
        """
            If user pass JWT authorization
            self.scope['accept_connection'] will be True and Websocket accept a request,
            else will be raised DenyConnection error.
        """
        if not self.scope['accept_connection']:
            raise exceptions.DenyConnection("Invalid token.")
        self.accept()
        self.send(text_data=json.dumps({
            'message': "Hellow world!!!!!!!!!!!"
        }))

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        self.send(text_data=json.dumps({
            'message': message
        }))
