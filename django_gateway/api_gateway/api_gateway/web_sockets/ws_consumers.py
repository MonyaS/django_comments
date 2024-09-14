import json

from asgiref.sync import sync_to_async
from django.db.models import QuerySet

from api_gateway.message_broker.rabbit_mq_broker import MessageBroker
from api_gateway.models import User, InternalException
from api_gateway.serializers.json_validator import JsonValidator
from channels import exceptions
from channels.generic.websocket import AsyncWebsocketConsumer


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

        self.group_name = f"user_{self.scope['user'].id}"

        self.broker = await MessageBroker()
        await self.broker.send({}, "comments", "get", self.group_name)

        await self.channel_layer.group_add(self.group_name, self.channel_name)

        # Add the user to the common group for all connected users
        self.common_group_name = "all_users"
        await self.channel_layer.group_add(self.common_group_name, self.channel_name)

        await self.accept()
        # TODO After success connet to WebSocket user must get a list of all added comments and a Captcha data
        #  for creating a new comment

    async def disconnect(self, close_code):
        if self.scope['accept_connection']:
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        user_obj: User = self.scope["user"]
        data_json: dict = json.loads(text_data)
        try:
            data = JsonValidator(name="add_comment", dict_data=data_json).validate_comment()
        except InternalException as err:
            await self.send(str(err.args[0]))
            return

        # TODO Check if user Captcha is valid

        # Get a message broker object and send user data to comments microservice
        await self.broker.send(
            {
                "user_id": user_obj.id,
                "home_page": data["home_page"],
                "text": data["text"],
                "parent_id": data["parent_id"] if data["parent_id"] else None
            }, "comments", "add", self.group_name)
        # TODO as an answer to any message from user, need to send a new Captcha
        #  from Captcha microservice for a new comment

    # Handler for 'get_comments' message type from broker consumer
    async def get_comments(self, response):
        comments = response["response"]["comments"]

        # Get a list if uniq user ids
        user_ids = set()
        stack = comments[:]
        while stack:
            comment = stack.pop()
            user_ids.add(comment['user_id'])
            stack.extend(comment['children'])

        # Get all users which create a comments
        users: list[User] = await User.get_users(user_ids)
        users_info = {user.id: {"mailbox_address": user.mailbox_address, "username": user.username} for user in users}

        def get_comment_user(comment_dict: dict):
            # Get information for this exactly comment
            info = users_info.get(comment_dict["user_id"])
            # Add user info to comment record
            comment_dict.update(info)

            # Create a recursive for all internal comments
            if comment_dict["children"]:
                for children_comment in comment_dict["children"]:
                    get_comment_user(children_comment)

        # Add a user info for all root comments
        for comment in comments:
            get_comment_user(comment)

        # Send the response message back to the WebSocket client
        await self.send(text_data=json.dumps(comments))

    # Handler for 'add_comment' message type from broker consumer
    async def add_comment(self, response):
        response = response["response"]
        # Get all users which create a comments
        user: User = await User.get_user((response["user_id"]))
        # Add user info to comment record
        response.update({"mailbox_address": user.mailbox_address, "username": user.username})

        # Send the response message back to the WebSocket client
        await self.send(text_data=json.dumps(response))
