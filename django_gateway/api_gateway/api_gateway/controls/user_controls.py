import time

from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from api_gateway.models import User, InternalException
from api_gateway.serializers.user_serializer import UserSerializer
from api_gateway.utils import exception_handler
from json_validator import JsonValidator


@require_http_methods(["POST"])
@exception_handler
def log_in(request: WSGIRequest) -> JsonResponse:
    """
    User login handler.
    """
    user_data = JsonValidator(request, "users_login").validate()
    user = User.authorize(user_data.get("mailbox_address"), user_data.get("password"))
    return JsonResponse({"status": 1, "data": {"token": user.get_token(), "timestamp": time.time()}}, status=200)


@require_http_methods(["POST"])
@exception_handler
def register(request: WSGIRequest) -> JsonResponse:
    """
    User registration handler.
    """
    user_data = JsonValidator(request, "users_register").validate()
    serializer = UserSerializer(data=user_data)
    if serializer.is_valid():
        user = serializer.save()

        return JsonResponse({"status": 1, "data": {"token": user.get_token(), "timestamp": time.time()}}, status=200)
    else:
        raise InternalException({"status": 0, "error": "Some data is wrong."}, 422)
