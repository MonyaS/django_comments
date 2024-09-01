import json

from channels import exceptions
from channels.generic.websocket import WebsocketConsumer

from api_gateway.models import User
from api_gateway.serializers.json_validator import JsonValidator


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
        # TODO After success connet to WebSocket user must get a list of all added comments and a Captcha data
        #  for creating a new comment

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        user_obj: User = self.scope["user"]
        data_json = json.loads(text_data)
        data = JsonValidator(name="add_comment", dict_data=data_json).validate_comment()
        # TODO Check if user Captcha is valid

        # TODO After receiving a message from user need to send a message to message microservice with data:
        #   {"username": user_obj.username, "mailbox_address": user_obj.mailbox_address, "home_page":data["home_page"],
        #   "text": data["text"}}

        # TODO as an answer to any message from user, need to send a new Captcha
        #  from Captcha microservice for a new comment
