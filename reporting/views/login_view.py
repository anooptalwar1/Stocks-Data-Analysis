from rest_framework import viewsets, mixins, permissions
from rest_framework.settings import api_settings
from rest_framework.response import Response
from reporting.models.helpers.has_permission import has_permission
from reporting.models.user import User, UserSerializer
from rest_framework import authentication, exceptions
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
import jwt
from django.conf import settings
import datetime


class LoginView(viewsets.GenericViewSet):

    @method_decorator(ensure_csrf_cookie)
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        response = Response()
        if (username is None) or (password is None):
            raise exceptions.AuthenticationFailed(
                'username and password required')

        user = User.objects.filter(username=username).first()
        if(user is None):
            raise exceptions.AuthenticationFailed('user not found')
        if (not user.password == password):
            raise exceptions.AuthenticationFailed('wrong password')

        serialized_user = UserSerializer(user).data

        access_token = self.generate_access_token(user)
        refresh_token = self.generate_refresh_token(user)

        response.set_cookie(key='refreshtoken', value=refresh_token, httponly=True)
        response.data = {
            'access_token': access_token,
            'user': serialized_user,
        }

        return response

    def generate_access_token(self, user):

        access_token_payload = {
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=5),
            'iat': datetime.datetime.utcnow(),
        }
        access_token = jwt.encode(access_token_payload,
                                  settings.SECRET_KEY, algorithm='HS256')
        return access_token


    def generate_refresh_token(self, user):
        refresh_token_payload = {
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
            'iat': datetime.datetime.utcnow()
        }
        refresh_token = jwt.encode(
            refresh_token_payload, settings.REFRESH_TOKEN_SECRET, algorithm='HS256')

        return refresh_token