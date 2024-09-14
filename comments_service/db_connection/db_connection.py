from typing import List

import psycopg2

from config import Configure
from models.comment import Comment
from models.universal_exeption import InternalException


class DbConnectionSingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


def execution_sql(func):
    """
        Decorator for all methods that contain modifying SQL requests.
        Designed to intercept possible errors in the query and provide a fail-safe connection to the database.
    """

    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception:
            self.connection.rollback()
            raise InternalException({"error": "Your data isn't valid."})

    return wrapper


class DbConnection(metaclass=DbConnectionSingletonMeta):

    def __init__(self):
        self.connection = psycopg2.connect(**Configure.get_db_connection_credentials(), client_encoding="utf8")
        self.cursor = self.connection.cursor()

    @execution_sql
    def initial_migrations(self):
        """
            Execute initial migrations to DB.
        """
        with open("db_connection/Initial_db_migrations.sql", "r") as file:
            sql_content = file.read()

        self.cursor.execute(sql_content.replace("{db_name}", f'"{Configure.DB_NAME}"'))
        self.connection.commit()

    @execution_sql
    def add_comment_to_db(self, comment: Comment):
        self.cursor.execute('''
                INSERT INTO "comments" 
                (user_id,
                parent_id,
                home_page,
                text
                )
                VALUES (%s,%s, %s, %s) RETURNING id''',
                            (comment.user_id, comment.parent_id, comment.home_page, comment.text))
        # Fetch the inserted ID
        inserted_id = self.cursor.fetchone()[0]
        self.connection.commit()
        return inserted_id

    def get_all_comments(self) -> List[Comment]:
        self.cursor.execute("SELECT * FROM comments")
        results_data = list(self.cursor.fetchall())
        comments = []
        for comment in results_data:
            record_id, user_id, parent_id, home_page, text = comment
            comments.append(Comment(record_id=record_id,
                                    user_id=user_id,
                                    parent_id=parent_id,
                                    home_page=home_page,
                                    text=text))

        return comments
