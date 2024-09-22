"""
This module provides custom authentication classes for the Radary application.
Classes:
    TokenAuthentication(BaseAuthentication):
        Custom authentication class that authenticates users based on a token provided in the request headers.
        Methods:
            authenticate(request):
                Authenticates the user based on the 'Authorization' header in the request.
                Returns a tuple of (user, token) if authentication is successful, otherwise raises AuthenticationFailed.
    PhoneNumberBackend(ModelBackend):
        Custom authentication backend that allows users to authenticate using their phone number and password.
        Methods:
            authenticate(request, phone_number=None, password=None, **kwargs):
                Authenticates the user based on the provided phone number and password.
                Returns the user if authentication is successful, otherwise returns None.
"""

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from .models import Token

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
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:

            return None
        
        if user.check_password(password):
            return user

        return None