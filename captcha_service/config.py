import os
import re


class Configure:
    # RabbitMQ credentials
    RABBITMQ_USER = os.getenv("RABBITMQ_USER")
    RABBITMQ_USER_PASSWORD = os.getenv("RABBITMQ_USER_PASSWORD", "")
    RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "")
    RABBITMQ_PORT = os.getenv("RABBITMQ_PORT", "")

    def validate(self):
        self._validate_rabbit_credentials()

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
