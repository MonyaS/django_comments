from broker.rabbit_mq_broker import MessageBroker
from config import Configure
from db_connection.db_connection import DbConnection

# Initialize connections
Configure().validate()
db_obj = DbConnection()
broker_obj = MessageBroker()
db_obj.initial_migrations()

broker_obj.connect()
