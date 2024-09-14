from functools import wraps
from json.decoder import JSONDecodeError

from pika import BasicProperties

from initializing_connections import broker_obj
from models.universal_exeption import InternalException


def exception_handler(func):
    """
        Decorator for all controls.
        Main function intercepting an identifiable error: InternalException.
        Additional function, provide fault tolerance in the event of an unforeseen error.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except AssertionError:
            pass
        except TypeError:
            request_headers: BasicProperties = args[2]
            answer_key = request_headers.headers.get("answer_key")
            answer_user = request_headers.headers.get("answer_user")
            if answer_user and answer_key:
                broker_obj.send({"error": "Some data is wrong."}, recipient=answer_key, answer_user=answer_user)
            else:
                pass
        except InternalException as err:
            request_headers: BasicProperties = args[2]
            answer_key = request_headers.headers.get("answer_key")
            answer_user = request_headers.headers.get("answer_user")
            if answer_user and answer_key:
                broker_obj.send(err.args[0], recipient=answer_key, answer_user=answer_user)
            else:
                pass
        except Exception as err:
            print(err.args)

    return wrapper
