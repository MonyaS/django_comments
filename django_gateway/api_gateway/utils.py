from functools import wraps

from django.http import JsonResponse
from rest_framework import exceptions

from api_gateway.models.universal_exeption import InternalException


def exception_handler(func):
    """
        Decorator for all controls endpoint.
        Main function intercepting an identifiable error: InternalException.
        Additional function, provide fault tolerance in the event of an unforeseen error.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except TypeError:
            return JsonResponse({"status": 0, "error": "Some data is wrong."}, status=401)
        except KeyError:
            return JsonResponse({"status": 0, "error": "Some data is wrong."}, status=500)
        except exceptions.ParseError:
            return JsonResponse({"status": 0, "error": "Some data is wrong."}, status=401)
        except InternalException as err:
            return JsonResponse({"status": 0, "error": err.exception_data}, status=err.exception_code)

    return wrapper


