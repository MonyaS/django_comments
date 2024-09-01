from channels.middleware import BaseMiddleware

from api_gateway.models import User


class JWTAuthMiddleware(BaseMiddleware):
    """
        Middleware for Websocket JWT authentication.
    """

    async def __call__(self, scope, receive, send):
        headers = dict(scope['headers'])
        scope['accept_connection'] = False

        # Extract the JWT token from the 'authorization' header
        if b'authorization' in headers:
            auth_header = headers[b'authorization'].decode('utf8')
            if auth_header.startswith('Bearer '):
                # Check if token valid and if user with this toke exist
                scope['accept_connection'], scope['user'] = \
                    await User.get_user_from_ws_token(auth_header.split(' ')[1])

        return await super().__call__(scope, receive, send)
