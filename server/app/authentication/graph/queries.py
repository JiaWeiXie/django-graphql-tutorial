import strawberry
import strawberry_django

from server.app.authentication.graph import types as auth_types

__all__ = ("Query",)


@strawberry.type
class Query:
    users: list[auth_types.User] = strawberry_django.field()
