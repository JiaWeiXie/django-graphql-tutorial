import strawberry_django
from django.contrib.auth import get_user_model

__all__ = ("User",)

USER_MODEL = get_user_model()


@strawberry_django.type(USER_MODEL)
class User:
    username: str
    first_name: str
    last_name: str
    email: str
