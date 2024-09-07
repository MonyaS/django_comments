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
    RABBITMQ_USER = os.getenv("RABBITMQ_USER", "")
    RABBITMQ_USER_PASSWORD = os.getenv("RABBITMQ_USER_PASSWORD", "")
    RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "")
    RABBITMQ_PORT = os.getenv("RABBITMQ_PORT", "")

    # Reddis credentials
    REDDIS_USER = os.getenv("REDDIS_USER", "")
    REDDIS_USER_PASSWORD = os.getenv("REDDIS_USER_PASSWORD", "")
    REDDIS_HOST = os.getenv("REDDIS_HOST", "")
    REDDIS_PORT = os.getenv("REDDIS_PORT", "")

    def validate(self):
        self._validate_db_credentials()
        self._validate_rabbit_credentials()
        self._validate_reddis_credentials()

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
            'DB_PORT': r'^\d+$'
        }

        if not re.match(patterns['RABBITMQ_USER'], self.RABBITMQ_USER):
            raise KeyError("RabbitMQ username isn`t valid.")

        if not re.match(patterns['RABBITMQ_USER_PASSWORD'], self.RABBITMQ_USER_PASSWORD):
            raise KeyError("RabbitMQ password is too weak. Password must contain at least 8 characters.")

        if not re.match(patterns['RABBITMQ_HOST'], self.RABBITMQ_HOST):
            raise KeyError("RabbitMQ host isn`t valid.")

        if not re.match(patterns['RABBITMQ_PORT'], self.RABBITMQ_PORT):
            raise KeyError("RabbitMQ port isn`t valid.")

    def _validate_reddis_credentials(self):
        # Reddis db data validation patterns
        patterns = {
            'REDDIS_USER': r'^\w+$',
            'REDDIS_USER_PASSWORD': r'^.{8,}$',
            'REDDIS_HOST': r'^[\w\.-]+$',
            'REDDIS_PORT': r'^\d+$'
        }

        if not re.match(patterns['REDDIS_USER'], self.REDDIS_USER):
            raise KeyError("Reddis username isn`t valid.")

        if not re.match(patterns['REDDIS_USER_PASSWORD'], self.REDDIS_USER_PASSWORD):
            raise KeyError("Reddis password is too weak. Password must contain at least 8 characters.")

        if not re.match(patterns['REDDIS_HOST'], self.REDDIS_HOST):
            raise KeyError("Reddis host isn`t valid.")

        if not re.match(patterns['REDDIS_PORT'], self.REDDIS_PORT):
            raise KeyError("Reddis port isn`t valid.")

    @staticmethod
    def get_reddis_connection_string():
        return f"redis://{Configure.REDDIS_USER}:{Configure.REDDIS_USER_PASSWORD}@" \
               f"{Configure.REDDIS_HOST}:{Configure.REDDIS_PORT}/0"
