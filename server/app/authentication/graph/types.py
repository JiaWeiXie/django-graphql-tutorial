import strawberry
import strawberry_django
from django.contrib.auth import get_user_model

__all__ = (
    "User",
    "UserRegisterInput",
    "UserEditInput",
)

USER_MODEL = get_user_model()


@strawberry_django.type(USER_MODEL)
class User:
    id: strawberry.ID  # noqa: A003
    username: str
    first_name: str
    last_name: str
    email: str
    is_superuser: bool = strawberry.field(default=False)
    is_staff: bool = strawberry.field(default=False)
    is_active: bool = strawberry.field(default=True)


@strawberry_django.input(USER_MODEL)
class UserRegisterInput:
    username: str
    password: str


@strawberry_django.input(USER_MODEL)
class UserEditInput:
    username: str
    first_name: str
    last_name: str
    email: str
    is_superuser: bool | None = strawberry.field(default=False)
    is_staff: bool | None = strawberry.field(default=False)
    is_active: bool | None = strawberry.field(default=True)
