import json

from api_gateway.message_broker.rabbit_mq_broker import MessageBroker
from api_gateway.models import User, InternalException
from api_gateway.serializers.json_validator import JsonValidator
from channels import exceptions
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer


class CommentsConsumer(AsyncWebsocketConsumer):
    """
        Websocket consumer for comments.
    """

    async def connect(self):
        """
            If user pass JWT authorization
            self.scope['accept_connection'] will be True and Websocket accept a request,
            else will be raised DenyConnection error.
        """
        if not self.scope['accept_connection']:
            raise exceptions.DenyConnection("Invalid token.")

        self.user_id = self.scope["user"].id
        self.group_name = f"user_{self.user_id}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)

        await self.accept()
        # TODO After success connet to WebSocket user must get a list of all added comments and a Captcha data
        #  for creating a new comment

    async def disconnect(self, close_code):
        if self.scope['accept_connection']:
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        user_obj: User = self.scope["user"]
        data_json = json.loads(text_data)
        try:
            data = JsonValidator(name="add_comment", dict_data=data_json).validate_comment()
        except InternalException as err:
            await self.send(str(err.args[0]))
            return

        await self.send("Your data is right." + str(text_data))
        # TODO Check if user Captcha is valid

        # Get a message broker object and send user data to comments microservice
        self.broker = await MessageBroker()
        await self.broker.send(
            {
                "user_id": user_obj.id,
                "username": user_obj.username,
                "mailbox_address": user_obj.mailbox_address,
                "home_page": data["home_page"],
                "text": data["text"],
                "parent_id": data["parent_id"]
            }, "comments", "add")

        # TODO as an answer to any message from user, need to send a new Captcha
        #  from Captcha microservice for a new comment
