import strawberry
import strawberry_django

from server.app.blog.graph import types as blog_types

__all__ = ("Query",)


@strawberry.type
class Query:
    posts: list[blog_types.Post] = strawberry_django.field()
    tags: list[blog_types.Tag] = strawberry_django.field()
    categories: list[blog_types.Category] = strawberry_django.field()
    comments: list[blog_types.Comment] = strawberry_django.field()
