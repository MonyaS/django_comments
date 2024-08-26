from functools import wraps

from django.http import JsonResponse

from api_gateway.api_gateway.models.universal_exeption import InternalException


def exception_handler(func):
    @wraps(func)
    def wrapper():
        try:
            return func()
        except TypeError:
            return JsonResponse({"status": 0, "error": "Some data is wrong."}, status=401)
        except KeyError:
            return JsonResponse({"status": 0, "error": "Some data is wrong."}, status=500)
        except InternalException as err:
            return JsonResponse({"status": 0, "error": err.exception_data}, status=err.exception_code)

    return wrapper
