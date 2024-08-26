import time
import hashlib
import os

import jwt
from django.db import models
from django.db.models import Manager, QuerySet

from api_gateway.api_gateway.models.universal_exeption import InternalException


class User(models.Model):
    """
    Class that represent user in the system.

    Fields:
        email - user email address
        password - hashed user password
    """

    email = models.EmailField(unique=True)
    password = models.BinaryField()

    def get_token(self) -> str:
        """
            Generate a JWT token for user authentication.
        """
        self.email: str
        self.password: str
        dict_usr = {
            'generate_time': str(time.time()),
            'email': self.email,
            'user_password': self.password
        }
        return jwt.encode(dict_usr, os.getenv("AUTH_TOKEN_KEY"), algorithm='HS256')

    def check_password(self, user_password: str) -> bool:
        """
            Validate user_password with generated db hash.
        """
        db_password = self.password
        salt = db_password[:32]
        input_password_hash = hashlib.pbkdf2_hmac('sha256', user_password.encode('utf-8'), salt, 100000)
        return input_password_hash == db_password[32:]

    def __str__(self):
        return f"{self.email}:{self.password}"

    @classmethod
    def filter_user(cls, **kwargs) -> QuerySet:
        """
            Execute every user filter requests.
        """
        cls.objects: Manager
        return cls.objects.filter(**kwargs)

    @staticmethod
    def user_exists(**kwargs) -> bool:
        """
            Check if user exist in db.
        """
        return User.filter_user(**kwargs).exists()

    @staticmethod
    def _create_password_hash(user_password) -> bytes:
        """
            Method to generate a password hash for a new user.
        """
        salt = os.urandom(32)
        user_hash = hashlib.pbkdf2_hmac('sha256', user_password.encode('utf-8'), salt, 100000)
        return salt + user_hash

    @classmethod
    def authorize(cls, email: str, password: str) -> "User":
        """
            Get user from db and validate it`s password.
        """
        user = cls.filter_user(email=email.lower()).first()
        if not user:
            raise InternalException({"status": 0, "error": "User not found."}, 404)
        hashed_password = user.check_password(password)
        if hashed_password:
            return user
        else:
            raise InternalException({"status": 0, "error": "Login or password incorrect."}, 401)

    @classmethod
    def register_user(cls, email: str, password: str) -> "User":
        """
            Register a new user in db.
        """
        email = email.lower()
        if cls.user_exists(email=email):
            raise InternalException({"status": 0, "error": "User not found."}, 404)
        user = cls(email=email)
        user.password = cls._create_password_hash(password)
        user.save()
        return user
