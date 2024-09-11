import psycopg2

from config import Configure
from models.universal_exeption import InternalException


class DbConnectionSingletonMeta(type):
    _instances = {}

    async def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class DbConnection(metaclass=DbConnectionSingletonMeta):
    connection = psycopg2.connect(**Configure.get_db_connection_credentials(), client_encoding="utf8")
    cursor = connection.cursor()

    def __init__(self):
        self.initial_migrations()

    def execution_sql(self, func):
        """
            Decorator for all methods that contains modifying SQL requests.
            Designed to intercept possible errors in the query and provide a fail-safe connection to the database.
        """
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception:
                self.connection.rollback()
                raise InternalException({"error": "Your data isn't valid."})

        return wrapper

    @execution_sql
    def initial_migrations(self):
        """
            Execute initial migrations to DB.
        """
        with open("Initial_db_migrations.sql", "r") as file:
            sql_content = file.read()

        self.cursor.execute(sql_content.replace("{db_name}", f'"{Configure.DB_NAME}"'))
        self.connection.commit()
