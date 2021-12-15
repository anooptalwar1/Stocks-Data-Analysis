from functools import wraps

from django.core.exceptions import PermissionDenied


def has_permission(permission: str):
    def request_decorator(dispatch):
        @wraps(dispatch)
        def wrapper(*args, **kwargs):
            request = args[1]
            user = request.user
            if permission.lower() in user.permissions:
                return dispatch(*args, **kwargs)
            else:
                raise PermissionDenied

        return wrapper

    return request_decorator
