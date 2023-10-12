import strawberry
import strawberry_django
from strawberry_django.relay import ListConnectionWithTotalCount

from server.app.blog.graph import filters as blog_filters
from server.app.blog.graph import orders as blog_orders
from server.app.blog.graph import types as blog_types

__all__ = ("Query",)


@strawberry.type
class Query:
    posts: ListConnectionWithTotalCount[blog_types.Post] = strawberry_django.connection(
        order=blog_orders.PostOrder,
        filters=blog_filters.PostFilter,
    )
    tags: list[blog_types.Tag] = strawberry_django.field()
    categories: list[blog_types.Category] = strawberry_django.field()
    comments: list[blog_types.Comment] = strawberry_django.field()
    test_error: float = strawberry.field(resolver=lambda: 1 / 0)
