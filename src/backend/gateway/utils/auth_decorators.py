from functools import wraps

from graphql_jwt import exceptions, shortcuts, utils


def view_login_required(func):
    """
    Decorator for checking if user is logged in
    """

    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        token = utils.get_credentials(request, kwargs=kwargs)

        if not token:
            raise exceptions.PermissionDenied()

        user = shortcuts.get_user_by_token(token)

        if not user:
            raise exceptions.PermissionDenied()

        request.user = user

        return func(self, request, *args, **kwargs)

    return wrapper
