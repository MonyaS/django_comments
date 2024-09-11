from functools import wraps
from json.decoder import JSONDecodeError
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
        except TypeError:
            pass
            # return JsonResponse({"status": 0, "error": "Some data is wrong."}, status=401)
        except KeyError:
            pass
        except JSONDecodeError:
            # Appear when message contains invalid jason
            pass
        except InternalException as err:
            pass
            # return JsonResponse(err.args[0], status=err.args[1])

    return wrapper
