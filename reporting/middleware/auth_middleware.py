import os
import jwt
from django.http import HttpRequest
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication
from django.conf import settings
from django.middleware.csrf import CsrfViewMiddleware
from reporting.service.user_service import UserService
from reporting.models.user import User, UserSerializer

class CSRFCheck(CsrfViewMiddleware):
    def _reject(self, request, reason):
        # Return the failure reason instead of an HttpResponse
        return reason


class AuthMiddleware(BaseAuthentication):
    def __init__(self):
        self.user_service = UserService()

    def authenticate(self, request: HttpRequest):
        # OAuth2 Intercepted Requests will have this header.
        # Internal Apps can still invoke APIs unauthenticated.
        # TODO: Secure for Internal Apps as well
        exclude_path = ["/api/reporting/login"]
        if request.path not in exclude_path:
            authorization_header = request.headers.get('Authorization')

            if not authorization_header:
                return None
            try:
                access_token = authorization_header.split(' ')[1]
                payload = jwt.decode(
                    access_token, settings.SECRET_KEY, algorithms=['HS256'])

            except jwt.ExpiredSignatureError:
                raise exceptions.AuthenticationFailed('access_token expired')
            except IndexError:
                raise exceptions.AuthenticationFailed('Token prefix missing')
            print (f"payload: {payload}")
            user = User.objects.get(id=payload['user_id'])
            print (f"username: {user.username}")
            if user is None:
                raise exceptions.AuthenticationFailed('User not found')

            if not user.active:
                raise exceptions.AuthenticationFailed('user is inactive')
            print (f"active: {user.active}")

            self.enforce_csrf(request)

            if user.active:
                request.user = self._validate_user(user.username)
                return request.user, None
            elif os.getenv("env") == "dev" and os.getenv("user") is not None:
                # Locally X-Forwarded-Email is not set, and I don't want to whitelist CORS header and add it.
                # Instead, we support environment variable instead.
                request.user = self._validate_user(os.getenv("user"))
                return request.user, None

    def enforce_csrf(self, request):
        """
        Enforce CSRF validation
        """
        check = CSRFCheck()
        # populates request.META['CSRF_COOKIE'], which is used in process_view()
        check.process_request(request)
        reason = check.process_view(request, None, (), {})
        print(reason)
        if reason:
            # CSRF failed, bail with explicit error message
            raise exceptions.PermissionDenied('CSRF Failed: %s' % reason)

    def _validate_user(self, email):
        user = self.user_service.get_by_username(email)
        if not user:
            raise exceptions.PermissionDenied("Your user is not provisioned for the access!")
        else:
            return user
