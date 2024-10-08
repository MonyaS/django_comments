import os
import re


class Configure:
    SECRET_KEY = os.getenv("SECRET_KEY", "")

    AUTH_TOKEN_KEY = os.getenv("AUTH_TOKEN_KEY", "")
    WS_TOKEN_KEY = os.getenv("WS_TOKEN_KEY", "")

    # Db credentials
    DB_NAME = os.getenv("DB_NAME", "")
    DB_USER = os.getenv("DB_USER", "")
    DB_USER_PASSWORD = os.getenv("DB_USER_PASSWORD", "")
    DB_HOST = os.getenv("DB_HOST", "")
    DB_PORT = os.getenv("DB_PORT", "")

    # RabbitMQ credentials
    RABBITMQ_USER = os.getenv("RABBITMQ_USER")
    RABBITMQ_USER_PASSWORD = os.getenv("RABBITMQ_USER_PASSWORD", "")
    RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "")
    RABBITMQ_PORT = os.getenv("RABBITMQ_PORT", "")

    # Redis credentials
    REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")
    REDIS_HOST = os.getenv("REDIS_HOST", "")
    REDIS_PORT = os.getenv("REDIS_PORT", "")

    def validate(self):
        self._validate_db_credentials()
        self._validate_rabbit_credentials()
        self._validate_redis_credentials()

    def _validate_db_credentials(self):
        # Db data validation patterns
        patterns = {
            'DB_NAME': r'^\w+$',
            'DB_USER': r'^\w+$',
            'DB_USER_PASSWORD': r'^.{8,}$',
            'DB_HOST': r'^[\w\.-]+$',
            'DB_PORT': r'^\d+$'
        }

        if not re.match(patterns['DB_NAME'], self.DB_NAME):
            raise KeyError("Db name isn`t valid.")

        if not re.match(patterns['DB_USER'], self.DB_USER):
            raise KeyError("Db username isn`t valid.")

        if not re.match(patterns['DB_USER_PASSWORD'], self.DB_USER_PASSWORD):
            raise KeyError("Db password is too weak. Password must contain at least 8 characters.")

        if not re.match(patterns['DB_HOST'], self.DB_HOST):
            raise KeyError("Db host isn`t valid.")

        if not re.match(patterns['DB_PORT'], self.DB_PORT):
            raise KeyError("Db port isn`t valid.")

    def _validate_rabbit_credentials(self):
        # Db data validation patterns
        patterns = {
            'RABBITMQ_USER': r'^\w+$',
            'RABBITMQ_USER_PASSWORD': r'^.{8,}$',
            'RABBITMQ_HOST': r'^[\w\.-]+$',
            'RABBITMQ_PORT': r'^\d+$'
        }

        if not re.match(patterns['RABBITMQ_USER'], self.RABBITMQ_USER):
            raise KeyError("RabbitMQ username isn`t valid.")

        if not re.match(patterns['RABBITMQ_USER_PASSWORD'], self.RABBITMQ_USER_PASSWORD):
            raise KeyError("RabbitMQ password is too weak. Password must contain at least 8 characters.")

        if not re.match(patterns['RABBITMQ_HOST'], self.RABBITMQ_HOST):
            raise KeyError("RabbitMQ host isn`t valid.")

        if not re.match(patterns['RABBITMQ_PORT'], self.RABBITMQ_PORT):
            raise KeyError("RabbitMQ port isn`t valid.")

    def _validate_redis_credentials(self):
        # Redis db data validation patterns
        patterns = {
            'REDIS_PASSWORD': r'^.{8,}$',
            'REDIS_HOST': r'^[\w\.-]+$',
            'REDIS_PORT': r'^\d+$'
        }

        if not re.match(patterns['REDIS_PASSWORD'], self.REDIS_PASSWORD):
            raise KeyError("Redis password is too weak. Password must contain at least 8 characters.")

        if not re.match(patterns['REDIS_HOST'], self.REDIS_HOST):
            raise KeyError("Redis host isn`t valid.")

        if not re.match(patterns['REDIS_PORT'], self.REDIS_PORT):
            raise KeyError("Redis port isn`t valid.")

    @staticmethod
    def get_redis_connection_string():
        return f"redis://default:{Configure.REDIS_PASSWORD}@" \
               f"{Configure.REDIS_HOST}:{Configure.REDIS_PORT}/0"
