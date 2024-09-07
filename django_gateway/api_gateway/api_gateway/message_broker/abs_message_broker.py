from abc import ABC, abstractmethod


class MessageBrokerSingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
            instance.connect()
        return cls._instances[cls]


class ABSMessageBroker(ABC, metaclass=MessageBrokerSingletonMeta):
    connection = None

    @abstractmethod
    async def connect(self):
        """
            Create a connection to message broker and write it to self.connection
        """
        pass

    @abstractmethod
    async def send(self, data, recipient):
        """
            Method must get a data and send it to recipient, using self.connection
        """
        pass
