import strawberry
import strawberry_django
import strawberry_django.auth

from server.app.authentication.graph import types as auth_types

__all__ = ("Query",)


@strawberry.type
class Query:
    users: list[auth_types.User] = strawberry_django.field()
    me: auth_types.User | None = strawberry_django.auth.current_user()  # type: ignore
