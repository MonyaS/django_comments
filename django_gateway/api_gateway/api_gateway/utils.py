from functools import wraps

from api_gateway.models import User
from api_gateway.models.universal_exeption import InternalException
from channels.middleware import BaseMiddleware
from django.http import JsonResponse
from channels.exceptions import StopConsumer
from rest_framework import exceptions


def exception_handler(func):
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


class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        headers = dict(scope['headers'])
        scope['accept_connection'] = False

        # Extract the JWT token from the 'authorization' header
        if b'authorization' in headers:
            auth_header = headers[b'authorization'].decode('utf8')
            if auth_header.startswith('Bearer '):
                scope['accept_connection'], scope['user'] = await User.get_user_from_jwt_token(
                    auth_header.split(' ')[1])

        return await super().__call__(scope, receive, send)
