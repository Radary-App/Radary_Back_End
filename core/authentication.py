from.models import Token, User
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class TokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get('Authorization')
        if not token:
            return None

        try:
            token = token.split(' ')[1]
            token_obj = Token.objects.get(token=token)
        except (IndexError, Token.DoesNotExist):
            raise AuthenticationFailed('Invalid token.')

        return (token_obj.user, token_obj)
    

class PhoneNumberBackend(ModelBackend):
    def authenticate(self, request, phone_number=None, password=None, **kwargs):
        User = get_user_model()
        try:
            # Check if a user with the given phone number exists
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            return None
        
        # Check the password and return the user if valid
        if user.check_password(password):
            return user
        return None