from.models import Token
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

class TokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get('Authorization')
        if not token:
            return None

        try:
            token = token.split(' ')[1]  # Remove 'Token ' prefix
            token_obj = Token.objects.get(token=token)
        except (IndexError, Token.DoesNotExist):
            raise AuthenticationFailed('Invalid token.')

        return (token_obj.user, token_obj)