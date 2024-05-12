import jwt
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.contrib.auth.middleware import get_user
from channels.db import database_sync_to_async
from django.conf import settings
from rest_framework_simplejwt.backends import TokenBackend
from .models import User

# import sync_to_async
# from channels.db import database_sync_to_async


class JWTAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        try:

            query_string = scope.get('query_string', b'').decode()


            # Get the token from the query string
            access_token = query_string.split('=')[1]

            # Get the user from the jwt token
            token_backend = TokenBackend(
                algorithm='HS256')
            data = token_backend.decode(
                access_token, verify=False)

            user = await database_sync_to_async(User.objects.get)(id=data['user_id'])

            scope['user'] = user

        except Exception as e:
            print(f"JWT Authentication Error: {e}")
        #     print(f"JWT Authentication Error: {e}")
            scope['user'] = AnonymousUser()

        return await self.inner(scope, receive, send)

    def get_token(self, scope):
        headers = dict(scope.get('headers', []))

        if b'Authorization' in headers:
            auth_header = headers[b'Authorization'].decode()
            if auth_header.startswith('Bearer '):
                return auth_header.split()[1]
        return None

    @database_sync_to_async
    def authenticate(self, token):
        try:
            jwt_value = JWTAuthentication().get_validated_token(token)
            return jwt_value.user
        except (InvalidToken, TokenError, AttributeError):
            return AnonymousUser()
