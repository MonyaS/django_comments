from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from api_gateway.models import User, InternalException
from api_gateway.serializers.user_serializer import UserSerializer
from utils import exception_handler
from api_gateway.serializers.json_validator import JsonValidator


@require_http_methods(["POST"])
@exception_handler
def log_in(request: WSGIRequest) -> JsonResponse:
    """
    User login handler.
    """
    user_data = JsonValidator(name="users_login", request=request).validate()
    user = User.authorize(user_data.get("mailbox_address"), user_data.get("password"))
    response = JsonResponse({"status": 1}, headers={'authorization': user.get_ws_token()}, status=200)
    response.set_cookie(
        key="token",
        value=user.get_cookies_token(),
        httponly=True,
        samesite="Strict",
        # secure=True,
        max_age=86400
    )
    return response


@require_http_methods(["POST"])
@exception_handler
def register(request: WSGIRequest) -> JsonResponse:
    """
    User registration handler.
    """
    user_data = JsonValidator(name="users_register", request=request).validate()
    serializer = UserSerializer(data=user_data)
    if serializer.is_valid():
        user = serializer.save()
        response = JsonResponse({"status": 1}, headers={'authorization': user.get_ws_token()}, status=200)
        response.set_cookie(
            key="token",
            value=user.get_cookies_token(),
            httponly=True,
            samesite="Strict",
            # secure=True,
            max_age=86400
        )
        return response
    else:
        raise InternalException({"status": 0, "error": "Some data is wrong."}, 422)


@require_http_methods(["POST"])
@exception_handler
def refresh_token(request: WSGIRequest) -> JsonResponse:
    """
    Endpoint to refresh WebSocket user token.
    """
    token = request.COOKIES.get("token")
    # Extract the JWT token from the 'token' cookie
    if not token or not token.startswith('Bearer '):
        raise InternalException({"status": 0, "error": "Unauthorized."}, 403)

    # Check if token valid and if user with this token exist
    accept_refresh, user = User.get_user_from_auth_token(token.split(' ')[1])
    if accept_refresh:
        # Create an answer with new WebSocket token
        response = JsonResponse({"status": 1}, headers={'authorization': user.get_ws_token()}, status=200)
        response.set_cookie(
            key="token",
            value=token,
            httponly=True,
            samesite="Strict",
            # secure=True,
            max_age=86400
        )
        return response
    else:
        raise InternalException({"status": 0, "error": "Unauthorized."}, 403)
