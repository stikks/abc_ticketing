from django.contrib.auth import authenticate, login

from app import models


def authenticate_user(request, username, password):
    """
    authenticate user
    :return:
    """
    try:
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)

        return user
    except Exception as e:
        raise e


def register_user(request, **kwargs):
    """
    register new user account
    :param request:
    :param kwargs:
    :return:
    """
    try:
        user = models.Account.objects.create_user(**kwargs)

        if user:
            login(request, user)

        return user
    except Exception as e:
        raise e
