import os
import re


class Configure:
    # Db credentials
    DB_NAME = os.getenv("COMMENTS_DB_NAME", "")
    DB_USER = os.getenv("COMMENTS_DB_USER", "")
    DB_USER_PASSWORD = os.getenv("COMMENTS_DB_USER_PASSWORD", "")
    DB_HOST = os.getenv("COMMENTS_DB_HOST", "")
    DB_PORT = os.getenv("COMMENTS_DB_PORT", "")

    # RabbitMQ credentials
    RABBITMQ_USER = os.getenv("RABBITMQ_USER")
    RABBITMQ_USER_PASSWORD = os.getenv("RABBITMQ_USER_PASSWORD", "")
    RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "")
    RABBITMQ_PORT = os.getenv("RABBITMQ_PORT", "")

    def validate(self):
        self._validate_db_credentials()
        self._validate_rabbit_credentials()

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

    @staticmethod
    def get_db_connection_credentials() -> dict:
        connection_dict = {'dbname': Configure.DB_NAME,
                           'user': Configure.DB_USER,
                           'password': Configure.DB_USER_PASSWORD,
                           'port': Configure.DB_PORT,
                           'host': Configure.DB_HOST}
        return connection_dict
