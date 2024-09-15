from broker.rabbit_mq_broker import MessageBroker
from config import Configure

# Initialize connections
Configure().validate()
broker_obj = MessageBroker()

broker_obj.connect()
