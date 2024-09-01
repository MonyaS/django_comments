import hashlib
import os
import time
from typing import Union

import jwt
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.db import models
from django.db.models import Manager, QuerySet
from jwt import InvalidTokenError

from api_gateway.models.universal_exeption import InternalException
from config import Configure


class User(models.Model):
    """
    Class that represent user in the system.

    Fields:
        mailbox_address - user mailbox_address address
        username - username in the system
        password - hashed user password
    """

    mailbox_address = models.EmailField(unique=True)
    username = models.TextField(max_length=32, unique=True)
    password = models.BinaryField()

    def get_cookies_token(self) -> str:
        """
            Generate a JWT token for user authentication.
        """
        dict_usr = {
            'generate_time': str(time.time()),
            'mailbox_address': self.mailbox_address
        }
        return f"Bearer {jwt.encode(dict_usr, Configure.AUTH_TOKEN_KEY, algorithm='HS256')}"

    def get_ws_token(self) -> str:
        dict_usr = {
            'live_time': str(time.time() + 900),  # Token live for a 15 minutes
            'mailbox_address': self.mailbox_address,
        }
        return f"Bearer {jwt.encode(dict_usr, Configure.WS_TOKEN_KEY, algorithm='HS256')}"

    def check_password(self, user_password: str) -> bool:
        """
            Validate user_password with generated db hash.
        """
        db_password = self.password.tobytes()
        salt = db_password[:32]
        input_password_hash = hashlib.pbkdf2_hmac('sha256', user_password.encode('utf-8'), salt, 100000)
        return input_password_hash == db_password[32:]

    def __str__(self):
        return f"{self.mailbox_address}:{self.password}"

    @classmethod
    def filter_user(cls, **kwargs) -> QuerySet:
        """
            Execute every user filter requests.
        """
        cls.objects: Manager
        return cls.objects.filter(**kwargs)

    @staticmethod
    def create_password_hash(user_password) -> bytes:
        """
            Method to generate a password hash for a new user.
        """
        salt = os.urandom(32)
        user_hash = hashlib.pbkdf2_hmac('sha256', user_password.encode('utf-8'), salt, 100000)
        return salt + user_hash

    @classmethod
    def authorize(cls, mailbox_address: str, password: str) -> "User":
        """
            Get user from db and validate it`s password.
        """
        user: "User" = cls.filter_user(mailbox_address=mailbox_address).first()
        if not user:
            raise InternalException({"status": 0, "error": "User not found."}, 404)
        hashed_password = user.check_password(password)
        if hashed_password:
            return user
        else:
            raise InternalException({"status": 0, "error": "Login or password incorrect."}, 401)

    @classmethod
    def get_user_from_auth_token(cls, token: str) -> tuple[bool, Union[AnonymousUser, "User"]]:
        """
            Method to authorize user from their JWT token.
            If user not found or their token invalid, returns AnonymousUser.
        """
        try:
            payload = jwt.decode(token, Configure.AUTH_TOKEN_KEY, algorithms=["HS256"])
            user = cls.objects.get(mailbox_address=payload['mailbox_address'])
            return True, user
        except (InvalidTokenError, User.DoesNotExist):
            return False, AnonymousUser()

    @classmethod
    @database_sync_to_async
    def get_user_from_ws_token(cls, token: str) -> tuple[bool, Union[AnonymousUser, "User"]]:
        """
            Method to authorize user from their JWT token.
            If user not found or their token invalid, returns AnonymousUser.
        """
        try:
            payload = jwt.decode(token, Configure.WS_TOKEN_KEY, algorithms=["HS256"])
            if float(payload.get("live_time", 0)) < time.time():
                raise InvalidTokenError
            user = cls.objects.get(mailbox_address=payload['mailbox_address'])
            return True, user
        except (InvalidTokenError, User.DoesNotExist):
            return False, AnonymousUser()
